array_contains () {
    local seeking=$1; shift
    local in=0
    for element; do
        if [[ $element == "$seeking" ]];
        then
            in=1
            break
        fi
    done
    return $in
}

URL="${PROF_GITHUB}"
URI=$( echo "${URL}" | sed "s,https://github.com/,,g" )
CONTENTS="https://api.github.com/repos/${URI}/contents/"
PROF_WORKS=$( curl "${CONTENTS}" 2>/dev/null | jq -r '.[] | select(.type == "dir") | .name' )

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

teste="${COMMIT_FILES[*]}"
echo "${teste}"
teste=$( echo "${COMMIT_FILES[@]}" | jq -r .[] )
echo "${teste}"
teste=$( echo "${COMMIT_FILES[@]}" | jq -r .[] | readarray -t added_modified_files - )
echo "${teste}"
exit 1
for added_modified_file in "${added_modified_files[@]}";
do
  work=$( echo "${added_modified_file}" | cut -d "/" -f1 );
  if [[ "${work}" == ".github" ]];
  then
    continue;
  fi;
  if [[ $( array_contains "${work}" "${PROF_WORKS[@]}" ) == 1 ]];
  then
    echo "${work}";
    grade=0;
    if [[ -z $( curl "${CONTENTS}/${work}" 2>/dev/null | jq -r '.[] | select(.name == "due_to.txt")' 2>/dev/null ) ]];
    then
      grade=1;
    else
      date=$( date +"$( curl "${CONTENTS}/${work}/due_to.txt" 2>/dev/null | jq -r .content | base64 -d - )" )
      if [[ ${date} < ${COMMIT_TIME} ]];
      then
        grade=1;
      fi;
    fi;
  fi;
  echo ${grade};
done