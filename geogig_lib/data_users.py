# -*- coding: utf-8 -*-
import os, sys

BASE_REPO = {
        'database_user_name' : 'postgres',
        'database_user_password' : 'senha2',
        'database_schema_name' : 'edgv',
        'database_name' : 'rs_rf1',
        'bkp_path' : os.getcwd(),
        'machine_ip' : '127.0.0.1',
        'machine_port' : '5432',
        'branch_name' : 'master',
        'repository_db_name' : 'repository',
        'repository_schema_name' : 'repo',
        'repository_name' : 'repo_origin'
}

MERGE_BRANCHES = {
    'main': 'reambulacao',
    'branches': [
                'alengrazi',
                'lunardi',
                'carvalho',
                'mendonca',
                'nepomuceno',
                'tolfo',
                'henrique',
                'castro'
            ],
    'conflict_db': {
        'database_user_name' : 'postgres',
        'database_user_password' : 'senha2',
        'database_name' : 'rs_rf1',
        'machine_ip' : '127.0.0.1',
        'machine_port' : '5432'
    }
}

USERS_REPO = [
        {
            'database_user_name' : 'postgres',
            'database_user_password' : 'senha2',
            'database_schema_name' : 'edgv',
            'database_name' : 'user1',
            'bkp_path' : os.getcwd(),
            'machine_ip' : '127.0.0.1',
            'machine_port' : '5432',
            'branch_name' : 'master',
            'repository_db_name' : 'user1_repo',
            'repository_schema_name' : 'repo',
            'repository_name' : 'repo_user1'
        }
]

BASE_REPO['base'] = True
USERS_REPO.append(BASE_REPO)