# -*- coding: utf-8 -*-

from users_data import USERS_CONFIG, SERVER
from merge_data import MERGE_BRANCHES
from utils import logger, smtp, connection
from backups import Backups
from import_add_commit_push import Import_Add_Commit_Push
from server_merge import Server_Merge
from pull_export import Pull_Export

logger, log_path = logger.get_low_logger()

def check_all_connection():
    count_computers = len(USERS_CONFIG)
    count_computers_connected = 0
    for USER in USERS_CONFIG:
        if connection.check(USER, logger):
            count_computers_connected += 1
    if not(count_computers == count_computers_connected):
        logger.erro(u"Not all computers connected - total : {0}, connected : {0}".format(
                count_computers, 
                count_computers_connected
            )
        )
        return False
    return True

def all_backups():
    for USER in USERS_CONFIG:
        bkp = Backups(USER, logger)
        result = bkp.run_process()
        if not(result):
            return False
    return True

def import_add_commit_push():
    for USER in USERS_CONFIG:
        process = Import_Add_Commit_Push(USER, logger)
        result = process.run_process()
        if not(result):
            return False
    return True

def server_merge_dell_add_branch():
    m_proc = Server_Merge(SERVER, MERGE_BRANCHES, logger)
    return m_proc.run_process()

def pull_export():
    for USER in USERS_CONFIG:
        p_proc = Pull_Export(USER, logger)
        if not(p_proc.run_process()):
            return False
    return True

def start():
    if  not(check_all_connection()):
        logger.error(u"Not all computers connected")
        return
    if  not(all_backups()):
        logger.error(u"Erro in backups")
        return
    if not(import_add_commit_push()):
        logger.error(u"Erro Import Add Commit Push")
        return
    if not(server_merge_dell_add_branch()):
        logger.error(u"Erro Merge")
        return 
    if not(pull_export()):
        logger.erro(u"Erro Pull Export")
        return 
    logger.debug(u"All successful processes!")

if __name__ == '__main__':
    try:
        msg = start()
    except:
        pass
    smtp.send_email(u"email_origin", u"password", [u"email_dest"], log_path)
