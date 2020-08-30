"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import collections
import datetime
import itertools
from decimal import Decimal

from tabledata import TableData

from pytablewriter.style import Style


TIME = datetime.datetime(2017, 1, 1, 0, 0, 0)
INF = float("inf")
NAN = float("nan")

headers = ["a", "b", "c", "dd", "e"]
value_matrix = [
    ["1", 123.1, "a", "1", 1],
    [2, 2.2, "bb", "2.2", 2.2],
    [3, 3.3, "ccc", "3", "cccc"],
]
value_matrix_with_none = [
    ["1", None, "a", "1", None],
    [None, 2.2, None, "2.2", 2.2],
    [3, 3.3, "ccc", None, "cccc"],
    [None, None, None, None, None],
]

mix_header_list = [
    "i",
    "f",
    "c",
    "if",
    "ifc",
    "bool",
    "inf",
    "nan",
    "mix_num",
    "time",
]
mix_value_matrix = [
    [
        1,
        1.1,
        "aa",
        1,
        1,
        True,
        INF,
        NAN,
        1.0,
        TIME,
    ],
    [
        2,
        2.2,
        "bbb",
        2.2,
        2.2,
        False,
        Decimal("inf"),
        Decimal("nan"),
        INF,
        "2017-01-02 03:04:05+09:00",
    ],
    [
        3,
        3.33,
        "cccc",
        -3,
        "ccc",
        True,
        float("infinity"),
        float("NAN"),
        NAN,
        TIME,
    ],
]
mix_tabledata = TableData(table_name="mix data", headers=mix_header_list, rows=mix_value_matrix)

float_header_list = ["a", "b", "c"]
float_value_matrix = [
    [0.01, 0.00125, 0.0],
    [1.0, 99.9, 0.01],
    [1.2, 999999.123, 0.001],
]
float_tabledata = TableData(
    table_name="float data", headers=float_header_list, rows=float_value_matrix
)

value_matrix_iter = [
    [
        [1, 2, 3],
        [11, 12, 13],
    ],
    [
        [1, 2, 3],
        [11, 12, 13],
    ],
    [
        [101, 102, 103],
        [1001, 1002, 1003],
    ],
]

value_matrix_iter_1 = [
    [
        ["a b c d e f g h i jklmn", 2.1, 3],
        ["aaaaa", 12.1, 13],
    ],
    [
        ["bbb", 2, 3],
        ["cc", 12, 13],
    ],
    [
        ["a", 102, 103],
        ["", 1002, 1003],
    ],
]

Data = collections.namedtuple("Data", "table indent header value expected")
null_test_data_list = [
    Data(table="dummy", indent=0, header=header, value=value, expected="")
    for header, value in itertools.product([None, [], ""], [None, [], ""])
]

vut_style_tabledata = TableData(
    "style test",
    [
        "none",
        "empty",
        "tiny",
        "small",
        "medium",
        "large",
        "null w/ bold",
        "L bold",
        "S italic",
        "L bold italic",
    ],
    [
        [111, 111, 111, 111, 111, 111, "", 111, 111, 111],
        [1234, 1234, 1234, 1234, 1234, 1234, "", 1234, 1234, 1234],
    ],
)
vut_styles = [
    None,
    Style(),
    Style(font_size="TINY"),
    Style(font_size="SMALL"),
    Style(font_size="MEDIUM", thousand_separator=","),
    Style(font_size="LARGE", thousand_separator=" "),
    Style(font_weight="bold", thousand_separator=","),
    Style(font_size="LARGE", font_weight="bold"),
    Style(font_size="SMALL", font_style="italic"),
    Style(font_size="LARGE", font_weight="bold", font_style="italic"),
]
