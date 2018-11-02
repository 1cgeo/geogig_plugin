import sys, os, platform, json
from multiprocessing import Pool
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ALL_USERS_CONFIG import USERS


if platform.system() == 'Windows':
    new_console_command = 'cmd.exe /c start'.split()
else:
    new_console_command = 'x-terminal-emulator -e'.split()

echo = [sys.executable]
 
def run_process(command):
    cmd = " ".join(new_console_command+echo+[command])
    print cmd
    os.popen(cmd)

backup_file_path = ''
commit_file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), '8_START_ALL_PROCESS', 'commit.py')
merge_file_paht = ''
pull_export_file_path = ''


step1 = []
for n, _ in enumerate(USERS.ALL_CONFIG):
    step1.append(u"{} {}".format(commit_file_path, n))
    
step1 = tuple(step1)
run_process(step1[0])
''' pool = Pool(processes=3)
pool.map(run_process, tuple(step1))
pool.close() 
 '''
