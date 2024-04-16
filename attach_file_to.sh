#!/bin/bash

function get_line_number () {
    local text=$1;
    local file=$2;
    grep "$text" $file -n -m1 | cut -d':' -f1
}

attachable_file=$1
attachable_file_path=$(find "$PWD" -name "$attachable_file")
attach_to=$2

function main() {
    local status=$(git status)

    # Check If Update Is Needed
    if ! [[ "$status" =~ .*"$attachable_file".* ]]; then return; fi;

    # Get Start & End Indexes Of Code Block
    local start=$(get_line_number "<!-- start $attachable_file" $attach_to);
    local end=$(get_line_number "<!-- end $attachable_file" $attach_to);

    ((start+=2)); # Increment By 2, Start After "```"
    ((end-=2)); # Decrement By 2, End Before "```"

    # Delete Code Block Lines
    sed -i -e "${start},${end}d;" $attach_to;

    ((start-=1)); # Increment By 2, Start After "```"

    # Add Code Block Lines
    sed -i "${start}r $attachable_file_path" $attach_to;
}

main
