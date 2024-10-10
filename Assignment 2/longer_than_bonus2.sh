#!/usr/bin/env bash

set -o errexit
set -o nounset

n=$1
path=$2

if [ -d "$path" ]
then
    for file in "$2"/*
    do
    no_of_lines=$(wc -l < $file)
    if [ "$no_of_lines" -ge "$n" ]
    then
        name_of_file=$(basename $file)
        echo -e ""$name_of_file"\t"$no_of_lines""
    fi
done

elif [ -f "$path" ]
then 
    no_of_lines=$(wc -l < $path)
    if [ "$no_of_lines" -ge "$n" ]
    then
        name_of_file=$(basename $path)
        echo -e ""$name_of_file"\t"$no_of_lines""
    fi
fi

