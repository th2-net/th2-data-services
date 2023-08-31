#!/bin/bash

API_GEN_FILE='api_gen.py'

function main() {
    echo 'Generate API docs'

    if python3 $API_GEN_FILE ; then
        echo "Docs generation succeeded"
    else
        echo "Docs generation was failed"
        exit 1
    fi

    exit 0
}

main
