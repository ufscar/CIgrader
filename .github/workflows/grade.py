import os
import requests

URL = os.getenv('PROF_GITHUB')
URI = URL.replace('https://github.com/', '')
CONTENTS = f"https://api.github.com/repos/{URI}/contents/"
PROF_WORKS = [r['name'] for r in requests.get(CONTENTS).json() if r['type'] == 'dir']
COMMIT_FILES = os.getenv('COMMIT_FILES')
print(COMMIT_FILES, type(COMMIT_FILES))

# for added_modified_file in "${files[@]}";
# do
#   work=$( echo "${added_modified_file}" | cut -d "/" -f1 );
# #  echo "${work}";
# #  echo " \"${work}\" == \".github\" ";
#   if [[ "${work}" == ".github" ]];
#   then
#     continue;
#   fi;
#   to_grade=$( array_contains "${work}" "${PROF_WORKS[@]}" )
#   echo "${to_grade}"
#   if [[ "${to_grade}" == "1" ]];
#   then
# #    echo "GRADE? 1";
#     grade=0;
#     date_specs=$( curl "${CONTENTS}/${work}" 2>/dev/null | jq -r '.[] | select(.name == "due_to.txt")' 2>/dev/null )
#     if [[ -z ${date_specs} ]];
#     then
#       grade=1;
#     else
#       date=$( date +"$( curl "${CONTENTS}/${work}/due_to.txt" 2>/dev/null | jq -r .content | base64 -d - )" )
#       if [[ ${date} < ${COMMIT_TIME} ]];
#       then
#         grade=1;
#       fi;
#     fi;
#   fi;
#   echo ${grade};
# done