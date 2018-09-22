# -*- coding: utf-8 -*-
import os, sys

BASE_REPO = {
        'database_user_name' : 'postgres',
        'database_user_password' : 'postgres',
        'database_name' : 'reambulacaodb',
        'machine_ip' : '10.2.1.51',
        'machine_port' : '5432',
        'repository_db_name' : 'reambulacaorepo',
        'repository_schema_name' : 'repositorios',
        'repository_name' : 'rs_rf1_repo'
}

MERGE_BRANCHES = {
    'main': 'reambulacao',
    'branches': [
                'alegranzi'
            ],
    'conflict_db': {
        'database_user_name' : 'postgres',
        'database_user_password' : 'postgres',
        'database_name' : 'conflitos',
        'machine_ip' : '10.2.1.51',
        'machine_port' : '5432'
    },
    'EPSG' : '31982'
}