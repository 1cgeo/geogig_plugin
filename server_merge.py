# -*- coding: utf-8 -*-
import socket, time, sys, os, thread, platform, psycopg2, json
from datetime import datetime
from repository import Repository
from thread_process import Thread_Process
from datetime import datetime
from utils import logger, path
 
class Server_Merge:
   
    def __init__(self, base_repo, merge_branches, logger=False):
        self.logger = logger
        self.base_repo = base_repo
        self.main_branch = merge_branches['main']
        self.merge_branches = merge_branches['branches']
        self.conflict_db = merge_branches['conflict_db']
        self.EPSG = merge_branches['EPSG']
        self.conflicts_json = { 'clonflicts_data' : []}
        geogig_path = path.get_geogig_path()
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

    def export_feature(self, layer, data):
        self.conflicts_json['clonflicts_data'].append({layer : data})

    def merge(self, main, branch):
        self.repository.branches[branch].clean_staging_area()
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
            self.repository.branches[main].commit(
                u'merge - {0}'.format(branch)
            )
            self.logger.debug(u"Geogig Commit Merge")
            return True

    def export_conflicts_data(self):
        if self.conflicts_json:
            conflicts_dir_path = os.path.join(os.getcwd(), 'conflicts_data')
            path.create_dir(conflicts_dir_path)
            conflicts_path_file = os.path.join(conflicts_dir_path, u'{0}.json'.format(datetime.today().strftime('%Y%m%d_%H-%M-%S')))
            with open(conflicts_path_file, 'w') as outfile:
                json.dumps(self.conflicts_json, outfile)

    def run_process(self):
        count_sucess = 0
        for branch in self.merge_branches:
            self.logger.info(u'INIT MERGE - {0}'.format(branch))
            self.repository.branches[self.main_branch].clean_staging_area()
            result = self.merge(self.main_branch, branch)
            if result:
                count_sucess += 1
                self.logger.info(u'FINISH MERGE - {0}'.format(branch))
                self.repository.del_branch(branch)
            else:
                self.repository.merge_abort()
                self.logger.error(u'ERROR MERGE ABORT - BRANCH : {0}'.format(branch))
                break
        self.export_conflicts_data()
        self.repository.branches[self.main_branch].show_resume_commit_by_tag(u'merge')
        if len(self.merge_branches) == count_sucess:
            [self.repository.add_branch(branch) for branch in self.merge_branches]
            return True
        else:
            self.logger.debug(u"ERROR MERGE!")
            return False
        
if __name__ == '__main__':
    pass
  
  