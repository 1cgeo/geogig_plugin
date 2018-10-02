# -*- coding: utf-8 -*-
import sys, os

def exist(path):
    return os.path.exists(path)

def create_dir(path):
    if not(exist_path(path)):
        os.mkdir(path)

