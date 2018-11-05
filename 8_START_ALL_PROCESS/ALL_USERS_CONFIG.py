# -*- coding: utf-8 -*-
import os
class USERS(object):
        PATH_BACKUP = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), 'bkps')
        BD_COMMIT_SUMMARY = {
            'database_user_name' : 'postgres',
            'database_user_password' : 'postgres',
            'database_name' : 'repositorio_lote3',
            'machine_ip' : '10.2.1.18',
            'machine_port' : '5432'
        }
        ALL_CONFIG = [
            {
                'database_user_name' : 'postgres',
                'database_user_password' : 'postgres',
                'database_schema_name' : 'edgv', 
                'database_name' : 'rs_rf1',
                'bkp_path' : PATH_BACKUP,
                'machine_ip' : '10.2.1.18',
                'machine_port' : '5432',
                'branch_name' : 'reambulacao',
                'repository_db_name' : 'repositorio_lote3',
                'repository_schema_name' : 'repositorios',
                'repository_name' : 'rs_rf1_repo',
                'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe',
                'BASE' : True,
                'commit_summary' : BD_COMMIT_SUMMARY
            },
            {
                'database_user_name' : 'postgres',
                'database_user_password' : 'postgres',
                'database_schema_name' : 'edgv', 
                'database_name' : 'rs_rf1',
                'bkp_path' : PATH_BACKUP,
                'machine_ip' : '10.2.1.61',
                'machine_port' : '5432',
                'branch_name' : 'campos',
                'repository_db_name' : 'repositorio_lote3',
                'repository_schema_name' : 'repositorios',
                'repository_name' : 'rs_rf1_repo',
                'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe',
                'commit_summary' : BD_COMMIT_SUMMARY
            },
            {
                'database_user_name' : 'postgres',
                'database_user_password' : 'postgres',
                'database_schema_name' : 'edgv', 
                'database_name' : 'rs_rf1',
                'bkp_path' : PATH_BACKUP,
                'machine_ip' : '10.2.1.56',
                'machine_port' : '5432',
                'branch_name' : 'henrique',
                'repository_db_name' : 'repositorio_lote3',
                'repository_schema_name' : 'repositorios',
                'repository_name' : 'rs_rf1_repo',
                'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe',
                'commit_summary' : BD_COMMIT_SUMMARY
            },
            {
                'database_user_name' : 'postgres',
                'database_user_password' : 'postgres',
                'database_schema_name' : 'edgv', 
                'database_name' : 'rs_rf1',
                'bkp_path' : PATH_BACKUP,
                'machine_ip' : '10.2.1.54',
                'machine_port' : '5432',
                'branch_name' : 'nepomuceno',
                'repository_db_name' : 'repositorio_lote3',
                'repository_schema_name' : 'repositorios',
                'repository_name' : 'rs_rf1_repo',
                'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe',
                'commit_summary' : BD_COMMIT_SUMMARY
            },
            {
                'database_user_name' : 'postgres',
                'database_user_password' : 'postgres',
                'database_schema_name' : 'edgv', 
                'database_name' : 'rs_rf1',
                'bkp_path' : PATH_BACKUP,
                'machine_ip' : '10.2.1.22',
                'machine_port' : '5432',
                'branch_name' : 'castro',
                'repository_db_name' : 'repositorio_lote3',
                'repository_schema_name' : 'repositorios',
                'repository_name' : 'rs_rf1_repo',
                'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe',
                'commit_summary' : BD_COMMIT_SUMMARY
            },
            {
                'database_user_name' : 'postgres',
                'database_user_password' : 'postgres',
                'database_schema_name' : 'edgv', 
                'database_name' : 'rs_rf1',
                'bkp_path' : PATH_BACKUP,
                'machine_ip' : '10.2.1.57',
                'machine_port' : '5432',
                'branch_name' : 'saraiva',
                'repository_db_name' : 'repositorio_lote3',
                'repository_schema_name' : 'repositorios',
                'repository_name' : 'rs_rf1_repo',
                'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe',
                'commit_summary' : BD_COMMIT_SUMMARY
            },
            {
                'database_user_name' : 'postgres',
                'database_user_password' : 'postgres',
                'database_schema_name' : 'edgv', 
                'database_name' : 'rs_rf1',
                'bkp_path' : PATH_BACKUP,
                'machine_ip' : '10.2.1.59',
                'machine_port' : '5432',
                'branch_name' : 'barbosa',
                'repository_db_name' : 'repositorio_lote3',
                'repository_schema_name' : 'repositorios',
                'repository_name' : 'rs_rf1_repo',
                'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe',
                'commit_summary' : BD_COMMIT_SUMMARY
            }
            
        ]
        def __init__(self):
                pass