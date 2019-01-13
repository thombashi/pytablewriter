# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, print_function, unicode_literals

import sys


def print_test_result(expected, actual, error=None):
    print("[expected]\n{}\n".format(expected), flush=True)
    print("[actual]\n{}\n".format(actual), flush=True)

    if error:
        print(error, file=sys.stderr, flush=True)
