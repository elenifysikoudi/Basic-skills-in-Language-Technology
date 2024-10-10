#!/usr/bin/env bash

set -o errexit
set -o nounset

current_dir=$(pwd)
path=$1
remarks="$current_dir/$2"


for file in "$path"/*
do  
    name=$(basename "$file")
    student_code=${name:0:4}
    filename=${name:5}
    target_dir="$current_dir/$student_code"
    
    if ! [ -d "$target_dir" ]
    then 
        mkdir "$target_dir"
    fi
    cp "$file" "$target_dir/$filename"

    if [ -n "$remarks" ]
    then
        remarks_name="remarks_$student_code"
        cp "$remarks" "$target_dir/$remarks_name"
    fi
done  


