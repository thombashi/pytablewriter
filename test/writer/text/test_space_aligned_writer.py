"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import collections
import itertools
from textwrap import dedent

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
        expected=dedent(
            """\
            i   f     c     if   ifc  bool     inf     nan  mix_num             time           
            1  1.10  aa     1.0    1  True   Infinity  NaN         1  2017-01-01T00:00:00      
            2  2.20  bbb    2.2  2.2  False  Infinity  NaN  Infinity  2017-01-02 03:04:05+09:00
            3  3.33  cccc  -3.0  ccc  True   Infinity  NaN       NaN  2017-01-01T00:00:00      
            """
        ),
    ),
    Data(
        header=None,
        value=value_matrix,
        expected=dedent(
            """\
            1  123.1  a    1.0     1
            2    2.2  bb   2.2   2.2
            3    3.3  ccc  3.0  cccc
            """
        ),
    ),
    Data(
        header=float_header_list,
        value=float_value_matrix,
        expected=dedent(
            """\
             a         b         c  
            0.01       0.0012  0.000
            1.00      99.9000  0.010
            1.20  999999.1230  0.001
            """
        ),
    ),
]

empty_test_data_list = [
    Data(header=header, value=value, expected=None)
    for header, value in itertools.product([None, [], ""], [None, [], ""])
]

table_writer_class = ptw.SpaceAlignedTableWriter


class Test_SpaceAlignedTableWriter_write_new_line:
    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()

        assert out == "\n"


class Test_SpaceAlignedTableWriter_write_table:
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
