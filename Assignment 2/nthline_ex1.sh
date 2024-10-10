#!/usr/bin/env bash

# This solves the first exercise at the last slide of the lecture on Bash

set -o errexit
set -o nounset

n=$1

for file in ./*
do
    # the double quotes around $file make sure also filenames with
    # spaces are presented as 1 file to cat
    cat "$file" | head -n$n | tail -n1
done
