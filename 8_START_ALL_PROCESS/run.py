import sys, os, platform, json
from multiprocessing import Pool
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ALL_USERS_CONFIG import USERS
from datetime import datetime


#DATE LOG
date = datetime.today().strftime('%Y%m%d_%H-%M-%S')


def validate_step(step_name):
    log_dir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), 'logs')
    validate = []
    for log in os.listdir(log_dir):
        if date in log:
            ok = True
            with open(os.path.join(log_dir, log)) as log_file:
                data = log_file.readlines()
                for l in data:
                    if len(l.split('-')) > 4 and l.split('-')[4].lower().strip() == u'error':
                        ok = False
            validate.append(ok)
    return True if not(False in validate) else False
    
def run_process(command):
    cmd = " ".join(echo+[command])
    print u"START COMMAND : {}".format(cmd)
    os.popen(cmd)

def get_steps(path_command, only_base=False, not_base=False):
    step = []
    if only_base:
        for n, USER in enumerate(USERS.ALL_CONFIG):
            if 'BASE' in USER:
                step.append(u"{} {} {} {}".format(path_command, n, USER['branch_name'], date))
                return step
    elif not_base:
        for n, USER in enumerate(USERS.ALL_CONFIG):
            if not('BASE' in USER):
                step.append(u"{} {} {} {}".format(path_command, n, USER['branch_name'], date))
    else:
        for n, USER in enumerate(USERS.ALL_CONFIG):
            step.append(u"{} {} {} {}".format(path_command, n, USER['branch_name'], date))
    return tuple(step)

if __name__ == '__main__':
    #PATHS COMMANDS
    backup_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), '8_START_ALL_PROCESS', 'backup.py')
    commit_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), '8_START_ALL_PROCESS', 'commit.py')
    merge_paht = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), '8_START_ALL_PROCESS', 'merge.py')
    export_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), '8_START_ALL_PROCESS', 'export.py')
    pull_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), '8_START_ALL_PROCESS', 'pull_all.py')
    backup_exported_db_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), '8_START_ALL_PROCESS', 'backup_exported_db.py')
    restore_all_dbs_users = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), '8_START_ALL_PROCESS', 'retore_dbs.py')
    
    #PYTHON
    echo = [sys.executable]
    #START ALL PROCESSES
    tag_process = ['backup', 'commit', 'merge', 'export', 'pull', 'bkp_exported_db', 'restore_all_dbs_users']
    all_process = [backup_path, commit_path, merge_paht, export_path, pull_path, backup_exported_db_path, restore_all_dbs_users]
    for data in zip(tag_process, all_process):
        tag_process = data[0]
        proc = data[1]
        if tag_process in ['merge', 'export', 'bkp_exported_db']:
            steps = get_steps(proc, only_base=True)
        elif tag_process in ['pull', 'restore_all_dbs_users']:
            steps = get_steps(proc, not_base=True)
        else:
            steps = get_steps(proc)
        pool = Pool(processes=3)
        pool.map(run_process, steps)
        pool.close()
        if validate_step(tag_process):
            print u"###{} sucess!###".format(tag_process).upper()
        else:
            print u"###{} failed!###".format(tag_process).upper()
            break
        


