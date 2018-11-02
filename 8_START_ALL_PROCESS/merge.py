# -*- coding: utf-8 -*-

import os.path
import sys
from MERGE_CONFIG import MERGE_CONFIG 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import logger, smtp, connection
from process.server_merge import Server_Merge


if __name__ == '__main__':
    n = sys.argv[1]
    branch = sys.argv[2]
    date = sys.argv[3]
    logger, log_path = logger.get_low_logger(date, branch, 'merge')
    #try:
    if not connection.check(MERGE_CONFIG['server'], logger):
        raise Exception(u'Erro conexão com o servidor')
    if not connection.check(MERGE_CONFIG['conflict_db'], logger):
        raise Exception(u'Erro conexão com o banco de conflitos')
    m_proc = Server_Merge(MERGE_CONFIG['server'],
                        MERGE_CONFIG['branches'],
                        MERGE_CONFIG['conflict_db'],
                        MERGE_CONFIG['EPSG'],
                        logger
                    )
    result = m_proc.run_process()
    if result:
        logger.info(u"Merge finalizado sem erros")
    else:
        logger.error(u"Erro no processo de Merge")
    #except Exception as e:
    #    logger.error(e)
    #finally:
    #    pass
        #smtp.send_email_with_attach(u"desenv.1dl@gmail.com", u"desenv1dl", [u"desenv.1dl@gmail.com", "diniz.ime@gmail.com","cesar.soares@gmail.com"], 'Merge', log_path)
