# -*- coding: utf-8 -*-
import logging, os, sys
from datetime import datetime

def get_low_logger():
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.FileHandler(
        u'{0}/logs/{1}.log'.format(
            os.getcwd(),
            datetime.today().strftime('%Y%m%d_%H-%M-%S')
        ), 
        mode='w'
    )
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(u'GEOGIG PLUGIN')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger

def get_high_logger():
    pass

''' # 'application' code
low_logger =  get_low_logger()
low_logger.debug('debug message')
low_logger.info('info message')
low_logger.warn('warn message')
low_logger.error('error message')
low_logger.critical('critical message') '''