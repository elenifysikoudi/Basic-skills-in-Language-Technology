#!/usr/bin/env bash

set -o errexit
set -o nounset

while true
do
    symbol=$(($RANDOM % 2))
    if [ "$symbol" -eq 0 ]
    then 
        echo -ne \\
    else
        echo -n /
    fi
done