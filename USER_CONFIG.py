# -*- coding: utf-8 -*-
import os
class UserConfig(object):
        USER_CONFIG = {
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
                'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe'
        }
        def __init__(self):
                pass