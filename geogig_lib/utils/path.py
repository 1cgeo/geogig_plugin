# -*- coding: utf-8 -*-
import sys, os

def exist(path):
    return os.path.exists(path)

def create_dir(path):
    if not(exist(path)):
        os.mkdir(path)

