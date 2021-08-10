URL=${PROF_GITHUB}
echo "$URL"

#readarray -t added_modified_files <<<"$(jq -r '.[]' <<<'${{ steps.files.outputs.added_modified }}')"
#for added_modified_file in "${added_modified_files[@]}"; do
#  echo "${added_modified_file}" | cut -d "/" -f1
#done