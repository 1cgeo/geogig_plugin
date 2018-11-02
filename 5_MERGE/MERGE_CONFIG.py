# -*- coding: utf-8 -*-

import os

MERGE_CONFIG = {
    'server': {
            'database_user_name' : 'postgres',
            'database_user_password' : 'postgres',
            'database_schema_name' : 'edgv', 
            'database_name' : 'rs_rf1',
            'bkp_path' : os.path.join(os.getcwd(), 'bkps'),
            'machine_ip' : '10.2.1.18',
            'machine_port' : '5432',
            'branch_name' : 'reambulacao',
            'repository_db_name' : 'repositorio_lote3',
            'repository_schema_name' : 'repositorios',
            'repository_name' : 'rs_rf1_repo',
            'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe',
            'base' : True
    },
    'branches': [
                'castro',
                'nepomuceno',
                'campos',
                'henrique',
                'barbosa',
                'saraiva'
            ],
    'conflict_db': {
        'database_user_name' : 'postgres',
        'database_user_password' : 'postgres',
        'database_name' : 'conflitos',
        'machine_ip' : '10.2.1.18',
        'machine_port' : '5432'
    },
    'EPSG' : '31982'
}

