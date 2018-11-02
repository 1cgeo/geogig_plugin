# -*- coding: utf-8 -*-
import socket, time, sys, os, thread, platform, subprocess, psycopg2
from process.repository import Repository
from datetime import datetime
from utils import path
 
class Import_Add_Commit_Push:
   
    def __init__(self, config, push=False, logger=False):
        self.logger = logger
        self.do_push = push
        self.user_data = config
        self.branch = self.user_data['branch_name']
        self.geogig_path = path.get_geogig_path()
        self.repository = Repository(
            self.user_data['machine_ip'],
            self.user_data['machine_port'],
            self.user_data['repository_db_name'],
            self.user_data['repository_schema_name'],
            self.user_data['repository_name'],
            self.user_data['database_user_name'],
            self.user_data['database_user_password'],
            self.geogig_path,
            self.logger
        )

    def connectPsycopg2(self):
        conn = psycopg2.connect(
            u"""dbname='{0}' user='{1}' host='{2}' port='{3}' password='{4}'""".format(
                self.user_data['repository_db_name'], 
                self.user_data['database_user_name'], 
                self.user_data['machine_ip'], 
                self.user_data['machine_port'], 
                self.user_data['database_user_password']
            )
        )
        conn.set_session(autocommit=True)
        return conn
        
    def insert_summary_on_db(self):
        summary, commit_uuid = self.repository.branches[self.branch].get_summary()
        pg_cursor = self.connectPsycopg2().cursor()
        date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        for layer_name in summary:
            values = [ 
                "'{}'".format(layer_name), 
                summary[layer_name]['A'], 
                summary[layer_name]['R'], 
                summary[layer_name]['M'], 
                "'{}'".format(commit_uuid),
                "TIMESTAMP '{}'".format(date),
                "'{}'".format(self.branch) 
            ]   
            pg_cursor.execute( u"""INSERT INTO public.commit_summary (layer,  count_add, count_del, count_change, uuid, time, branch) VALUES ({});""".format(
                    u','.join([str(v) for v in values])
                )   
            )   
        pg_cursor.close()
        self.logger.debug(u"Export summary commit - user : {}".format(self.branch)) if self.logger else ''


    def pg_import(self, check_commit=True):
        result = self.repository.branches[self.branch].isEqualHEADs(
            self.user_data['machine_ip'],
            self.user_data['machine_port'],
            self.user_data['database_name'],
            self.user_data['database_user_name'],
            self.user_data['database_user_password']
        )
        result = True if not(check_commit) else result
        if result:
            self.logger.debug(u"Geogig Import - user : {}".format(self.branch)) if self.logger else ''
            self.repository.branches[self.branch].pg_import_schema(   
                self.user_data['machine_ip'],
                self.user_data['machine_port'],
                self.user_data['database_name'],
                self.user_data['database_schema_name'],
                self.user_data['database_user_name'],
                self.user_data['database_user_password']
            )
        else:
            self.logger.error(u"DIFFERENT HEADS") if self.logger else ''
        return result
    
    def push(self):
        if self.do_push: 
            self.repository.branches[self.branch].push(self.branch)
            self.logger.debug(u"Geogig Push : {0}".format(self.branch)) if self.logger else ''
    
    def add_commit(self, layers_list=False):
        self.repository.branches[self.branch].add(layers_list)
        self.repository.branches[self.branch].commit(u'commit manual - {0}'.format(self.branch))
        self.logger.debug(u"Geogig Add, Commit - user : {0}".format(self.branch)) if self.logger else ''
        
    def check_status(self):
        status = self.repository.branches[self.branch].status()
        if ( status and u'edgv' in status):
            return True

    def abort_process(self):
        self.repository.branches[self.branch].clean_staging_area()
        self.repository.reset_commit(position=1)
        
    def run_process(self):
        self.logger.info(u"Init Import, Add, Commit and Push(if needed): {0}".format(self.branch)) if self.logger else ''
        self.repository.branches[self.branch].clean_staging_area()
        if not(self.pg_import()):
           return False
        if self.check_status():
            self.add_commit()
            if not(self.pg_import(check_commit=False)):
                return False
            if self.check_status():
                self.abort_process()
                return False
            self.push()
            self.repository.branches[self.branch].insert_uuid_on_db(   
                self.user_data['machine_ip'],
                self.user_data['machine_port'],
                self.user_data['database_name'],
                self.user_data['database_user_name'],
                self.user_data['database_user_password'],
                u'COMMIT'
            )
            self.insert_summary_on_db()
        else:
            self.logger.info(u'Nothing to commit on {0}'.format(self.branch)) if self.logger else '' 
        self.repository.branches[self.branch].show_resume_commit_by_tag(u'commit')
        return True
     