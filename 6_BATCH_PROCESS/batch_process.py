# -*- coding: utf-8 -*-

from BATCH_CONFIG import USERS_CONFIG, MERGE_CONFIG 
from utils import logger, smtp, connection
from process.backups import Backups
from process.import_add_commit_push import Import_Add_Commit_Push
from process.serve_merge import Server_Merge
from process.pull_export import Pull_Export

logger, log_path = logger.get_low_logger()
run_time = datetime.datetime.now()

def check_all_connection(users):
    computers_not_connected = []
    for user in users:
        if not connection.check(user, logger):
            computers_not_connected.append(user["machine_ip"])
    if len(computers_not_connected) > 0:
        logger.error(u"Not all computers connected - total : {0}, connected : {1}".format(
                len(computers_not_connected), 
                ",".join(computers_not_connected)
            )
        )
        return False
    return True

def all_backups(server, users, logger):
    bkp = Backups(server, logger)
    result = bkp.run_process()
    if not(result):
        return False, server["machine_ip"]
    for user in users:
        bkp = Backups(user, logger)
        result = bkp.run_process()
        if not(result):
            return False, user["machine_ip"]
    return True, True

def import_add_commit_push(server, users):
    process = Import_Add_Commit_Push(server, False, logger)
    result = process.run_process()
    if not(result):
        return False, server["machine_ip"]
    #smtp.send_email(u"desenv.1dl@gmail.com", u"PASSWORD", [u"desenv.1dl@gmail.com", "diniz.ime@gmail.com","cesar.soares@gmail.com"], run_time, 'Batch_Process_Import', 'Finalizado servidor {0}'.format(server["branch_name"]))
    for user in users:
        process = Import_Add_Commit_Push(user, True, logger)
        result = process.run_process()
        if not(result):
            return False, user["machine_ip"]
        #smtp.send_email(u"desenv.1dl@gmail.com", u"PASSWORD", [u"desenv.1dl@gmail.com", "diniz.ime@gmail.com","cesar.soares@gmail.com"], run_time, 'Batch_Process_Import', 'Finalizado usuário {0}'.format(user["branch_name"]))
    return True, True

def pull_export(server, users):
    process = Pull_Export(server, False, logger)
    result = process.run_process()
    if not(result):
        return False, server["machine_ip"]
    #smtp.send_email(u"desenv.1dl@gmail.com", u"PASSWORD", [u"desenv.1dl@gmail.com", "diniz.ime@gmail.com","cesar.soares@gmail.com"], run_time, 'Batch_Process_Export', 'Finalizado servidor {0}'.format(server["branch_name"]))
    for user in users:
        process = Pull_Export(user, True, logger)
        result = process.run_process()
        if not(result):
            return False, user["machine_ip"]
        #smtp.send_email(u"desenv.1dl@gmail.com", u"PASSWORD", [u"desenv.1dl@gmail.com", "diniz.ime@gmail.com","cesar.soares@gmail.com"], run_time, 'Batch_Process_Export', 'Finalizado usuário {0}'.format(user["branch_name"]))
    return True, True


if __name__ == '__main__':
    try:
        if not check_all_connection(USERS_CONFIG):
            raise ConnectionError()
        logger.info(u"Todas as conexões em funcionamento!")

        bkp, user_error_bkp = all_backups(MERGE_CONFIG['server'], USERS_CONFIG, logger)
        if not bkp:
            logger.error(u"Erro no backup do usuário {0}", user_error_bkp)
            raise BackupError()
        logger.info(u"Backup finalizado com sucesso!")
        #smtp.send_email(u"desenv.1dl@gmail.com", u"PASSWORD", [u"desenv.1dl@gmail.com", "diniz.ime@gmail.com","cesar.soares@gmail.com"], run_time, 'Batch_Process_Backup', 'Todos os backups finalizados')

        imp, imp_error = import_add_commit_push(MERGE_CONFIG['server'], USERS_CONFIG)
        if not imp:
            logger.error(u"Erro no import do usuário {0}", imp_error)
            raise ImportError()

        m_proc = Server_Merge(MERGE_CONFIG['server'],
                            MERGE_CONFIG['branches'],
                            MERGE_CONFIG['conflict_db'],
                            MERGE_CONFIG['EPSG'],
                            logger
                        )
        result = m_proc.run_process()
        if not result:
            logger.error(u"Erro no processo de Merge")
            raise MergeError()
        #smtp.send_email(u"desenv.1dl@gmail.com", u"PASSWORD", [u"desenv.1dl@gmail.com", "diniz.ime@gmail.com","cesar.soares@gmail.com"], run_time, 'Batch_Process_Merge', 'Todos os merges finalizados')

        exp, exp_error = pull_export(MERGE_CONFIG['server'], USERS_CONFIG)
        if not exp:
            logger.error(u"Erro de export do usuário {0}", imp_error)
            raise ExportError()
        #smtp.send_email(u"desenv.1dl@gmail.com", u"PASSWORD", [u"desenv.1dl@gmail.com", "diniz.ime@gmail.com","cesar.soares@gmail.com"], run_time, 'Batch_Process_Export', 'Todos os exports finalizados')


        logger.info(u"Processo finalizado com sucesso!")
    except ConnectionError:
        logger.error(u"Não foi possível estabelecer conexão com os usuários")
    except BackupError:
        logger.error(u"Não foi possível de realizar o backup em todos os usuários")
    finally:
        #smtp.send_email_with_attach(u"desenv.1dl@gmail.com", u"PASSWORD", [u"desenv.1dl@gmail.com", "diniz.ime@gmail.com","cesar.soares@gmail.com"], 'Batch_Process', log_path)