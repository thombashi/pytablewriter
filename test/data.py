# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

_inf = float("inf")
_nan = float("nan")

header_list = ["a", "b", "c", "dd", "e"]
value_matrix = [
    ["1", 123.1, "a", "1",   1],
    [2, 2.2, "bb", "2.2", 2.2],
    [3, 3.3, "ccc", "3",   "cccc"],
]
value_matrix_with_none = [
    ["1", None, "a", "1",   None],
    [None, 2.2, None, "2.2", 2.2],
    [3, 3.3, "ccc", None,   "cccc"],
    [None, None, None, None,   None],
]

mix_header_list = ["i", "f", "c", "if", "ifc", "bool", "inf", "nan", "mix"]
mix_value_matrix = [
    [1, 1.1,  "aa",   1,   1,     True,   _inf,       _nan,  1.0],
    [2, 2.2,  "bbb",  2.2, 2.2,   False,  "inf",      "nan", _inf],
    [3, 3.33, "cccc", -3,  "ccc", "true", "infinity", "NAN", _nan],
]
