import re
import os
import stat
import requests
import json
import urllib.request
import subprocess

from datetime import datetime as dt2

URL = os.getenv('PROF_GITHUB')
URI = URL.replace('https://github.com/', '')
CONTENTS = f"https://api.github.com/repos/{URI}/contents/"
PROF_WORKS = [r['name'] for r in requests.get(CONTENTS).json() if r['type'] == 'dir']
COMMIT_FILES = json.loads(os.getenv('COMMIT_FILES', "[]"))
COMMIT_TIME = os.getenv('COMMIT_TIME')
if COMMIT_TIME is None:
    COMMIT_TIME = dt2.now()
else:
    COMMIT_TIME = dt2.strptime(json.loads(COMMIT_TIME), "%Y-%m-%dT%H:%M:%SZ")
commit_time_string = COMMIT_TIME.strftime('%Y%m%d%H%M%S')
GRADER_EXEC = 'grader'

graded = set()
for file in COMMIT_FILES:
    work = file.split('/')[0]
    if work == ".github":
        continue
    if work in graded:
        continue
    graded.add(work)
    if work not in PROF_WORKS:
        continue
    prof_files = {r['name']: r["download_url"] for r in requests.get(f'{CONTENTS}/{work}').json()}
    if 'due_to.txt' in prof_files:
        date = requests.get(prof_files['due_to.txt']).content
        date = re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', str(date, encoding='utf8'))
        del prof_files['due_to.txt']
        if date:
            date = dt2.strptime(date.group(0), "%Y-%m-%dT%H:%M:%S")
            if COMMIT_TIME > date:
                continue
    print(f'TASK: {work}')
    if len(prof_files) != 1:
        print('ERROR: invalid number of grader files (warn your professor)')
        continue
    curr = os.getcwd()
    os.chdir(work)
    urllib.request.urlretrieve(list(prof_files.values())[0], GRADER_EXEC)
    os.system('ls -lh')
    os.chmod(GRADER_EXEC, stat.S_IEXEC)
    os.system('ls -lh')
    result = subprocess.run([f'./{GRADER_EXEC}', '2>&1'], capture_output=True)
    with open(f'grader_{commit_time_string}.txt', 'wb') as log_file:
        log_file.write(result.stdout)
    print(result.stdout)
    os.remove('grader')



