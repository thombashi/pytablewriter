#!/usr/bin/env bash

if [ "$TRAVIS_OS_NAME" = "osx" ]; then
    if ! type python3 > /dev/null 2>&1; then
        # Install Python3 on osx
        brew upgrade python
    fi

    pip3 install pip setuptools --upgrade
    pip3 install .[test]
else
    pip install pip setuptools --upgrade
    pip install .[test]
fi
