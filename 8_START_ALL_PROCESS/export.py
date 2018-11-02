# -*- coding: utf-8 -*-

import os.path
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from USER_CONFIG import UserConfig
from utils import logger, smtp, connection
from process.pull_export import Pull_Export

logger, log_path = logger.get_low_logger()

if __name__ == '__main__':
    n = sys.argv[1]
    branch = sys.argv[2]
    date = sys.argv[3]
    BASE = False
    for USER in USERS.ALL_CONFIG
        if 'BASE' in USER and USER['BASE']:
            BASE = USER
    logger, log_path = logger.get_low_logger(date, branch, 'commit')
    try:
        if BASE:
            if not connection.check(BASE, logger):
                raise Exception(u'Erro conexão')
            process = Pull_Export(BASE, False, logger)
            result = process.run_process()
            if result:
                logger.info(u"Pull e Export finalizado sem erros")
        if not(result) or not(BASE):
            logger.error(u"Erro no processo de Pull/Export")
    except Exception as e:
        logger.error(e)
    finally:
        pass
        #smtp.send_email_with_attach(u"desenv.1dl@gmail.com", u"desenv1dl", [u"desenv.1dl@gmail.com", "diniz.ime@gmail.com","cesar.soares@gmail.com"], 'Pull_Export', log_path)
