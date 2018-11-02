# -*- coding: utf-8 -*-
import socket, time, sys, os, thread, platform
from repository import Repository
from datetime import datetime

 
class Pull_Export:
   
    def __init__(self, config, pull, logger=False):
        self.logger = logger
        self.export_count = 0
        self.user_data = config
        self.pull = pull
        self.branch = self.user_data['branch_name']
        geogig_path = self.get_geogig_path()
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
    
    def get_geogig_path(self):
        geogig_path = os.path.join(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
            'geogig_bin',
            'bin',
            'geogig' if  platform.system() == 'Linux' else 'geogig.bat'
        )
        return geogig_path

    def export(self):
        result = True
        for i in range(1, 3):
            self.logger.debug(u"Geogig Export {} - user : {}".format(i, self.branch)) if self.logger else ''
            self.repository.branches[self.branch].pg_export_schema(
                self.user_data['machine_ip'],
                self.user_data['machine_port'],
                self.user_data['database_name'],
                self.user_data['database_schema_name'],
                self.user_data['database_user_name'],
                self.user_data['database_user_password']
            )
            self.logger.debug(u"Geogig Import {} - user : {}".format(i, self.branch)) if self.logger else ''
            self.repository.branches[self.branch].pg_import_schema(   
                    self.user_data['machine_ip'],
                    self.user_data['machine_port'],
                    self.user_data['database_name'],
                    self.user_data['database_schema_name'],
                    self.user_data['database_user_name'],
                    self.user_data['database_user_password']
            )
            count_list = len(self.repository.branches[self.branch].get_all_data_staging_work())
            break if count_list == 0 else ''
        if count_list > 0 :
            self.logger.error(u'EXPORT FAILED! USER : {0}'.format(self.branch))
            self.logger.debug(u"STATUS : {0}".format(self.repository.branches[self.branch].status())) if self.logger else ''
            result = False
        if result:
            self.repository.branches[self.branch].clean_table_on_db(   
                self.user_data['machine_ip'],
                self.user_data['machine_port'],
                self.user_data['database_name'],
                self.user_data['database_user_name'],
                self.user_data['database_user_password']
            )
            self.repository.branches[self.branch].insert_uuid_on_db(   
                self.user_data['machine_ip'],
                self.user_data['machine_port'],
                self.user_data['database_name'],
                self.user_data['database_user_name'],
                self.user_data['database_user_password'],
                u'EXPORT'
            )
        self.repository.branches[self.branch].clean_staging_area()
        return result

    def run_process(self):
        self.repository.branches[self.branch].clean_staging_area()
        if self.pull:
            self.repository.branches[self.branch].pull(self.branch)
            self.logger.debug(u"Geogig Pull - user : {0}".format(self.branch)) 
        return self.export()