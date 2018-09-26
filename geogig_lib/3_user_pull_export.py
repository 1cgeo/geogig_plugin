# -*- coding: utf-8 -*-
import socket, time, sys, os, thread, platform
from geogig import Repository
from thread_process import Thread_Process
from datetime import datetime
from users_data import USERS_REPO
from utils import Utils
 
class Pos_Process:
   
    def __init__(self, config, logger=False):
        self.logger = logger
        self.export_count = 0
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
    
    def export(self):
        branch = self.user_data['branch_name']
        self.logger.debug(u"Geogig Export - user : {0}".format(branch)) 
        self.repository.branches[branch].pg_export_schema(
            self.user_data['machine_ip'],
            self.user_data['machine_port'],
            self.user_data['database_name'],
            self.user_data['database_schema_name'],
            self.user_data['database_user_name'],
            self.user_data['database_user_password']
        )
        self.logger.debug(u"Geogig Import - user : {0}".format(branch)) 
        self.repository.branches[branch].pg_import_schema(   
                self.user_data['machine_ip'],
                self.user_data['machine_port'],
                self.user_data['database_name'],
                self.user_data['database_schema_name'],
                self.user_data['database_user_name'],
                self.user_data['database_user_password']
        )
        if (self.repository.branches[branch].status() and u'edgv' in self.repository.branches[branch].status()):
            if self.export_count == 0:
                self.export_count += 1
                self.export()
            else:
                self.logger.error(u'EXPORT NÃO REALIZADO! USER : {0}'.format(branch)) 

    def run_process(self):   
        utils = Utils()   
        if utils.check_connection(self.user_data, self.logger):
            if not('base' in self.user_data and self.user_data['base']):
                branch = self.user_data['branch_name']
                self.logger.debug(u"Geogig Pull - user : {0}".format(branch)) 
                self.repository.branches[branch].pull(branch)
            self.export()

if __name__ == '__main__':
    logger = Utils().get_low_logger()
    p_proc = Pos_Process(USERS_REPO, logger)
    p_proc.run_process()
  