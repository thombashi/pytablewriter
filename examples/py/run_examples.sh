#!/bin/sh

# Execute all of the examples

for l in $(find . -executable -type f -not -name 'run_examples.sh'); do
    echo "$l"
    $l
done
