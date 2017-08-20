# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import print_function
from __future__ import unicode_literals

from pytablewriter._function import convert_idx_to_alphabet
import pytest


class Test_convert_idx_to_alphabet(object):

    @pytest.mark.parametrize(["value", "expected"], [
        [
            range(30),
            [
                "A", "B", "C", "D", "E",
                "F", "G", "H", "I", "J",
                "K", "L", "M", "N", "O",
                "P", "Q", "R", "S", "T",
                "U", "V", "W", "X", "Y",
                "Z", "AA", "AB", "AC", "AD",
            ]
        ],
        [
            range(0, 900, 30),
            [
                "A", "AE", "BI", "CM", "DQ",
                "EU", "FY", "HC", "IG", "JK",
                "KO", "LS", "MW", "OA", "PE",
                "QI", "RM", "SQ", "TU", "UY",
                "WC", "XG", "YK", "ZO", "AAS",
                "ABW", "ADA", "AEE", "AFI", "AGM",
            ]
        ],
    ])
    def test_normal(self, value, expected):
        assert [convert_idx_to_alphabet(v) for v in value] == expected
