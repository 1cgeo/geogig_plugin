# -*- coding: utf-8 -*-

import os.path
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from USER_CONFIG import UserConfig
from utils import logger, smtp, connection
from process.backups import Backups

logger, log_path = logger.get_low_logger()

if __name__ == '__main__':
    try:
        USER = UserConfig.USER_CONFIG
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
        os.system("net rpc service stop gg_backup  -I 127.0.0.1 -U administrador{0}senha".format('%'))
        #smtp.send_email_with_attach(u"desenv.1dl@gmail.com", u"desenv1dl", [u"desenv.1dl@gmail.com", "diniz.ime@gmail.com","cesar.soares@gmail.com"], 'Backup', log_path)
