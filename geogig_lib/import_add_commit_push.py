# -*- coding: utf-8 -*-
import socket, time, sys, os, thread, platform
from repository import Repository
from thread_process import Thread_Process
from datetime import datetime
from utils import path
 
class Import_Add_Commit_Push:
   
    def __init__(self, config, logger=False):
        self.logger = logger
        self.user_data = config
        geogig_path = os.path.join(
            os.getcwd(),
            'geogig_bin',
            'bin',
            'geogig' if  platform.system() == 'Linux' else 'geogig.bat'
        )
        self.repository = Repository(
            self.user_data['machine_ip'],
            self.user_data['machine_port'],
            self.user_data['repository_db_name'],
            self.user_data['repository_schema_name'],
            self.user_data['repository_name'],
            self.user_data['database_user_name'],
            self.user_data['database_user_password'],
            geogig_path,
            self.logger
        )
    
    def spatial_test(self):
        if not('base' in self.user_data and self.user_data['base']):
            branch = self.user_data['branch_name']
            approved_layers_list, repproved_layers_list = self.repository.branches[branch].spatial_test(   
                self.user_data['machine_ip'],
                self.user_data['machine_port'],
                self.user_data['database_name'],
                self.user_data['database_user_name'],
                self.user_data['database_user_password']
            )
            self.logger.debug(u"***RESULT TEST SPATIAL***") if self.logger else ''
            print_approved = u"\n".join([ u"{} - {}".format(row[0], row[1]) for row in approved_layers_list])
            print_repproved = u"\n".join([ u"{} - {}".format(row[0], row[1]) for row in repproved_layers_list])
            self.logger.debug(u'LAYERS APPROVED BRANCH : {0} : \n{1}'.format(branch, print_approved)) if self.logger else ''
            self.logger.debug(u'LAYERS REPPROVED BRANCH : {0} : \n{1}'.format(branch, print_repproved)) if self.logger else ''
            return approved_layers_list, repproved_layers_list
        else:
            self.logger.debug(u"NO SPATIAL TEST AT 'BASE'") if self.logger else ''
    
    def pg_import(self):
        branch = self.user_data['branch_name']
        self.logger.debug(u"Geogig Import - user : {}".format(branch)) if self.logger else ''
        self.repository.branches[branch].pg_import_schema(   
            self.user_data['machine_ip'],
            self.user_data['machine_port'],
            self.user_data['database_name'],
            self.user_data['database_schema_name'],
            self.user_data['database_user_name'],
            self.user_data['database_user_password']
        
        )
    
    def push(self):
        branch = self.user_data['branch_name']
        if not('base' in self.user_data and self.user_data['base']): 
                self.repository.branches[branch].push(branch)
                self.logger.debug(u"Geogig Push : {0}".format(branch)) if self.logger else ''
    
    def add_commit(self, layers_list=False):
        branch = self.user_data['branch_name']
        status = self.repository.branches[branch].status() 
        if ( status and u'edgv' in status):
            self.repository.branches[branch].add(layers_list)
            self.repository.branches[branch].commit(
                u'commit diario - {0}'.format(branch)
            )
            self.logger.debug(u"Geogig Add, Commit - user : {0}".format(branch)) if self.logger else ''
        else:
            self.logger.info(u'Nothing to commit on {0}'.format(branch)) if self.logger else ''
        
    def run_process(self):
        self.logger.info(u"Init Import, Add, Commit and Push(if not base) - user : {0}".format(self.user_data['branch_name'])) if self.logger else ''
        self.repository.branches[self.user_data['branch_name']].clean_staging_area()
        branch = self.user_data['branch_name']
        self.pg_import()
        approved_layers_list, repproved_layers_list = self.spatial_test()
        if len(repproved_layers_list) > 0:
            self.add_commit([ row[1] for row in approved_layers_list])
            self.repository.branches[branch].clean_staging_area()
        else:
            self.add_commit()
        self.push()
        self.repository.branches[self.user_data['branch_name']].show_resume_commit_by_tag(u'commit')
        return True
           
if __name__ == '__main__':
    pass
     