#!/bin/bash

set -euo pipefail

attachable_file=$1
attachable_file_path=$(find "$PWD" -name "$attachable_file")
output_file_path=$PWD"/"$2

function main() {
  status=$(git status)

  if [[ "$status" =~ .*"$attachable_file".* ]]; then
    count=0
    start_line=0
    end_line=0

    exec 0<"$output_file_path"
    while read -r line
    do
      count=$((count+1))

      if [[ $line =~ "<!--".*"start".*"$attachable_file" ]]; then
        start_line=$count
      fi

      if [[ $line =~ "<!--".*"end".*"$attachable_file" ]]; then
        end_line=$count
      fi
    done

    head -n $start_line "$output_file_path" > buffer
    {
      printf '```python\n'
      cat "$attachable_file_path"
      printf '\n```\n'
      tail -n $((count - end_line + 1)) "$output_file_path"
    }>> buffer
    rm "$output_file_path"
    mv -f buffer "$output_file_path"
    git add "$output_file_path"
  fi

  exit 0
}

main