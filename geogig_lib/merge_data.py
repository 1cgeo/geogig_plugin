# -*- coding: utf-8 -*-
import os, sys

MERGE_BRANCHES = {
    'main': 'reambulacao',
    'branches': [
                'alegranzi'
            ],
    'conflict_db': {
        'database_user_name' : 'postgres',
        'database_user_password' : 'postgres',
        'database_name' : 'conflitos',
        'machine_ip' : '10.2.1.1',
        'machine_port' : '5432'
    },
    'EPSG' : '31982'
}