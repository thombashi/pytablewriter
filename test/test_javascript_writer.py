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


Data = collections.namedtuple(
    "Data", "table indent header value is_write_header expected")

normal_test_data_list = [
    Data(
        table="tablename",
        indent=0,
        header=header_list,
        value=value_matrix,
        is_write_header=True,
        expected="""var tablename = [
    ["a", "b", "c", "dd", "e"],
    [1, 123.1, "a", 1.0, "1"],
    [2, 2.2, "bb", 2.2, "2.2"],
    [3, 3.3, "ccc", 3.0, "cccc"]
];
"""
    ),
    Data(
        table="tablename",
        indent=0,
        header=header_list,
        value=None,
        is_write_header=True,
        expected="""var tablename = [
    ["a", "b", "c", "dd", "e"]
];
"""
    ),
    Data(
        table="table name",
        indent=0,
        header=header_list,
        value=value_matrix,
        is_write_header=True,
        expected="""var table_name = [
    ["a", "b", "c", "dd", "e"],
    [1, 123.1, "a", 1.0, "1"],
    [2, 2.2, "bb", 2.2, "2.2"],
    [3, 3.3, "ccc", 3.0, "cccc"]
];
"""
    ),
    Data(
        table="tablename",
        indent=0,
        header=header_list,
        value=value_matrix,
        is_write_header=False,
        expected="""var tablename = [
    [1, 123.1, "a", 1.0, "1"],
    [2, 2.2, "bb", 2.2, "2.2"],
    [3, 3.3, "ccc", 3.0, "cccc"]
];
"""
    ),
    Data(
        table="tablename",
        indent=1,
        header=header_list,
        value=value_matrix,
        is_write_header=True,
        expected="""    var tablename = [
        ["a", "b", "c", "dd", "e"],
        [1, 123.1, "a", 1.0, "1"],
        [2, 2.2, "bb", 2.2, "2.2"],
        [3, 3.3, "ccc", 3.0, "cccc"]
    ];
"""
    ),
    Data(
        table="tablename",
        indent=0,
        header=header_list,
        value=value_matrix_with_none,
        is_write_header=True,
        expected="""var tablename = [
    ["a", "b", "c", "dd", "e"],
    [1, null, "a", 1.0, null],
    [null, 2.2, null, 2.2, "2.2"],
    [3, 3.3, "ccc", null, "cccc"],
    [null, null, null, null, null]
];
"""
    ),
    Data(
        table="tablename",
        indent=0,
        header=mix_header_list,
        value=mix_value_matrix,
        is_write_header=True,
        expected="""var tablename = [
    ["i", "f", "c", "if", "ifc", "bool", "inf", "nan", "mix_num", "time"],
    [1, 1.10, "aa", 1.0, "1", true, Infinity, NaN, 1.0, new Date("2017-01-01T00:00:00")],
    [2, 2.20, "bbb", 2.2, "2.2", false, Infinity, NaN, Infinity, new Date("2017-01-02T03:04:05+0900")],
    [3, 3.33, "cccc", -3.0, "ccc", true, Infinity, NaN, NaN, new Date("2017-01-01T00:00:00")]
];
"""
    ),

]

exception_test_data_list = [
    Data(
        table="",
        indent=normal_test_data_list[0].indent,
        header=normal_test_data_list[0].header,
        value=normal_test_data_list[0].value,
        is_write_header=True,
        expected=pytablewriter.EmptyTableNameError
    ),
    Data(
        table="dummy",
        indent=normal_test_data_list[0].indent,
        header=[],
        value=[],
        is_write_header=True,
        expected=pytablewriter.EmptyHeaderError
    ),
    Data(
        table="dummy",
        indent=normal_test_data_list[0].indent,
        header=[],
        value=normal_test_data_list[0].value,
        is_write_header=True,
        expected=pytablewriter.EmptyHeaderError
    ),
    Data(
        table="dummy",
        indent=normal_test_data_list[0].indent,
        header=None,
        value=normal_test_data_list[0].value,
        is_write_header=True,
        expected=pytablewriter.EmptyHeaderError
    ),
]

table_writer_class = pytablewriter.JavaScriptTableWriter


class Test_JavaScriptTableWriter_write_new_line:

    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_JavaScriptTableWriter_write_table:

    @pytest.mark.parametrize(
        ["table", "indent", "header", "value", "is_write_header", "expected"],
        [
            [
                data.table, data.indent, data.header, data.value,
                data.is_write_header, data.expected
            ]
            for data in normal_test_data_list
        ]
    )
    def test_normal_single(
            self, capsys, table, indent, header, value,
            is_write_header, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.set_indent_level(indent)
        writer.header_list = header
        writer.value_matrix = value
        writer.is_write_header = is_write_header

        writer.write_table()

        out, _err = capsys.readouterr()
        assert out == expected

    @pytest.mark.parametrize(["table", "header", "expected"], [
        [
            "tablename",
            ["ha", "hb", "hc"],
            """var tablename = [
    ["ha", "hb", "hc"],
    [1, 2, 3],
    [11, 12, 13],
    [1, 2, 3],
    [11, 12, 13],
    [101, 102, 103],
    [1001, 1002, 1003]
];
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
        ["table", "indent", "header", "value", "is_write_header", "expected"],
        [
            [
                data.table, data.indent, data.header, data.value,
                data.is_write_header, data.expected
            ]
            for data in exception_test_data_list
        ]
    )
    def test_exception(
            self, capsys, table, indent, header, value,
            is_write_header, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.set_indent_level(indent)
        writer.header_list = header
        writer.value_matrix = value
        writer.is_write_header = is_write_header

        with pytest.raises(expected):
            writer.write_table()
