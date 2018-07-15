#!/bin/sh

if [ "$TRAVIS_OS_NAME" = "osx" ] && ! python3; then
    # Install Python3 on osx
    brew upgrade python
    pip3 install setuptools --upgrade
    pip3 install .[test]
else
    pip install setuptools --upgrade
    pip install .[test]
fi
