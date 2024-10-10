#!/usr/bin/env bash

# This solves the second exercise at the last slide of the lecture on Bash

set -o errexit
set -o nounset

n=5

# The double quotes around the parameter $@ make sure
# arguments-with-spaces (like filenames with spaces) are handled as 1
# item in the sequence
for file in "$@"
do
    # the double quotes around $file make sure also filenames with
    # spaces are presented as 1 file to cat
    cat "$file" | head -n$n | tail -n1
done
