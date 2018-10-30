# -*- coding: utf-8 -*-

import os.path
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from USER_CONFIG import UserConfig
from utils import logger, smtp, connection
from process.pull_export import Pull_Export

logger, log_path = logger.get_low_logger()

if __name__ == '__main__':
    try:
        USER = UserConfig.USER_CONFIG
        if not connection.check(USER, logger):
            raise Exception(u'Erro conexão')
        process = Pull_Export(USER, False, logger)
        result = process.run_process()
        if result:
            logger.info(u"Pull e Export finalizado sem erros")
        else:
            logger.error(u"Erro no processo de Pull/Export")
    except Exception as e:
        logger.error(e)
    finally:
        pass
        #smtp.send_email_with_attach(u"desenv.1dl@gmail.com", u"desenv1dl", [u"desenv.1dl@gmail.com", "diniz.ime@gmail.com","cesar.soares@gmail.com"], 'Pull_Export', log_path)