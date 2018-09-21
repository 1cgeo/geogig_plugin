ALL_USERS_CONFIG = [
        #user 1
        
        {
            'process_name' : 'pre process BASE',
            'user' : {
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
                'repository_name' : 'repo_origin',
                'base' : True,
            }
        },
        {
            'process_name' : 'pre process user1',
            'user' : {
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
        }
       
    ]