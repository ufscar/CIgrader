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
echo "PROF_WORKS"
echo "${PROF_WORKS}"

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


files=$( echo "${COMMIT_FILES[@]}" | jq -r .[] )
for added_modified_file in "${files[@]}";
do
  work=$( echo "${added_modified_file}" | cut -d "/" -f1 );
  echo "${work}";
  if [[ "${work}" == ".github" ]];
  then
    continue;
  fi;
  to_grade=$( array_contains "${work}" "${PROF_WORKS[@]}" )
  echo "GRADE? ${to_grade}"
  if [[ "${to_grade}" == "1" ]];
  then
    echo "GRADE? 1";
    grade=0;
    date_specs=$( curl "${CONTENTS}/${work}" 2>/dev/null | jq -r '.[] | select(.name == "due_to.txt")' 2>/dev/null )
    if [[ -z ${date_specs} ]];
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