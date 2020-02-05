"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""


import re


def strip_quote(text, value):
    re_replace = re.compile("[\"']{:s}[\"']".format(value), re.MULTILINE)

    return re_replace.sub(value, text)
