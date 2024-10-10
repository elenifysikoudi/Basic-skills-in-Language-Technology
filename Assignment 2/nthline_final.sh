#!/usr/bin/env bash
set -o errexit
set -o nounset

n=$1
shift
for file in "$@"
do
    cat "$file" | head -n$n | tail -n1
done

    