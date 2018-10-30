# -*- coding: utf-8 -*-
import logging, os, sys, path, socket, time
from datetime import datetime


def get_low_logger():
    formatter = logging.Formatter(u'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_path_dir = os.path.join(os.getcwd(), 'logs')
    path.create_dir(log_path_dir)
    log_file_name = u'{0}.log'.format(datetime.today().strftime('%Y%m%d_%H-%M-%S'))
    log_path_file = os.path.join(log_path_dir, log_file_name)
    handler = logging.FileHandler(
        log_path_file, 
        mode='w'
    )
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(u'GEOGIG PLUGIN')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger, log_path_file