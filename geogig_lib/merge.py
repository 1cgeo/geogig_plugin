# -*- coding: utf-8 -*-
import socket, time, sys, os, thread, platform, psycopg2
from geogig import Repository
from thread_process import Thread_Process
from datetime import datetime
from data_users import BASE_REPO, MERGE_BRANCHES
from log import get_low_logger
 
class Merge:
   
    def __init__(self, base_repo, merge_branches):
        self.logger = get_low_logger()
        self.base_repo = base_repo
        self.main_branch = merge_branches['main']
        self.merge_branches = merge_branches['branches']
        self.conflict_db = merge_branches['conflict_db']
        self.psycopg2_connection = self.connectPsycopg2()
        geogig_path = os.path.join(
            os.getcwd(),
            'geogig_bin',
            'bin',
            'geogig' if  platform.system() == 'Linux' else 'geogig.bat'
        )
        self.repository = Repository(
            self.base_repo['machine_ip'],
            self.base_repo['machine_port'],
            self.base_repo['repository_db_name'],
            self.base_repo['repository_schema_name'],
            self.base_repo['repository_name'],
            self.base_repo['database_user_name'],
            self.base_repo['database_user_password'],
            geogig_path
        )

    def connectPsycopg2(self):
        conn = psycopg2.connect(
            u"""dbname='{0}' user='{1}' host='{2}' port='{3}' password='{4}'""".format(
                self.conflict_db['database_name'], 
                self.conflict_db['database_user_name'], 
                self.conflict_db['machine_ip'], 
                self.conflict_db['machine_port'], 
                self.conflict_db['database_user_password']
            )
        )
        conn.set_session(autocommit=True)
        return conn

    def export_feature(self, layer, data):
        pg_cursor = self.psycopg2_connection.cursor()
        pg_cursor.execute(
            """INSERT INTO %s (%s) VALUES (%s);""",
            (layer, fields, values)
        )


    def merge(self, main, branch):
        conflicts = self.repository.branches[main].merge(branch)
        if conflicts == 'Success':
            return True
        else:
            self.logger.info(u'{0} conflitos encontrados'.format(len(conflicts))) 
            blacklist = ['controle_id', 'ultimo_usuario', 'data_modificacao']
            for conflict in conflicts:
                true_conflict = False
                for key in conflict['ours']:
                    if key not in blacklist and conflict['theirs'][key] != conflict['ours'][key]:
                        true_conflict = True
                choices = ['theirs', 'ours']
                if conflicts['theirs'][conflicts['theirs'].keys()[0]] == 'DELETADO'
                    choices.reverse()

                self.repository.branches[main].merge_features(conflicts['camada'], choice[0])
                if true_conflict:
                    self.export_feature(conflict['camada'], conflict[choice(1)])
            return True

    def check_connection(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((
                self.base_repo['machine_ip'],
                int(self.base_repo['machine_port'])
            ))
            s.shutdown(2)
            return True
        except:
            return False

    def run_process(self):
        if self.check_connection():
            for branch in self.merge_branches:
                self.logger.info(u'INICIANDO MERGE - {0}'.format(branch))
                result = self.merge(self.main_branch, branch)
                if result:
                    self.logger.info(u'FINALIZADO MERGE - {0}'.format(branch))
                else:
                    self.logger.error(u'ERRO NO MERGE - {0}'.format(branch)) 
    
if __name__ == '__main__':
    m_proc = Merge(BASE_REPO, MERGE_BRANCHES)
    m_proc.run_process()
  
  