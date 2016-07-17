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
from .data import value_matrix_with_none
from .data import mix_header_list
from .data import mix_value_matrix


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
        header=header_list,
        value=[],
        expected=""""a","b","c","dd","e"
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
    Data(
        col_delim=",",
        header=header_list,
        value=value_matrix_with_none,
        expected=""""a","b","c","dd","e"
1,,"a",1.0,
,2.2,,2.2,"2.2"
3,3.3,"ccc",,"cccc"
,,,,
"""
    ),
    Data(
        col_delim=",",
        header=mix_header_list,
        value=mix_value_matrix,
        expected=""""i","f","c","if","ifc","bool","inf","nan","mix_num","time"
1,1.10,"aa",1.0,"1",True,inf,nan,1.0,"2017-01-01 00:00:00"
2,2.20,"bbb",2.2,"2.2",False,inf,nan,inf,"2017-01-02 03:04:05+0900"
3,3.33,"cccc",-3.0,"ccc",True,inf,nan,nan,"2017-01-01 00:00:00"
"""
    ),
]

exception_test_data_list = [

]

table_writer_class = pytablewriter.CsvTableWriter


class Test_CsvTableWriter_write_new_line:

    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
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

        out, _err = capsys.readouterr()
        assert out == expected

    @pytest.mark.parametrize(["table", "header", "expected"], [
        [
            "tablename",
            ["ha", "hb", "hc"],
            """"ha","hb","hc"
1,2,3
11,12,13
1,2,3
11,12,13
101,102,103
1001,1002,1003
""",
        ],
    ])
    def test_normal_multiple(self, capsys, table, header, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.header_list = header

        writer.is_write_header = True
        writer.is_write_closing_row = False
        writer.write_table()

        writer.is_write_opening_row = False
        writer.is_write_header = False
        writer.value_matrix = [
            [1, 2, 3],
            [11, 12, 13],
        ]
        writer.write_table()
        writer.write_table()

        writer.is_write_closing_row = True
        writer.value_matrix = [
            [101, 102, 103],
            [1001, 1002, 1003],
        ]
        writer.write_table()

        out, _err = capsys.readouterr()
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
