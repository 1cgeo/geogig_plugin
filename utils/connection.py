# -*- coding: utf-8 -*-
import socket, time, sys, os
import logging, os, sys
from datetime import datetime
 

def check(user_data, logger=False):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((
            user_data['machine_ip'],
            int(user_data['machine_port'])
        ))
        s.shutdown(2)
        return True
    except:
        msg = u"Not connection user: {0} ip: {1}".format(
            user_data['machine_ip'],
            user_data['machine_port']
        )
        logger.error(msg) if logger else ''
        return False