# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import collections

import pytablewriter
import pytest

from .data import header_list
from .data import value_matrix


Data = collections.namedtuple("Data", "col_delim header value expected")

normal_test_data_list = [
    Data(
        col_delim=",",
        header=header_list,
        value=value_matrix,
        expected=""""a","b","c","dd","e"
1,123.1,"a",1.0,"1"
2,2.2,"bb",2.2,"2.2"
3,3.3,"ccc",3.0,"cccc"
"""
    ),
    Data(
        col_delim=",",
        header=[],
        value=value_matrix,
        expected="""1,123.1,"a",1.0,"1"
2,2.2,"bb",2.2,"2.2"
3,3.3,"ccc",3.0,"cccc"
"""
    ),
    Data(
        col_delim="\t",
        header=None,
        value=value_matrix,
        expected="""1\t123.1\t"a"\t1.0\t"1"
2\t2.2\t"bb"\t2.2\t"2.2"
3\t3.3\t"ccc"\t3.0\t"cccc"
"""
    ),
]

exception_test_data_list = [
    Data(
        col_delim=",",
        header=[],
        value=[],
        expected=pytablewriter.EmptyValueError,
    ),
    Data(
        col_delim=",",
        header=header_list,
        value=[],
        expected=pytablewriter.EmptyValueError,
    ),
]

table_writer_class = pytablewriter.CsvTableWriter


class Test_CsvTableWriter_write_new_line:

    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, err = capsys.readouterr()
        assert out == "\n"


class Test_CsvTableWriter_write_table:

    @pytest.mark.parametrize(["col_delim", "header", "value", "expected"], [
        [data.col_delim, data.header, data.value, data.expected]
        for data in normal_test_data_list
    ])
    def test_normal(self, capsys, col_delim, header, value, expected):
        writer = table_writer_class()
        writer.column_delimiter = col_delim
        writer.header_list = header
        writer.value_matrix = value
        writer.write_table()

        out, err = capsys.readouterr()
        assert out == expected

    @pytest.mark.parametrize(["header", "value", "expected"], [
        [data.header, data.value, data.expected]
        for data in exception_test_data_list
    ])
    def test_exception(self, capsys, header, value, expected):
        writer = table_writer_class()
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table()
