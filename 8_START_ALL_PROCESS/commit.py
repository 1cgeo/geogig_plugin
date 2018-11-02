# -*- coding: utf-8 -*-

import os.path
import sys
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ALL_USERS_CONFIG import USERS
from utils import logger, smtp, connection
from process.import_add_commit_push import Import_Add_Commit_Push

logger, log_path = logger.get_low_logger()

if __name__ == '__main__':
    try:
        n = sys.argv[1]
        USER = USERS.ALL_CONFIG[int(n)]
        do_push = False if 'BASE' in USER and USER['BASE'] else True
        if not connection.check(USER, logger):
            raise Exception(u'Erro conexão')
        process = Import_Add_Commit_Push(USER, do_push, logger)
        result = process.run_process()
        if result:
            logger.info(u"Commit/Push finalizado sem erros")
        else:
            logger.error(u"Erro no processo de Import/Add/Commit/Push")
    except Exception as e:
        logger.error(e)
    finally:
        os.system('sc stop commit_push')
        #smtp.send_email_with_attach(u"desenv.1dl@gmail.com", u"desenv1dl", [u"desenv.1dl@gmail.com", "diniz.ime@gmail.com","cesar.soares@gmail.com"], 'Commit_Push', log_path)
