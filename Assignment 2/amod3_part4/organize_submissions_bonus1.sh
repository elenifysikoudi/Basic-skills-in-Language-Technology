#!/usr/bin/env bash

set -o errexit
set -o nounset

current_dir=$(pwd)
path=$1
cd "$path"

for file in ./*
do  
    student_code=${file:0:6}
    filename=${file:7}
    if ! [ -d "../$student_code" ]
   then 
      mkdir "../$student_code"
    fi

    cp "$file" "../$student_code/$filename"


done