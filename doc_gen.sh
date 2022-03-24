#!/bin/bash

TOC_GEN_FILE='gh-md-toc'
API_GEN_FILE='api_gen.py'


function install_toc_generator() {
    wget https://raw.githubusercontent.com/ekalinin/github-markdown-toc/master/gh-md-toc
    chmod a+x gh-md-toc
}

function main() {
    echo 'Generate API docs'
    python3 $API_GEN_FILE

    echo
    echo 'Add TOC to README.md'

    # check_if_toc_generator_exists
    if [ ! -f $TOC_GEN_FILE ]; then
        install_toc_generator
    fi

    ./gh-md-toc --no-backup --hide-footer README.md

    exit 0
}

main