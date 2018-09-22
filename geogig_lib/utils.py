# -*- coding: utf-8 -*-
import socket, time, sys, os
import logging, os, sys
from datetime import datetime

 
class Utils:

    def create_dir_bkps(self, path):
        if not(os.path.exists(path)):
            os.mkdir(path)

    def check_connection(self, user_data, logger=False):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((
                user_data['machine_ip'],
                int(user_data['machine_port'])
            ))
            s.shutdown(2)
            return True
        except:
            msg = "Not connection user: {0} ip: {1}".format(
                user_data['machine_ip'],
                user_data['machine_port']
            )
            self.logger.error(msg) if self.logger else ''
            return False

    def get_low_logger(self):
        formatter = logging.Formatter(u'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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

    def get_high_logger(self):
        pass

if __name__ == '__main__':
    #test logger
    low_logger =  Utils().get_low_logger()
    low_logger.debug('debug message')
    low_logger.info('info message')
    low_logger.warn('warn message')
    low_logger.error('error message')
    low_logger.critical('critical message')
