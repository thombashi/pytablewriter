#!/usr/bin/env bash

if [ "$TOXENV" != "cov" ] ; then
    tox -- --md-report-color never --md-report-zeros empty
else
    tox
fi
