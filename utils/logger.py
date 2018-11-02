# -*- coding: utf-8 -*-
import logging, os, sys, path, socket, time
from datetime import datetime

def create_dir(path):
    if not(os.path.exists(path)):
        os.mkdir(path)

def get_low_logger(branch='', step=''):
    formatter = logging.Formatter(u'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_path_dir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), 'logs')
    create_dir(log_path_dir)
    branch = '_{}'.format(branch) if branch else ''
    step = '_{}'.format(step) if step else ''
    log_file_name = u'{}{}{}.log'.format(datetime.today().strftime('%Y%m%d_%H-%M-%S', branch, step))
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