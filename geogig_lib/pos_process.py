# -*- coding: utf-8 -*-
import socket, time, sys, os, thread, platform
from geogig import Repository
from thread_process import Thread_Process
from datetime import datetime
from data_users import ALL_USERS_CONFIG
 
class Pos_Process:
   
    def __init__(self, config):
        self.export_count = 0
        self.process_name = config['process_name']
        self.user_data = config['user']
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
            geogig_path
        )
    
    def export(self):
        branch = self.user_data['branch_name']
        if not('base' in self.user_data and self.user_data['base']): 
            self.repository.branches[branch].fetch(branch)
        self.repository.branches[branch].pg_export_schema(
            self.user_data['machine_ip'],
            self.user_data['machine_port'],
            self.user_data['database_name'],
            self.user_data['database_schema_name'],
            self.user_data['database_user_name'],
            self.user_data['database_user_password']
        )
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
                self.export()
                self.export_count += 1
            else:
                print u'export branch : {0} ERROR!'.format(branch)

    def check_connection(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((
                self.user_data['machine_ip'],
                int(self.user_data['machine_port'])
            ))
            s.shutdown(2)
            return True
        except:
            return False

    def run_process(self):   
        if self.check_connection():
            self.thread1 = Thread_Process(self.export, u"{0} : Fetch, export, import database".format(self.process_name))
            self.thread1.start()

if __name__ == '__main__':
    for config in ALL_USERS_CONFIG:
        p_proc = Pos_Process(config)
        p_proc.run_process()
  