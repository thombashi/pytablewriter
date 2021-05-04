"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import collections
import itertools

import pytest

import pytablewriter as ptw

from ..._common import print_test_result
from ...data import (
    float_header_list,
    float_value_matrix,
    mix_header_list,
    mix_value_matrix,
    value_matrix,
)


Data = collections.namedtuple("Data", "header value expected")

normal_test_data_list = [
    Data(
        header=mix_header_list,
        value=mix_value_matrix,
        expected=""""i"\t"f"\t"c"\t"if"\t"ifc"\t"bool"\t"inf"\t"nan"\t"mix_num"\t"time"
1\t1.1\t"aa"\t1\t1\tTrue\tInfinity\tNaN\t1\t"2017-01-01T00:00:00"
2\t2.2\t"bbb"\t2.2\t2.2\tFalse\tInfinity\tNaN\tInfinity\t"2017-01-02 03:04:05+09:00"
3\t3.33\t"cccc"\t-3\t"ccc"\tTrue\tInfinity\tNaN\tNaN\t"2017-01-01T00:00:00"
""",
    ),
    Data(
        header=None,
        value=value_matrix,
        expected="""1\t123.1\t"a"\t1\t1
2\t2.2\t"bb"\t2.2\t2.2
3\t3.3\t"ccc"\t3\t"cccc"
""",
    ),
    Data(
        header=float_header_list,
        value=float_value_matrix,
        expected=""""a"\t"b"\t"c"
0.01\t0.00125\t0
1\t99.9\t0.01
1.2\t999999.123\t0.001
""",
    ),
]

empty_test_data_list = [
    Data(header=header, value=value, expected=None)
    for header, value in itertools.product([None, [], ""], [None, [], ""])
]

table_writer_class = ptw.TsvTableWriter


class Test_TsvTableWriter_write_new_line:
    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()

        assert out == "\n"


class Test_TsvTableWriter_write_table:
    @pytest.mark.parametrize(
        ["header", "value", "expected"],
        [[data.header, data.value, data.expected] for data in normal_test_data_list],
    )
    def test_normal(self, capsys, header, value, expected):
        writer = table_writer_class()
        writer.headers = header
        writer.value_matrix = value
        writer.write_table()

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected

        # margin setting must be ignored
        writer.margin = 1
        out = writer.dumps()
        print_test_result(expected=expected, actual=out)
        assert out == expected

    @pytest.mark.parametrize(
        ["header", "value", "expected"],
        [[data.header, data.value, data.expected] for data in empty_test_data_list],
    )
    def test_normal_empty(self, header, value, expected):
        writer = table_writer_class()
        writer.headers = header
        writer.value_matrix = value

        assert writer.dumps() == ""
        assert str(writer) == ""
