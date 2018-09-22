# -*- coding: utf-8 -*-
import os, sys

BASE_REPO = {
        'database_user_name' : 'postgres',
        'database_user_password' : 'postgres',
        'machine_ip' : '10.2.1.1',
        'machine_port' : '5432',
        'repository_db_name' : 'repositorio',
        'repository_schema_name' : 'repositorios',
        'repository_name' : 'rs_rf1_repo'
}

MERGE_BRANCHES = {
    'main': 'reambulacao',
    'branches': [
                'lunardi2'
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