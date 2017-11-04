# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import collections
import itertools

import pytest

import pytablewriter as ptw

from .data import (
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
        expected="""i   f     c    if   ifc  bool     inf     nan  mix_num             time           
1   1.1  aa      1    1  True   Infinity  NaN         1  2017-01-01 00:00:00      
2   2.2  bbb   2.2  2.2  False  Infinity  NaN  Infinity  2017-01-02 03:04:05+09:00
3  3.33  cccc   -3  ccc  True   Infinity  NaN       NaN  2017-01-01 00:00:00      
"""),
    Data(
        header=None,
        value=value_matrix,
        expected="""1  123.1  a      1     1
2    2.2  bb   2.2   2.2
3    3.3  ccc    3  cccc
"""),
    Data(
        header=float_header_list,
        value=float_value_matrix,
        expected=""" a        b         c  
0.01     0.00125      0
   1        99.9   0.01
 1.2  999999.123  0.001
"""),
]

exception_test_data_list = [
    Data(
        header=header,
        value=value,
        expected=ptw.EmptyTableDataError)
    for header, value in itertools.product([None, [], ""], [None, [], ""])
]

table_writer_class = ptw.SpaceAlignedTableWriter


class Test_SpaceAlignedTableWriter_write_new_line(object):

    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()

        assert out == "\n"


class Test_SpaceAlignedTableWriter_write_table(object):

    @pytest.mark.parametrize(["header", "value", "expected"], [
        [data.header, data.value, data.expected]
        for data in normal_test_data_list
    ])
    def test_normal(self, capsys, header, value, expected):
        writer = table_writer_class()
        writer.header_list = header
        writer.value_matrix = value
        writer.write_table()

        out, _err = capsys.readouterr()

        print("[expected]\n{}".format(expected))
        print("[actual]\n{}".format(out))

        assert out == expected

    @pytest.mark.parametrize(["header", "value", "expected"], [
        [data.header, data.value, data.expected]
        for data in exception_test_data_list
    ])
    def test_exception(self, header, value, expected):
        writer = table_writer_class()
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table()
