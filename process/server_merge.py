# -*- coding: utf-8 -*-
import socket, time, sys, os, thread, platform, psycopg2, json
from datetime import datetime
from repository import Repository
from datetime import datetime
from utils import logger, path
 
class Server_Merge:
   
    def __init__(self, base_repo, merge_branches, conflict_db, epsg, logger=False):
        self.logger = logger
        self.base_repo = base_repo
        self.main_branch = base_repo['branch_name']
        self.merge_branches = merge_branches
        self.conflict_db = conflict_db
        self.EPSG = epsg
        self.pg_cursor = self.connectPsycopg2()
        geogig_path = self.get_geogig_path()
        self.repository = Repository(
            self.base_repo['machine_ip'],
            self.base_repo['machine_port'],
            self.base_repo['repository_db_name'],
            self.base_repo['repository_schema_name'],
            self.base_repo['repository_name'],
            self.base_repo['database_user_name'],
            self.base_repo['database_user_password'],
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
        return conn.cursor()

    def export_feature(self, layer, data):
        del data['data_modificacao']
        del data['id']
        data['geom'] = u"SRID={1};{0}".format(data['geom'], self.EPSG)
        self.logger.debug(u"layer : {0} , data : {1}".format(layer, data))
        values = []
        for x in data.values():
            values += ["'{0}'".format(x.decode("utf-8"))] if x else ['NULL']
        self.pg_cursor.execute(
            u"""INSERT INTO {0} ({1}) VALUES ({2});""".format(
                u"{0}.{1}".format(layer.split('/')[0], layer.split('/')[1]), 
                u",".join(data.keys()), 
                u",".join(values)
            )
        )

    def merge(self, main, branch):
        self.repository.branches[branch].clean_staging_area()
        self.repository.branches[main].clean_staging_area()
        conflicts = self.repository.branches[main].merge(branch)
        if conflicts == 'Success':
            return True
        else:
            self.logger.info(u'{0} conflitos encontrados'.format(len(conflicts))) 
            blacklist = [u'controle_id', u'ultimo_usuario', u'data_modificacao']
            for conflict in conflicts:
                true_conflict = False
                for key in conflict[u'ours']:
                    if not(key in blacklist) and conflict[u'theirs'][key] != conflict[u'ours'][key]:
                        true_conflict = True
                choices = [u'theirs', u'ours']
                if conflict['ours'].values()[0] == u'DELETADO':
                    choices = [u'ours', u'theirs']
                if u"tipo" in conflict[u'theirs'].keys() and conflict[u'theirs'][u'tipo'] == u'999':
                    choices = [u'ours', u'theirs']
                self.repository.branches[main].merge_features({
                    conflict[u'camada'] : choices[0]
                })
                if true_conflict:
                    self.export_feature(conflict['camada'], conflict[choices[1]])
                    self.logger.debug(u"Geogig export conflicts on database")
            self.repository.branches[main].commit(
                u'merge - {0}'.format(branch)
            )
            self.logger.debug(u"Geogig Commit Merge")
            return True
                
    def run_process(self):
        count_sucess = 0
        for branch in self.merge_branches:
            self.logger.info(u'INIT MERGE - {0}'.format(branch))
            result = self.merge(self.main_branch, branch)
            if result:
                count_sucess += 1
                self.logger.info(u'FINISH MERGE - {0}'.format(branch))
                self.repository.del_branch(branch)
            else:
                self.repository.merge_abort()
                self.logger.error(u'ERROR MERGE ABORT - BRANCH : {0}'.format(branch))
                break
        self.pg_cursor.close()
        self.repository.branches[self.main_branch].show_resume_commit_by_tag(u'merge')
        if len(self.merge_branches) == count_sucess:
            [self.repository.add_branch(branch) for branch in self.merge_branches]
            return True
        else:
            self.logger.debug(u"ERROR MERGE!")
            return False