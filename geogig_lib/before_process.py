# -*- coding: utf-8 -*-
import socket, time, sys, os, thread, platform
from geogig import Repository
from thread_process import Thread_Process
from datetime import datetime

class After_Process:
   
    def __init__(self, config):
        self.process_name = config['process_name']
        self.user_data = config['user']
        self.repository_data = config['repository']
        self.repository = Repository(
            self.repository_data['machine_ip'],
            self.repository_data['machine_port'],
            self.repository_data['database_name'],
            self.repository_data['database_schema_name'],
            self.repository_data['name'],
            self.repository_data['database_user_name'],
            self.repository_data['database_user_password'],
            self.repository_data['geogig_path']
        )
    
    def bkp_production_db(self):      
        cmd = u'export PGPASSWORD="{password}";pg_dump -U {name} -h {m_ip} -p {m_port} -d {db_name} -f {bkp_path}/{bkp_db_name}.sql'.format(
            password = self.user_data['database_user_password'],
            name = self.user_data['database_user_name'],
            m_ip = self.user_data['machine_ip'],
            m_port = self.user_data['machine_port'],
            db_name = self.user_data['database_name'],
            bkp_path = self.user_data['bkp_path'],
            bkp_db_name = self.user_data['bkp_database_name']
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
            bkp_repo_name = self.user_data['bkp_repository_name']
        )
        os.system(cmd)

    def import_total(self):
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
        if (u'edgv' in self.repository.branches[branch].status()):
            self.repository.branches[branch].add()
            self.repository.branches[branch].commit(
                u'commit diario - {0}'.format(branch)
            )
            repositorio.branches[branch].push(branch)
        #else:
        #    print u'nada para commitar em {0}'.format(branch)           
    
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
            #print u"Process '{0}': initializing...".format(self.process_name)
            self.thread1 = Thread_Process(self.bkp_production_db, u"{0} : Backup production database".format(self.process_name))
            self.thread2 = Thread_Process(self.bkp_repository_db, u"{0} : Backup repository database".format(self.process_name))
            self.thread3 = Thread_Process(self.import_total, u"{0} : Geogig : Import, Add, Commit and Push".format(self.process_name))
            self.thread1.start()
            self.thread2.start()
            self.thread3.start()
            #print u"Process '{0}': started".format(self.process_name)

if __name__ == '__main__':
    geogig_path = os.path.join(
        '.',
        os.getcwd(),
        'geogig_bin',
        'bin',
        'geogig' if  platform.system() == 'Linux' else 'geogig.bat'
    )
    repo = { 
        'repository' : {
                'name' : 'repo_origin',
                'database_user_name' : 'postgres',
                'database_user_password' : 'senha2',
                'database_name' : 'repository',
                'database_schema_name' : 'repo',
                'machine_ip' : '127.0.0.1',
                'machine_port' : '5432',
                'geogig_path' : geogig_path
            }
    }
    all_config = [
        #user 1
        {
            'process_name' : 'pre process user1',
            'user' : {
                'database_user_name' : 'postgres',
                'database_user_password' : 'senha2',
                'database_schema_name' : 'edgv',
                'database_name' : 'user1',
                'bkp_path' : os.getcwd(),
                'bkp_database_name' : 'user1-db-20182020',
                'bkp_repository_name' : 'user1-repo-20182020',
                'machine_ip' : '127.0.0.1',
                'machine_port' : '5432',
                'branch_name' : 'master',
                'repository_name' : 'repo_user1',
                'repository_schema_name' : 'user1_repo'
            }
        },
        #user 2
       """  { 
            'process_name' : 'pre process user2',
            'user' : {
                'branch_name' : 'user2',
                'database_user_name' : 'postgres',
                'database_user_password' : '',
                'database_schema_name' : 'edgv',
                'database_name' : 'user2',
                'bkp_path' : os.getcwd(),
                'bkp_database_name' : 'user2-db-20182019',
                'bkp_repository_name' : 'user2-repo-20182019',
                'machine_ip' : '127.0.0.1',
                'machine_port' : '5432',
                'repository_branch_name' : 'master',
                'repository_name' : 'repo',
                'repository_db_schema_name' : 'repo'
            }
           
        } """
    ]
    for config in all_config:
        config.update(repo)
        aft_proc = After_Process(config)
        aft_proc.run_process()
  