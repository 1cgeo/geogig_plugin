# -*- coding: utf-8 -*-
import os
class USERS(object):
        ALL_CONFIG = [
            {
                'database_user_name' : 'postgres',
                'database_user_password' : 'postgres',
                'database_schema_name' : 'edgv', 
                'database_name' : 'base',
                'bkp_path' : os.path.join(os.getcwd(), '/media/backup_srv'),
                'machine_ip' : 'localhost',
                'machine_port' : '5432',
                'branch_name' : 'reambulacao',
                'repository_db_name' : 'base_repo',
                'repository_schema_name' : 'repositorios',
                'repository_name' : 'rs_rf1_repo',
                'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe',
                'BASE' : True
            },
            {
                'database_user_name' : 'postgres',
                'database_user_password' : 'postgres',
                'database_schema_name' : 'edgv', 
                'database_name' : 'campos',
                'bkp_path' : os.path.join(os.getcwd(), '/media/backup_srv'),
                'machine_ip' : 'localhost',
                'machine_port' : '5432',
                'branch_name' : 'campos',
                'repository_db_name' : 'campos_repo',
                'repository_schema_name' : 'repositorios',
                'repository_name' : 'rs_rf1_repo',
                'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe',
                
            },
            {
                'database_user_name' : 'postgres',
                'database_user_password' : 'postgres',
                'database_schema_name' : 'edgv', 
                'database_name' : 'castro',
                'bkp_path' : os.path.join(os.getcwd(), '/media/backup_srv'),
                'machine_ip' : 'localhost',
                'machine_port' : '5432',
                'branch_name' : 'castro',
                'repository_db_name' : 'castro_repo',
                'repository_schema_name' : 'repositorios',
                'repository_name' : 'rs_rf1_repo',
                'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe',
                
            },
            {
                'database_user_name' : 'postgres',
                'database_user_password' : 'postgres',
                'database_schema_name' : 'edgv', 
                'database_name' : 'henrique',
                'bkp_path' : os.path.join(os.getcwd(), '/media/backup_srv'),
                'machine_ip' : 'localhost',
                'machine_port' : '5432',
                'branch_name' : 'henrique',
                'repository_db_name' : 'henrique_repo',
                'repository_schema_name' : 'repositorios',
                'repository_name' : 'rs_rf1_repo',
                'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe',
                
            },
            {
                'database_user_name' : 'postgres',
                'database_user_password' : 'postgres',
                'database_schema_name' : 'edgv', 
                'database_name' : 'nepomuceno',
                'bkp_path' : os.path.join(os.getcwd(), '/media/backup_srv'),
                'machine_ip' : 'localhost',
                'machine_port' : '5432',
                'branch_name' : 'nepomuceno',
                'repository_db_name' : 'nepomuceno_repo',
                'repository_schema_name' : 'repositorios',
                'repository_name' : 'rs_rf1_repo',
                'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe',
                
            }
            
        ]
        def __init__(self):
                pass