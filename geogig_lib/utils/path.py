# -*- coding: utf-8 -*-
import sys, os

def exist(path):
    return os.path.exists(path)

def create_dir(path):
    if not(exist(path)):
        os.mkdir(path)

def get_geogig_path():
    geogig_path = os.path.join(
        os.getcwd(),
        'geogig_bin',
        'bin',
        'geogig' if  platform.system() == 'Linux' else 'geogig.bat'
    )
    return geogig_path

