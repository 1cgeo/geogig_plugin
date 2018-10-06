# -*- coding: utf-8 -*-
import os, sys

SERVER = {
        'database_user_name' : 'postgres',
        'database_user_password' : 'senha2',
        'database_schema_name' : 'edgv', 
        'database_name' : 'base',
        'bkp_path' : os.path.join(os.getcwd(), 'bkps'),
        'machine_ip' : '127.0.0.1',
        'machine_port' : '5432',
        'branch_name' : 'reambulacao',
        'repository_db_name' : 'base_repo',
        'repository_schema_name' : 'repositorios',
        'repository_name' : 'rs_rf1_repo',
        'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe',
        'base' : True
}

USERS_CONFIG = [
    SERVER,
    {
        'database_user_name' : 'postgres',
        'database_user_password' : 'senha2',
        'database_schema_name' : 'edgv', 
        'database_name' : 'alegranzi',
        'bkp_path' : os.path.join(os.getcwd(), 'bkps'),
        'machine_ip' : '127.0.0.1',
        'machine_port' : '5432',
            'branch_name' : 'alegranzi',
            'repository_db_name' : 'alegranzi_repo',
            'repository_schema_name' : 'repositorios',
            'repository_name' : 'rs_rf1_repo',
            'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe'
    },
    {
        'database_user_name' : 'postgres',
        'database_user_password' : 'senha2',
        'database_schema_name' : 'edgv', 
        'database_name' : 'lunardi',
        'bkp_path' : os.path.join(os.getcwd(), 'bkps'),
        'machine_ip' : '127.0.0.1',
        'machine_port' : '5432',
            'branch_name' : 'lunardi',
            'repository_db_name' : 'lunardi_repo',
            'repository_schema_name' : 'repositorios',
            'repository_name' : 'rs_rf1_repo',
            'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe'
    },
    {
        'database_user_name' : 'postgres',
        'database_user_password' : 'senha2',
        'database_schema_name' : 'edgv', 
        'database_name' : 'nepomuceno',
        'bkp_path' : os.path.join(os.getcwd(), 'bkps'),
        'machine_ip' : '127.0.0.1',
        'machine_port' : '5432',
            'branch_name' : 'nepomuceno',
            'repository_db_name' : 'nepomuceno_repo',
            'repository_schema_name' : 'repositorios',
            'repository_name' : 'rs_rf1_repo',
            'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe'
    }]
'''     SERVER,
        {
        'database_user_name' : 'postgres',
        'database_user_password' : 'senha2',
        'database_schema_name' : 'edgv', 
        'database_name' : 'alegranzi',
        'bkp_path' : os.path.join(os.getcwd(), 'bkps'),
        'machine_ip' : '127.0.0.1',
        'machine_port' : '5432',
            'branch_name' : 'alegranzi',
            'repository_db_name' : 'alegranzi_repo',
            'repository_schema_name' : 'repositorios',
            'repository_name' : 'rs_rf1_repo',
            'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe'
    },
    {
        'database_user_name' : 'postgres',
        'database_user_password' : 'senha2',
        'database_schema_name' : 'edgv', 
        'database_name' : 'lunardi',
        'bkp_path' : os.path.join(os.getcwd(), 'bkps'),
        'machine_ip' : '127.0.0.1',
        'machine_port' : '5432',
            'branch_name' : 'lunardi',
            'repository_db_name' : 'lunardi_repo',
            'repository_schema_name' : 'repositorios',
            'repository_name' : 'rs_rf1_repo',
            'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe'
    },
    {
        'database_user_name' : 'postgres',
        'database_user_password' : 'senha2',
        'database_schema_name' : 'edgv', 
        'database_name' : 'nepomuceno',
        'bkp_path' : os.path.join(os.getcwd(), 'bkps'),
        'machine_ip' : '127.0.0.1',
        'machine_port' : '5432',
            'branch_name' : 'nepomuceno',
            'repository_db_name' : 'nepomuceno_repo',
            'repository_schema_name' : 'repositorios',
            'repository_name' : 'rs_rf1_repo',
            'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe'
    }
    
    
]

 '''
