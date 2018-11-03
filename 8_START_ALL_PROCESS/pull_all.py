# -*- coding: utf-8 -*-
import socket, time, sys, os, thread, platform
from ALL_USERS_CONFIG import USERS

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from process.repository import Repository
from datetime import datetime
from utils import logger, smtp, connection

 
class Pull_Export:
   
    def __init__(self, config, logger=False):
        self.logger = logger
        self.export_count = 0
        self.user_data = config
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

    def run_process(self):
        self.repository.branches[self.branch].clean_staging_area()
        self.repository.branches[self.branch].pull(self.branch)
        self.logger.debug(u"Geogig Pull - user : {0}".format(self.branch)) 
        return True
        
if __name__ == '__main__':
    n = sys.argv[1]
    branch = sys.argv[2]
    date = sys.argv[3]
    USER = USERS.ALL_CONFIG[int(n)]
    logger, log_path = logger.get_low_logger(date, branch, 'pull')
    #try:
    if not connection.check(USER, logger):
        raise Exception(u'Erro conexão')
    process = Pull_Export(USER, logger)
    result = process.run_process()
    if result:
        logger.info(u"Pull finalizado sem erros")
    else:
        logger.error(u"Erro no processo de Pull")
    #except Exception as e:
    #    logger.error(e)
    #finally:
    #    pass
        #smtp.send_email_with_attach(u"desenv.1dl@gmail.com", u"PASSWORD", [u"desenv.1dl@gmail.com", "diniz.ime@gmail.com","cesar.soares@gmail.com"], 'Pull_Export', log_path)
