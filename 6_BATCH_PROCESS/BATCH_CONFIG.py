# -*- coding: utf-8 -*-
USERS_CONFIG = [
        {
                'database_user_name' : 'postgres',
                'database_user_password' : 'postgres',
                'database_schema_name' : 'edgv', 
                'database_name' : 'rs_rf1',
                'bkp_path' : os.path.join(os.getcwd(), 'bkps'),
                'machine_ip' : '10.2.1.53',
                'machine_port' : '5432',
                'branch_name' : 'alegranzi',
                'repository_db_name' : 'repositorio',
                'repository_schema_name' : 'repositorios',
                'repository_name' : 'rs_rf1_repo',
                'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe'
        },
        {
                'database_user_name' : 'postgres',
                'database_user_password' : 'postgres',
                'database_schema_name' : 'edgv', 
                'database_name' : 'rs_rf1',
                'bkp_path' : os.path.join(os.getcwd(), 'bkps'),
                'machine_ip' : '10.2.1.54',
                'machine_port' : '5432',
                'branch_name' : 'nepomuceno',
                'repository_db_name' : 'repositorio',
                'repository_schema_name' : 'repositorios',
                'repository_name' : 'rs_rf1_repo',
                'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe'
        },
        {
                'database_user_name' : 'postgres',
                'database_user_password' : 'postgres',
                'database_schema_name' : 'edgv', 
                'database_name' : 'rs_rf1',
                'bkp_path' : os.path.join(os.getcwd(), 'bkps'),
                'machine_ip' : '10.2.1.61',
                'machine_port' : '5432',
                'branch_name' : 'lunardi',
                'repository_db_name' : 'repositorio',
                'repository_schema_name' : 'repositorios',
                'repository_name' : 'rs_rf1_repo',
                'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe'
        },
        {
                'database_user_name' : 'postgres',
                'database_user_password' : 'postgres',
                'database_schema_name' : 'edgv', 
                'database_name' : 'rs_rf1',
                'bkp_path' : os.path.join(os.getcwd(), 'bkps'),
                'machine_ip' : '10.2.1.60',
                'machine_port' : '5432',
                'branch_name' : 'mendonca',
                'repository_db_name' : 'repositorio',
                'repository_schema_name' : 'repositorios',
                'repository_name' : 'rs_rf1_repo',
                'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe'
        },
        {
                'database_user_name' : 'postgres',
                'database_user_password' : 'postgres',
                'database_schema_name' : 'edgv', 
                'database_name' : 'rs_rf1',
                'bkp_path' : os.path.join(os.getcwd(), 'bkps'),
                'machine_ip' : '10.2.1.57',
                'machine_port' : '5432',
                'branch_name' : 'carvalho',
                'repository_db_name' : 'repositorio',
                'repository_schema_name' : 'repositorios',
                'repository_name' : 'rs_rf1_repo',
                'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe'
        },
        {
                'database_user_name' : 'postgres',
                'database_user_password' : 'postgres',
                'database_schema_name' : 'edgv', 
                'database_name' : 'rs_rf1',
                'bkp_path' : os.path.join(os.getcwd(), 'bkps'),
                'machine_ip' : '10.2.1.55',
                'machine_port' : '5432',
                'branch_name' : 'tolfo',
                'repository_db_name' : 'repositorio',
                'repository_schema_name' : 'repositorios',
                'repository_name' : 'rs_rf1_repo',
                'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe'
        },
        {
                'database_user_name' : 'postgres',
                'database_user_password' : 'postgres',
                'database_schema_name' : 'edgv', 
                'database_name' : 'rs_rf1',
                'bkp_path' : os.path.join(os.getcwd(), 'bkps'),
                'machine_ip' : '10.2.1.58',
                'machine_port' : '5432',
                'branch_name' : 'castro',
                'repository_db_name' : 'repositorio',
                'repository_schema_name' : 'repositorios',
                'repository_name' : 'rs_rf1_repo',
                'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe'
        },
        {
                'database_user_name' : 'postgres',
                'database_user_password' : 'postgres',
                'database_schema_name' : 'edgv', 
                'database_name' : 'rs_rf1',
                'bkp_path' : os.path.join(os.getcwd(), 'bkps'),
                'machine_ip' : '10.2.1.56',
                'machine_port' : '5432',
                'branch_name' : 'henrique',
                'repository_db_name' : 'repositorio',
                'repository_schema_name' : 'repositorios',
                'repository_name' : 'rs_rf1_repo',
                'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe'
        }
]

MERGE_CONFIG = {
    'server' = {
            'database_user_name' : 'postgres',
            'database_user_password' : 'postgres',
            'database_schema_name' : 'edgv', 
            'database_name' : 'rs_rf1',
            'bkp_path' : os.path.join(os.getcwd(), 'bkps'),
            'machine_ip' : '10.2.1.1',
            'machine_port' : '5432',
            'branch_name' : 'reambulacao',
            'repository_db_name' : 'repositorio',
            'repository_schema_name' : 'repositorios',
            'repository_name' : 'rs_rf1_repo',
            'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe',
            'base' : True
    },
    'branches': [
                'lunardi',
                'tolfo',
                'nepomuceno',
                'carvalho',
                'mendonca',
                'henrique',
                'castro',
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

