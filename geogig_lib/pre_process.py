# -*- coding: utf-8 -*-
import socket, time, sys, os, thread, platform
from geogig import Repository
from thread_process import Thread_Process
from datetime import datetime
from users_data import USERS_REPO
from utils import Utils
 
class Pre_Process:
   
    def __init__(self, config, logger=False):
        self.logger = logger
        self.user_data = config
        geogig_path = os.path.join(
            os.getcwd(),
            'geogig_bin',
            'bin',
            'geogig' if  platform.system() == 'Linux' else 'geogig.bat'
        )
        self.pg_dump_path = u"{0}".format(
            u'export PGPASSWORD="{0}"; pg_dump'.format(self.user_data['database_user_password']) 
            if  platform.system() == 'Linux' 
            else 
                u'''set PGPASSWORD='{0}' && "{1}"'''.format(
                    self.user_data['pg_dump_path_windows'],
                    self.user_data['database_user_password']
                )
        )
        self.logger.debug(u"PG_DUMP_PATH : {0} user : {1}".format(self.pg_dump_path, self.user_data['branch_name']))
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
    
    def bkp_production_db(self):
        self.logger.info(
            u"Backup database: {0}, user : {1}".format(
                self.user_data['database_name'], 
                self.user_data['branch_name']
            )
        )
        cmd = u'{pg_dump} -U {name} -h {m_ip} -p {m_port} -d {db_name} -f {bkp_path}.sql'.format(
            name = self.user_data['database_user_name'],
            m_ip = self.user_data['machine_ip'],
            m_port = self.user_data['machine_port'],
            db_name = self.user_data['database_name'],
            bkp_path = os.path.join(
                    self.user_data['bkp_path'],
                    u"{0}-{1}-{2}".format(
                    datetime.today().strftime('%Y%m%d'),
                    self.user_data['branch_name'],
                    self.user_data['database_name']
                )
            ),
            pg_dump=self.pg_dump_path
        )
        self.logger.debug(u"Backup database cmd : {0} - user : {1}".format(cmd, self.user_data['branch_name']))
        os.popen(cmd)
      
    def bkp_repository_db(self):
        self.logger.info(
            u"Backup database: {0}, user : {1}".format(
                self.user_data['repository_db_name'], 
                self.user_data['branch_name']
            )
        )
        cmd = u'{pg_dump} -U {name} -h {m_ip} -p {m_port} -d {db_name} -f {bkp_path}.sql'.format(
            name = self.user_data['database_user_name'],
            m_ip = self.user_data['machine_ip'],
            m_port = self.user_data['machine_port'],
            db_name = self.user_data['repository_db_name'],
            bkp_path = os.path.join(
                    self.user_data['bkp_path'],
                    u"{0}-{1}-{2}".format(
                    datetime.today().strftime('%Y%m%d'),
                    self.user_data['branch_name'],
                    self.user_data['repository_name']
                )
            ),
            pg_dump=self.pg_dump_path
        )
        self.logger.debug(u"Backup repository cmd : {0} - user : {1}".format(cmd, self.user_data['branch_name']))
        os.popen(cmd)

    def import_user(self):
        branch = self.user_data['branch_name']
        for step in range(0):
            self.logger.debug(u"Geogig Import {0} - user : {1}".format(step, branch))
            self.repository.branches[branch].pg_import_schema(   
                self.user_data['machine_ip'],
                self.user_data['machine_port'],
                self.user_data['database_name'],
                self.user_data['database_schema_name'],
                self.user_data['database_user_name'],
                self.user_data['database_user_password']
            
            )
        if (self.repository.branches[branch].status() and u'edgv' in self.repository.branches[branch].status()):
            self.logger.debug(u"Geogig Add, Commit - user : {0}".format(branch))
            self.repository.branches[branch].add()
            self.repository.branches[branch].commit(
                u'commit diario - {0}'.format(branch)
            )
            if not('base' in self.user_data and self.user_data['base']):
                self.logger.debug(u"Geogig Push : {0}".format(branch)) 
                self.repository.branches[branch].push(branch)
        else:
           self.logger.info(u'Nothing to commit on {0}'.format(branch))

    def run_process(self):
        utils = Utils()   
        if utils.check_connection(self.user_data, self.logger):
            self.logger.info(u"STARTING PRE PROCESS {0}".format(self.user_data['branch_name']))
            utils.create_dir_bkps(self.user_data['bkp_path'])
            #self.bkp_production_db()
            #self.bkp_repository_db()
            self.import_user()
           

if __name__ == '__main__':
    logger = Utils().get_low_logger()
    for config in USERS_REPO:
        p_proc = Pre_Process(config, logger)
        p_proc.run_process()
     