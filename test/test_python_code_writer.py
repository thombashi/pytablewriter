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


Data = collections.namedtuple("Data", "table indent header value expected")

normal_test_data_list = [
    Data(
        table="",
        indent=0,
        header=header_list,
        value=value_matrix,
        expected="""[
    ["a", "b", "c", "dd", "e"],
    [1, 123.1, "a", 1.0, "1"],
    [2, 2.2, "bb", 2.2, "2.2"],
    [3, 3.3, "ccc", 3.0, "cccc"],
]
"""
    ),
    Data(
        table="tablename",
        indent=0,
        header=header_list,
        value=None,
        expected="""tablename = [
    ["a", "b", "c", "dd", "e"],
]
"""
    ),
    Data(
        table="tablename",
        indent=0,
        header=header_list,
        value=value_matrix,
        expected="""tablename = [
    ["a", "b", "c", "dd", "e"],
    [1, 123.1, "a", 1.0, "1"],
    [2, 2.2, "bb", 2.2, "2.2"],
    [3, 3.3, "ccc", 3.0, "cccc"],
]
"""
    ),
    Data(
        table="table name",
        indent=0,
        header=header_list,
        value=value_matrix,
        expected="""table_name = [
    ["a", "b", "c", "dd", "e"],
    [1, 123.1, "a", 1.0, "1"],
    [2, 2.2, "bb", 2.2, "2.2"],
    [3, 3.3, "ccc", 3.0, "cccc"],
]
"""
    ),
    Data(
        table="tablename",
        indent=1,
        header=header_list,
        value=value_matrix,
        expected="""    tablename = [
        ["a", "b", "c", "dd", "e"],
        [1, 123.1, "a", 1.0, "1"],
        [2, 2.2, "bb", 2.2, "2.2"],
        [3, 3.3, "ccc", 3.0, "cccc"],
    ]
"""
    ),
    Data(
        table="table name",
        indent=0,
        header=header_list,
        value=value_matrix_with_none,
        expected="""table_name = [
    ["a", "b", "c", "dd", "e"],
    [1, None, "a", 1.0, None],
    [None, 2.2, None, 2.2, "2.2"],
    [3, 3.3, "ccc", None, "cccc"],
    [None, None, None, None, None],
]
"""
    ),
    Data(
        table="tablename",
        indent=0,
        header=mix_header_list,
        value=mix_value_matrix,
        expected="""tablename = [
    ["i", "f", "c", "if", "ifc", "bool", "inf", "nan", "mix_num", "time"],
    [1, 1.10, "aa", 1.0, "1", True, float("inf"), float("nan"), 1.0, "2017-01-01 00:00:00"],
    [2, 2.20, "bbb", 2.2, "2.2", False, float("inf"), float("nan"), float("inf"), "2017-01-02 03:04:05+0900"],
    [3, 3.33, "cccc", -3.0, "ccc", True, float("inf"), float("nan"), float("nan"), "2017-01-01 00:00:00"],
]
"""
    ),
]

exception_test_data_list = [
    Data(
        table="dummy",
        indent=normal_test_data_list[0].indent,
        header=[],
        value=[],
        expected=pytablewriter.EmptyHeaderError
    ),
    Data(
        table="dummy",
        indent=normal_test_data_list[0].indent,
        header=[],
        value=value_matrix,
        expected=pytablewriter.EmptyHeaderError
    ),
    Data(
        table="dummy",
        indent=normal_test_data_list[0].indent,
        header=None,
        value=value_matrix,
        expected=pytablewriter.EmptyHeaderError
    ),
]

table_writer_class = pytablewriter.PythonCodeTableWriter


class Test_PythonCodeTableWriter_write_new_line:

    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_PythonCodeTableWriter_write_table:

    @pytest.mark.parametrize(
        ["table", "indent", "header", "value", "expected"],
        [
            [data.table, data.indent, data.header, data.value, data.expected]
            for data in normal_test_data_list
        ]
    )
    def test_normal(self, capsys, table, indent, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.set_indent_level(indent)
        writer.header_list = header
        writer.value_matrix = value
        writer.write_table()

        out, _err = capsys.readouterr()
        assert out == expected

    @pytest.mark.parametrize(["table", "header", "expected"], [
        [
            "tablename",
            ["ha", "hb", "hc"],
            """tablename = [
    ["ha", "hb", "hc"],
    [1, 2, 3],
    [11, 12, 13],
    [1, 2, 3],
    [11, 12, 13],
    [101, 102, 103],
    [1001, 1002, 1003],
]
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

    @pytest.mark.parametrize(
        ["table", "indent", "header", "value", "expected"],
        [
            [data.table, data.indent, data.header, data.value, data.expected]
            for data in exception_test_data_list
        ]
    )
    def test_exception(self, capsys, table, indent, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.set_indent_level(indent)
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table()
