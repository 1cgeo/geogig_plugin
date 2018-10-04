# -*- coding: utf-8 -*-
import socket, time, sys, os
import logging, os, sys
from datetime import datetime


def get_low_logger():
    formatter = logging.Formatter(u'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_path = u'{0}/logs/{1}.log'.format(
        os.getcwd(),
        datetime.today().strftime('%Y%m%d_%H-%M-%S')
    )
    handler = logging.FileHandler(
        log_path, 
        mode='w'
    )
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(u'GEOGIG PLUGIN')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger, log_path