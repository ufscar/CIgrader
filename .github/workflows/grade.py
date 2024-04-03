import re
import os
import stat
import requests
import json
import urllib.request
import github3
import subprocess

from datetime import datetime as dt2

def is_json(s):
    try:
        json.loads(s)
        return True
    except ValueError:
        return False

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
commit_time_string = COMMIT_TIME.strftime('%Y%m%d%H%M%S')
GRADER_EXEC = 'grader'
GRADER_FOLDER = 'comments'
DATE_FILE = 'due_to.txt'


def main():
    if URL is None:
        print('Variable PROF_GITHUB not defined')
        return

    if '***' in URL:
        print('The grader has no permition to see your secrets')
        return

    URI = URL.replace('https://github.com/', '')
    CONTENTS = f"https://api.github.com/repos/{URI}/contents/"

    prof_user, prof_repo = URI.split("/")
    print(f'PROFESSOR GITHUB: {prof_user} {prof_repo}')

    git = github3.GitHub(token=GITHUB_TOKEN)
    repo = git.repository(GITHUB_REPOSITORY_OWNER, GITHUB_REPOSITORY_NAME)

    js = requests.get(CONTENTS).json()
    if isinstance(js, (str, bytes)):
        return
        
    PROF_TASKS = [f['name'] for f in js if f['type'] == 'dir']
    COMMIT_TASKS = [file.split('/')[0] for file in COMMIT_FILES]
    if len(PROF_TASKS) == 0:
        return
    if GITHUB_ACTOR == prof_user:
        tasks_to_grade = set(PROF_TASKS)
    else:
        tasks_to_grade = set(t for t in COMMIT_TASKS if t in PROF_TASKS)

    print(tasks_to_grade)
    scores = list()
    for task in tasks_to_grade:
        if not os.path.exists(task):
            continue
        prof_files = {r['name']: r["download_url"] for r in requests.get(f'{CONTENTS}/{task}').json()}
        if DATE_FILE in prof_files:
            date = requests.get(prof_files[DATE_FILE]).content
            del prof_files[DATE_FILE]
            if GITHUB_ACTOR != prof_user:
                date = re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', str(date, encoding='utf8'))

                if date:
                    date = dt2.strptime(date.group(0), "%Y-%m-%dT%H:%M:%S")
                    if COMMIT_TIME > date:
                        continue
        print(f'TASK: {task}')
        if len(prof_files) != 1:
            print('ERROR: invalid number of grader files (warn your professor)')
            continue
        curr = os.getcwd()
        os.chdir(task)
        urllib.request.urlretrieve(list(prof_files.values())[0], GRADER_EXEC)
        os.chmod(GRADER_EXEC, stat.S_IRWXU)
        log_file = f'{task}_{commit_time_string}.txt'
        log = subprocess.run([f'./{GRADER_EXEC}'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT).stdout
        os.remove(GRADER_EXEC)
        repo.create_file(path=os.path.join(GRADER_FOLDER, log_file),
                         message=f'task "{task}" grader [skip ci]',
                         content=log
                         )
        log = str(log, encoding='utf8')
        print(log)
        score = log.strip().splitlines()
        if len(score) == 0:
            continue
        score = score[-1]
        if is_json(score):
            score_file = os.path.join(GRADER_FOLDER, f'{task}_current_score.txt')
            try:
                contents = repo.file_contents(path=score_file)
                contents.update(message=f'task "{task}" score [skip ci]',
                                content=bytes(score, encoding='utf8')
                                )
            except github3.exceptions.NotFoundError:
                repo.create_file(path=score_file,
                                 message=f'task "{task}" score [skip ci]',
                                 content=bytes(score, encoding='utf8')
                                 )

            score = json.loads(score)
            score['task'] = task
            scores.append(score)

        os.chdir(curr)

    print(json.dumps(scores))


if __name__ == '__main__':
    main()
