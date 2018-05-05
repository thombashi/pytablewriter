# encoding: utf-8

'''
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
'''

from __future__ import absolute_import, print_function, unicode_literals


def print_test_result(expected, actual):
    print("[expected]\n{}\n".format(expected))
    print("[actual]\n{}\n".format(actual))
