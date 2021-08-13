import re
import os
import stat
import requests
import json
import urllib.request
import github3
import subprocess

from datetime import datetime as dt2

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPOSITORY = os.getenv('GITHUB_REPOSITORY')
GITHUB_REPOSITORY_OWNER, GITHUB_REPOSITORY_NAME = GITHUB_REPOSITORY.split('/')
GITHUB_ACTOR = os.getenv('GITHUB_ACTOR')
COMMIT_FILES = json.loads(os.getenv('COMMIT_FILES', "[]"))
COMMIT_TIME = os.getenv('COMMIT_TIME')
if COMMIT_TIME is None:
    COMMIT_TIME = dt2.now()
else:
    COMMIT_TIME = dt2.strptime(json.loads(COMMIT_TIME), "%Y-%m-%dT%H:%M:%SZ")

URL = os.getenv('PROF_GITHUB')
URI = URL.replace('https://github.com/', '')
CONTENTS = f"https://api.github.com/repos/{URI}/contents/"
commit_time_string = COMMIT_TIME.strftime('%Y%m%d%H%M%S')
GRADER_EXEC = 'grader'
GRADER_FOLDER = 'comments'
DATE_FILE = 'due_to.txt'

git = github3.GitHub(token=GITHUB_TOKEN)
repo = git.repository(GITHUB_REPOSITORY_OWNER, GITHUB_REPOSITORY_NAME)

PROF_WORKS = [r['name'] for r in requests.get(CONTENTS).json() if r['type'] == 'dir']

print(f'PROFESSOR GITHUB: {URI}')

graded = set()
scores = list()
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
    if DATE_FILE in prof_files:
        date = requests.get(prof_files[DATE_FILE]).content
        date = re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', str(date, encoding='utf8'))
        del prof_files[DATE_FILE]
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
    os.chmod(GRADER_EXEC, stat.S_IRWXU)
    log_file = f'{work}_{commit_time_string}.txt'
    log = subprocess.run([f'./{GRADER_EXEC}'],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT).stdout
    os.remove(GRADER_EXEC)
    repo.create_file(path=os.path.join(GRADER_FOLDER, log_file),
                     message=f'task "{work}" grader',
                     content=log
                     )
    log = str(log, encoding='utf8')
    score = log.strip().splitlines()[-1]
    score_file = os.path.join(GRADER_FOLDER, f'{work}_current_score.txt')
    contents = repo.file_contents(path=score_file, ref='master')
    if not contents:
        repo.create_file(path=score_file,
                         message=f'task "{work}" score',
                         content=bytes(score, encoding='utf8')
                         )
    else:
        contents.update(message=f'task "{work}" score',
                        content=bytes(score, encoding='utf8')
                        )

    score = json.loads(score)
    score['task'] = work
    scores.append(score)
    os.chdir(curr)

print(json.dumps(scores))
