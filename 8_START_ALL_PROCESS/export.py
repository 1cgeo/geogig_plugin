# -*- coding: utf-8 -*-

import os.path
import sys
from ALL_USERS_CONFIG import USERS

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import logger, smtp, connection
from process.pull_export import Pull_Export

if __name__ == '__main__':
    n = sys.argv[1]
    branch = sys.argv[2]
    date = sys.argv[3]
    BASE = USERS.ALL_CONFIG[int(n)]
    logger, log_path = logger.get_low_logger(date, branch, 'export')
    try:
        
        if not connection.check(BASE, logger):
            raise Exception(u'Erro conexão')
        process = Pull_Export(BASE, False, logger)
        result = process.run_process()
        if result:
            logger.info(u"Pull e Export finalizado sem erros")
        else:
            logger.error(u"Erro no processo de Pull/Export")
    except Exception as e:
        logger.error(e)
    finally:
        pass
        #smtp.send_email_with_attach(u"desenv.1dl@gmail.com", u"PASSWORD", [u"desenv.1dl@gmail.com", "diniz.ime@gmail.com","cesar.soares@gmail.com"], 'Pull_Export', log_path)
