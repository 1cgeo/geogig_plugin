# -*- coding: utf-8 -*-
import os, sys

BASE_REPO = {
        'database_user_name' : 'postgres',
        'database_user_password' : 'senha',
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
        'database_user_password' : 'senha',
        'database_name' : 'conflitos',
        'machine_ip' : '10.2.1.51',
        'machine_port' : '5432'
    }
}

''' {
            'database_user_name' : 'postgres',
            'database_user_password' : 'senha',
            'database_schema_name' : 'edgv',
            'database_name' : 'henriquedb',
            'bkp_path' : os.getcwd(),
            'machine_ip' : '10.2.1.51',
            'machine_port' : '5432',
            'branch_name' : 'henrique',
            'repository_db_name' : 'henriquerepo',
            'repository_schema_name' : 'repositorios',
            'repository_name' : 'rs_rf1_repo'
        },
 '''
 ''' {
            'database_user_name' : 'postgres',
            'database_user_password' : 'senha',
            'database_schema_name' : 'edgv',
            'database_name' : 'castrodb',
            'bkp_path' : os.getcwd(),
            'machine_ip' : '10.2.1.51',
            'machine_port' : '5432',
            'branch_name' : 'castro',
            'repository_db_name' : 'castrorepo',
            'repository_schema_name' : 'repositorios',
            'repository_name' : 'rs_rf1_repo'
        }, '''
USERS_REPO = [
        {
            'database_user_name' : 'postgres',
            'database_user_password' : 'senha',
            'database_schema_name' : 'edgv',
            'database_name' : 'alegranzidb',
            'bkp_path' : os.getcwd(),
            'machine_ip' : '10.2.1.51',
            'machine_port' : '5432',
            'branch_name' : 'alegranzi',
            'repository_db_name' : 'alegranzirepo',
            'repository_schema_name' : 'repositorios',
            'repository_name' : 'rs_rf1_repo'
        },
         {
            'database_user_name' : 'postgres',
            'database_user_password' : 'senha',
            'database_schema_name' : 'edgv',
            'database_name' : 'tolfodb',
            'bkp_path' : os.getcwd(),
            'machine_ip' : '10.2.1.51',
            'machine_port' : '5432',
            'branch_name' : 'tolfo',
            'repository_db_name' : 'tolforepo',
            'repository_schema_name' : 'repositorios',
            'repository_name' : 'rs_rf1_repo'
        },
         
         {
            'database_user_name' : 'postgres',
            'database_user_password' : 'senha',
            'database_schema_name' : 'edgv',
            'database_name' : 'lunardidb',
            'bkp_path' : os.getcwd(),
            'machine_ip' : '10.2.1.51',
            'machine_port' : '5432',
            'branch_name' : 'lunardi',
            'repository_db_name' : 'lunardirepo',
            'repository_schema_name' : 'repositorios',
            'repository_name' : 'rs_rf1_repo'
        },
         {
            'database_user_name' : 'postgres',
            'database_user_password' : 'senha',
            'database_schema_name' : 'edgv',
            'database_name' : 'carvalhodb',
            'bkp_path' : os.getcwd(),
            'machine_ip' : '10.2.1.51',
            'machine_port' : '5432',
            'branch_name' : 'carvalho',
            'repository_db_name' : 'carvalhorepo',
            'repository_schema_name' : 'repositorios',
            'repository_name' : 'rs_rf1_repo'
        },
         {
            'database_user_name' : 'postgres',
            'database_user_password' : 'senha',
            'database_schema_name' : 'edgv',
            'database_name' : 'nepomucenodb',
            'bkp_path' : os.getcwd(),
            'machine_ip' : '10.2.1.51',
            'machine_port' : '5432',
            'branch_name' : 'nepomuceno',
            'repository_db_name' : 'nepomucenorepo',
            'repository_schema_name' : 'repositorios',
            'repository_name' : 'rs_rf1_repo'
        },
         
         {
            'database_user_name' : 'postgres',
            'database_user_password' : 'senha',
            'database_schema_name' : 'edgv',
            'database_name' : 'mendoncadb',
            'bkp_path' : os.getcwd(),
            'machine_ip' : '10.2.1.51',
            'machine_port' : '5432',
            'branch_name' : 'mendonca',
            'repository_db_name' : 'mendoncarepo',
            'repository_schema_name' : 'repositorios',
            'repository_name' : 'rs_rf1_repo'
        },
        
]

BASE_REPO['base'] = True
USERS_REPO.append(BASE_REPO)