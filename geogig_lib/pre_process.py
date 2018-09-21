# -*- coding: utf-8 -*-
import socket, time, sys, os, thread, platform
from geogig import Repository
from thread_process import Thread_Process
from datetime import datetime
from data_users import USERS_REPO
from log import get_low_logger
 
class Pre_Process:
   
    def __init__(self, config):
        self.logger = get_low_logger()
        self.user_data = config
        self.process_name = u"PRE PROCESS - {0}".format(self.user_data['branch_name'])
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
    
    def bkp_production_db(self):      
        cmd = u'export PGPASSWORD="{password}";pg_dump -U {name} -h {m_ip} -p {m_port} -d {db_name} -f {bkp_path}/{bkp_db_name}.sql'.format(
            password = self.user_data['database_user_password'],
            name = self.user_data['database_user_name'],
            m_ip = self.user_data['machine_ip'],
            m_port = self.user_data['machine_port'],
            db_name = self.user_data['database_name'],
            bkp_path = self.user_data['bkp_path'],
            bkp_db_name = u"{0}-{1}-{2}".format(
                datetime.today().strftime('%Y%m%d'),
                self.user_data['branch_name'],
                self.user_data['database_name']
            )
        )
        os.system(cmd)
      
    def bkp_repository_db(self):
        cmd = u'export PGPASSWORD="{password}";pg_dump -U {name} -h {m_ip} -p {m_port} -d {db_name} -f {bkp_path}/{bkp_repo_name}.sql'.format(
            password = self.user_data['database_user_password'],
            name = self.user_data['database_user_name'],
            m_ip = self.user_data['machine_ip'],
            m_port = self.user_data['machine_port'],
            db_name = self.user_data['database_name'],
            bkp_path = self.user_data['bkp_path'],
            bkp_repo_name = u"{0}-{1}-{2}".format(
                datetime.today().strftime('%Y%m%d'),
                self.user_data['branch_name'],
                self.user_data['repository_name']
            )
        )
        os.system(cmd)

    def import_user(self):
        branch = self.user_data['branch_name']
        for x in range(2):
            self.repository.branches[branch].pg_import_schema(   
                self.user_data['machine_ip'],
                self.user_data['machine_port'],
                self.user_data['database_name'],
                self.user_data['database_schema_name'],
                self.user_data['database_user_name'],
                self.user_data['database_user_password']
            
            )
        if (self.repository.branches[branch].status() and u'edgv' in self.repository.branches[branch].status()):
            self.repository.branches[branch].add()
            self.repository.branches[branch].commit(
                u'commit diario - {0}'.format(branch)
            )
            if not('base' in self.user_data and self.user_data['base']): 
                repositorio.branches[branch].push(branch)
        else:
           self.logger.info(u'nada para commitar em {0}'.format(branch))
            
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
        
    def create_dir_bkps(self):
        if not(os.path.exists(self.path)):
            os.mkdir(self.path)

    def run_process(self):   
        if self.check_connection():
            self.thread1 = Thread_Process(self.bkp_production_db, u"{0} : Backup production database".format(self.process_name))
            self.thread2 = Thread_Process(self.bkp_repository_db, u"{0} : Backup repository database".format(self.process_name))
            self.thread3 = Thread_Process(self.import_user, u"{0} : Geogig : Import, Add, Commit and Push".format(self.process_name))
            self.thread1.start()
            self.thread2.start()
            self.thread3.start()

if __name__ == '__main__':
    for config in USERS_REPO:
        p_proc = Pre_Process(config)
        p_proc.run_process()
  