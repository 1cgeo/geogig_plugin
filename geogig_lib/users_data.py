# -*- coding: utf-8 -*-
import os, sys


USERS_REPO = {
            'database_user_name' : 'postgres',
            'database_user_password' : 'postgres',
            'database_schema_name' : 'edgv', 
            'database_name' : 'rs_rf1',
            'bkp_path' : os.path.join(os.getcwd(), 'bkps'),
            'machine_ip' : '127.0.0.1',
            'machine_port' : '5432',
            'branch_name' : 'lunardi',
            'repository_db_name' : 'repositorio',
            'repository_schema_name' : 'repositorios',
            'repository_name' : 'rs_rf1_repo',
            'pg_dump_path_windows' : 'c:\\Program Files\\PostgreSQL\\10\\bin\\pg_dump.exe'
}


