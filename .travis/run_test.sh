#!/bin/sh

if [ "$TOXENV" != "cov" ] ; then
    tox
fi
