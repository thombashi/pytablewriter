# encoding: utf-8

from __future__ import unicode_literals


def bool_to_str(value):
    if value is True:
        return "true"
    if value is False:
        return "false"

    return value
