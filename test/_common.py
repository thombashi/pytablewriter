"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import sys


def print_test_result(expected, actual, error=None):
    print("[expected]\n{}\n".format(expected))
    print("[actual]\n{}\n".format(actual))

    if error:
        print(error, file=sys.stderr)

    print("----------------------------------------")
