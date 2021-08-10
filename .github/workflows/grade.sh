URL="https://github.com/ufscar/CIgrader-professor" # "${PROF_GITHUB}"
URI=$( echo "${URL}" | sed "s,https://github.com/,,g" )
CONTENTS="https://api.github.com/repos/${URI}/contents/"
PROF_WORKS=$( curl "${CONTENTS}" 2>/dev/null | jq -r '.[] | select(.type == "dir") | .name' )
COMMIT_TIME='${{ steps.author-date.outputs.result }}'
echo "${COMMIT_TIME}"

#for work in "${AUX[@]}";
#do
#  if [[ -z $( curl "${CONTENTS}/${work}" 2>/dev/null | jq -r '.[] | select(.name == "due_to.txt")' ) ]];
#  then
#    echo "${work}";
#  else [[  ]];
#  then
#
#  fi;
#done;


#readarray -t added_modified_files <<<"$(jq -r '.[]' <<<'${{ steps.files.outputs.added_modified }}')"
#for added_modified_file in "${added_modified_files[@]}";
#do
#  work=$( echo "${added_modified_file}" | cut -d "/" -f1 )
#  if [[ " ${PROF_WORKS[@]} " =~ " ${work} " ]];
#  then
#    grade=0;
#    if [[ -z $( curl "${CONTENTS}/${work}" 2>/dev/null | jq -r '.[] | select(.name == "due_to.txt")' 2>/dev/null ) ]];
#    then
#      grade=1;
#    else [[ date +"$( cat teste )" ]];
#    then
#      grade=1;
#    fi;
#  fi;
#done