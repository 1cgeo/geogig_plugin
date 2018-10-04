# -*- coding: utf-8 -*-
import os, sys

MERGE_BRANCHES = {
    'main': 'reambulacao',
    'branches': [
                'tolfo',
                'alegranzi'
            ],
    'conflict_db': {
        'database_user_name' : 'postgres',
        'database_user_password' : 'senha2',
        'database_name' : 'conflitos',
        'machine_ip' : '127.0.0.1',
        'machine_port' : '5432'
    },
    'EPSG' : '31982'
}