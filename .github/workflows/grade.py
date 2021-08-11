import re
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
    COMMIT_TIME = dt2.strptime(json.loads(COMMIT_TIME), "%Y-%m-%dT%H:%M:%SZ")

for file in COMMIT_FILES:
    work = file.split('/')[0]
    if work == ".github":
        continue
    print(work)
    if work in PROF_WORKS:
        grade = False
        date_specs = [r['name'] for r in requests.get(f'{CONTENTS}/{work}').json()]
        if 'due_to.txt' not in date_specs:
            grade = True
        else:
            date = base64.b64decode(requests.get(f'{CONTENTS}/{work}/due_to.txt').json()['content'])
            date = re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', str(date, encoding='utf8'))
            if not date:
                grade = False
            else:
                date = dt2.strptime(date.group(0), "%Y-%m-%dT%H:%M:%S")
                if COMMIT_TIME <= date:
                    grade = True
        print(grade)
