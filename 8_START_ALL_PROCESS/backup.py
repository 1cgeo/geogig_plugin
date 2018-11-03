# -*- coding: utf-8 -*-

import os.path
import sys
from ALL_USERS_CONFIG import USERS

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import logger, smtp, connection
from process.backups import Backups

if __name__ == '__main__':
    n = sys.argv[1]
    branch = sys.argv[2]
    date = sys.argv[3]
    USER = USERS.ALL_CONFIG[int(n)]
    logger, log_path = logger.get_low_logger(date, branch, 'backup')
    try:
        if not connection.check(USER, logger):
            raise Exception(u'Erro conexão')
        bkp = Backups(USER, logger)
        result = bkp.run_process()
        if result:
            logger.info(u"Backup finalizado sem erros")
        else:
            logger.error(u"Erro no processo de Backup")
    except Exception as e:
        print e
        logger.error(u"Não foi possível estabelecer conexão com o usuário")
    finally:
        pass
        #smtp.send_email_with_attach(u"desenv.1dl@gmail.com", u"PASSWORD", [u"desenv.1dl@gmail.com", "diniz.ime@gmail.com","cesar.soares@gmail.com"], 'Backup', log_path)
