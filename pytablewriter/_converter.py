# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import re


def lower_bool_converter(bool_value):
    return str(bool_value).lower()


def strip_quote(text, value):
    re_replace = re.compile(
        '["\']%s["\']' % (value), re.MULTILINE)
    return re_replace.sub(value, text)
