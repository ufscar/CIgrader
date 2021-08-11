import os
import requests
import json
import base64

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
    COMMIT_TIME = dt2.strptime("%Y-%m-%dT%H:%M:%S", json.loads(COMMIT_TIME).strip('Z'))

for file in COMMIT_FILES:
    work = file.split('/')[0]
    if work == ".github":
        continue
    print(work)
    if work in PROF_WORKS:
        print(f'GRADE: 1')
        grade = False
        date_specs = [r['name'] for r in requests.get(f'{CONTENTS}/{work}').json()]
        if 'due_to.txt' not in date_specs:
            grade = True
        date = base64.b64decode(requests.get(f'{CONTENTS}/{work}/due_to.txt').json()['content'])
        date = dt2.strptime("%Y-%m-%dT%H:%M:%SZ", str(date, encoding='utf8'))
        if COMMIT_TIME <= date:
            grade = True
        print(grade)
