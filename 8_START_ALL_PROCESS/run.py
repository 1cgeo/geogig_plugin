import sys, os, platform, json
from multiprocessing import Pool
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ALL_USERS_CONFIG import USERS
from datetime import datetime


if __name__ == '__main__':
    backup_file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), '8_START_ALL_PROCESS', 'backup.py')
    commit_file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), '8_START_ALL_PROCESS', 'commit.py')
    merge_file_paht = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), '8_START_ALL_PROCESS', 'merge.py')
    export_file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), '8_START_ALL_PROCESS', 'export.py')
    pull_file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), '8_START_ALL_PROCESS', 'pull_all.py')
    retore_dbs_file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), '8_START_ALL_PROCESS', 'retore_dbs.py')
    date = datetime.today().strftime('%Y%m%d_%H-%M-%S')

    echo = [sys.executable]
    
    def validate_step(step_name):
        log_dir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), 'logs')
        validate = []
        for log in os.listdir(log_dir):
            ok = True
            with open(os.path.join(log_dir, log)) as log_file:
                data = log_file.readlines()
                for l in data:
                    if len(l.split('-')) > 4 and l.split('-')[4].lower().strip() == u'error':
                        ok = False
            validate.append(ok)
        return len(list(set(validate)))
        
                

    def run_process(command):
        cmd = " ".join(echo+[command])
        print cmd
        os.popen(cmd)

    def get_steps(path_command, only_base=False, not_base=False):
        step = []
        if only_base:
            for n, USER in enumerate(USERS.ALL_CONFIG):
                if 'BASE' in USER:
                    return step.append(u"{} {} {} {}".format(path_command, n, USER['branch_name'], date))
        elif not_base:
            for n, USER in enumerate(USERS.ALL_CONFIG):
                if not('BASE' in USER):
                    step.append(u"{} {} {} {}".format(path_command, n, USER['branch_name'], date))
        else:
            for n, USER in enumerate(USERS.ALL_CONFIG):
                step.append(u"{} {} {} {}".format(path_command, n, USER['branch_name'], date))
        return tuple(step)

        

    tag_process = ['backups', 'commits', 'merges']#, 'export', 'pull', 'restore']
    all_process = [backup_file_path, commit_file_path, merge_file_paht]#, export_file_path, pull_file_path, retore_dbs_file_path]

    for data in zip(tag_process, all_process):
        tag_process = data[0]
        proc = data[1]
        if tag_process in ['merge', 'export']:
            steps = get_steps(proc, only_base=True)
        elif tag_process in ['pull', 'restore']:
            steps = get_steps(proc, not_base=True)
        else:
            steps = get_steps(proc)
        pool = Pool(processes=3)
        pool.map(run_process, steps)
        pool.close()
        if validate_step(tag_process) == 1:
            u"###{} sucess!###".format(tag_process).upper()
        else:
            u"###{} failed!###".format(tag_process).upper()
        


