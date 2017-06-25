# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals
import re


def strip_quote(text, value):
    re_replace = re.compile(
        '["\']{:s}["\']'.format(value), re.MULTILINE)
    return re_replace.sub(value, text)
