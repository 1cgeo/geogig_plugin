# -*- coding: utf-8 -*-
import os, sys

BASE_REPO = {
        'database_user_name' : 'postgres',
        'database_user_password' : 'postgres',
        'database_schema_name' : 'edgv',
        'database_name' : 'reambulacaodb',
        'bkp_path' : os.getcwd(),
        'machine_ip' : '10.2.1.51',
        'machine_port' : '5432',
        'branch_name' : 'reambulacao',
        'repository_db_name' : 'reambulacaorepo',
        'repository_schema_name' : 'repositorios',
        'repository_name' : 'rs_rf1_repo'
}

USERS_REPO = [
        {
            'database_user_name' : 'postgres',
            'database_user_password' : 'postgres',
            'database_schema_name' : 'edgv', 
            'database_name' : 'alegranzidb',
            'bkp_path' : os.getcwd(),
            'machine_ip' : '10.2.1.51',
            'machine_port' : '5432',
            'branch_name' : 'alegranzi',
            'repository_db_name' : 'alegranzirepo',
            'repository_schema_name' : 'repositorios',
            'repository_name' : 'rs_rf1_repo',
            'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe'
        }
]

BASE_REPO['base'] = True
USERS_REPO.append(BASE_REPO)