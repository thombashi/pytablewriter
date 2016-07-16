# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import re


def lower_bool_converter(bool_value):
    return str(bool_value).lower()


def str_datetime_converter(value):
    return value.strftime("%Y-%m-%dT%H:%M:%S%z")


def strip_quote(text, value):
    re_replace = re.compile(
        '["\']{:s}["\']'.format(value), re.MULTILINE)
    return re_replace.sub(value, text)
