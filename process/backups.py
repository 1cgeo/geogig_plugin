# -*- coding: utf-8 -*-
import socket, time, sys, os, platform
from repository import Repository
from datetime import datetime
from utils import path
 
class Backups:
   
    def __init__(self, config, logger=False):
        self.logger = logger
        self.user_data = config
        geogig_path = path.get_geogig_path()
        path.create_dir(self.user_data['bkp_path'])
        self.pg_dump_path = u"{0}".format(
            u'export PGPASSWORD="{0}"; pg_dump'.format(self.user_data['database_user_password']) 
            if  platform.system() == 'Linux' 
            else 
                u'''"{0}"'''.format(
                    self.user_data['pg_dump_path_windows']
                )
        )
        self.logger.debug(u"PG_DUMP_PATH : {0} user : {1}".format(self.pg_dump_path, self.user_data['branch_name']))
        self.os = os
    
    def bkp_production_db(self):
        self.logger.info(
            u"Backup database: {0}, user : {1}".format(
                self.user_data['database_name'], 
                self.user_data['branch_name']
            )
        )
        backup_path = u"{0}.sql".format(os.path.join(
                self.user_data['bkp_path'],
                u"{0}-{1}-{2}".format(
                    datetime.today().strftime('%Y%m%d'),
                    self.user_data['branch_name'],
                    self.user_data['database_name']
                )
            )
        )
        cmd = u'{pg_dump} -U {name} -h {m_ip} -p {m_port} -d {db_name} -f {bkp_path}'.format(
            name = self.user_data['database_user_name'],
            m_ip = self.user_data['machine_ip'],
            m_port = self.user_data['machine_port'],
            db_name = self.user_data['database_name'],
            bkp_path = backup_path,
            pg_dump=self.pg_dump_path
        )
        self.logger.debug(u"Backup database cmd : {0} - user : {1}".format(cmd, self.user_data['branch_name']))
        self.os.popen(cmd)
        return path.exist(backup_path)
      
    def bkp_repository_db(self):
        self.logger.info(
            u"Backup database: {0}, user : {1}".format(
                self.user_data['repository_db_name'], 
                self.user_data['branch_name']
            )
        )
        backup_path = u"{0}.sql".format(os.path.join(
                self.user_data['bkp_path'],
                u"{0}-{1}-{2}".format(
                    datetime.today().strftime('%Y%m%d'),
                    self.user_data['branch_name'],
                    self.user_data['repository_name']
                )
            )
        )
        cmd = u'{pg_dump} -U {name} -h {m_ip} -p {m_port} -d {db_name} -f {bkp_path}'.format(
            name = self.user_data['database_user_name'],
            m_ip = self.user_data['machine_ip'],
            m_port = self.user_data['machine_port'],
            db_name = self.user_data['repository_db_name'],
            bkp_path = backup_path,
            pg_dump=self.pg_dump_path
        )
        self.logger.debug(u"Backup repository cmd : {0} - user : {1}".format(cmd, self.user_data['branch_name']))
        self.os.popen(cmd)
        return path.exist(backup_path)
 
    def run_process(self):
        self.logger.info(u"Init Backups - user  : {0}".format(self.user_data['branch_name']))
        path.create_dir(self.user_data['bkp_path'])
        result_b1 = self.bkp_production_db()
        result_b2 = self.bkp_repository_db()
        if result_b1 and result_b2:
            return True
        return False