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


Data = collections.namedtuple("Data", "table header value expected")

normal_test_data_list = [
    Data(
        table="",
        header=header_list,
        value=value_matrix,
        expected="""{| class="wikitable"
! a
! b
! c
! dd
! e
|-
| style="text-align:right"| 1
| style="text-align:right"| 123.1
| a
| style="text-align:right"| 1.0
| style="text-align:right"| 1
|-
| style="text-align:right"| 2
| style="text-align:right"| 2.2
| bb
| style="text-align:right"| 2.2
| style="text-align:right"| 2.2
|-
| style="text-align:right"| 3
| style="text-align:right"| 3.3
| ccc
| style="text-align:right"| 3.0
| cccc
|}
"""
    ),
    Data(
        table=None,
        header=header_list,
        value=None,
        expected="""{| class="wikitable"
! a
! b
! c
! dd
! e
|-
|}
"""
    ),
    Data(
        table="test table",
        header=header_list,
        value=value_matrix,
        expected="""{| class="wikitable"
|+test table
! a
! b
! c
! dd
! e
|-
| style="text-align:right"| 1
| style="text-align:right"| 123.1
| a
| style="text-align:right"| 1.0
| style="text-align:right"| 1
|-
| style="text-align:right"| 2
| style="text-align:right"| 2.2
| bb
| style="text-align:right"| 2.2
| style="text-align:right"| 2.2
|-
| style="text-align:right"| 3
| style="text-align:right"| 3.3
| ccc
| style="text-align:right"| 3.0
| cccc
|}
"""
    ),
    Data(
        table="test table",
        header=header_list,
        value=value_matrix_with_none,
        expected="""{| class="wikitable"
|+test table
! a
! b
! c
! dd
! e
|-
| style="text-align:right"| 1
| 
| a
| style="text-align:right"| 1.0
| 
|-
| 
| style="text-align:right"| 2.2
| 
| style="text-align:right"| 2.2
| style="text-align:right"| 2.2
|-
| style="text-align:right"| 3
| style="text-align:right"| 3.3
| ccc
| 
| cccc
|-
| 
| 
| 
| 
| 
|}
"""
    ),
    Data(
        table="test table",
        header=mix_header_list,
        value=mix_value_matrix,
        expected="""{| class="wikitable"
|+test table
! i
! f
! c
! if
! ifc
! bool
! inf
! nan
! mix_num
! time
|-
| style="text-align:right"| 1
| style="text-align:right"| 1.10
| aa
| style="text-align:right"| 1.0
| style="text-align:right"| 1
| True
| inf
| nan
| style="text-align:right"| 1.0
| 2017-01-01 00:00:00
|-
| style="text-align:right"| 2
| style="text-align:right"| 2.20
| bbb
| style="text-align:right"| 2.2
| style="text-align:right"| 2.2
| False
| inf
| nan
| inf
| 2017-01-02 03:04:05+0900
|-
| style="text-align:right"| 3
| style="text-align:right"| 3.33
| cccc
| style="text-align:right"| -3.0
| ccc
| True
| inf
| nan
| nan
| 2017-01-01 00:00:00
|}
"""
    ),
]

exception_test_data_list = [
    Data(
        table="",
        header=[],
        value=[],
        expected=pytablewriter.EmptyHeaderError
    ),
    Data(
        table="",
        header=[],
        value=normal_test_data_list[0].value,
        expected=pytablewriter.EmptyHeaderError
    ),
    Data(
        table="",
        header=None,
        value=normal_test_data_list[0].value,
        expected=pytablewriter.EmptyHeaderError
    ),
]

table_writer_class = pytablewriter.MediaWikiTableWriter


class Test_MediaWikiTableWriter_write_new_line:

    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_MediaWikiTableWriter_write_table:

    @pytest.mark.parametrize(["table", "header", "value", "expected"], [
        [data.table, data.header, data.value, data.expected]
        for data in normal_test_data_list
    ])
    def test_normal(self, capsys, table, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.header_list = header
        writer.value_matrix = value
        writer.write_table()

        out, _err = capsys.readouterr()
        assert out == expected

    @pytest.mark.parametrize(["table", "header", "expected"], [
        [
            "tablename",
            ["ha", "hb", "hc"],
            """{| class="wikitable"
|+tablename
! ha
! hb
! hc
|-
| style="text-align:right"| 1
| style="text-align:right"| 2
| style="text-align:right"| 3
|-
| style="text-align:right"| 11
| style="text-align:right"| 12
| style="text-align:right"| 13
|-
| style="text-align:right"| 1
| style="text-align:right"| 2
| style="text-align:right"| 3
|-
| style="text-align:right"| 11
| style="text-align:right"| 12
| style="text-align:right"| 13
|-
| style="text-align:right"| 101
| style="text-align:right"| 102
| style="text-align:right"| 103
|-
| style="text-align:right"| 1001
| style="text-align:right"| 1002
| style="text-align:right"| 1003
|}
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
        writer.write_value_row_separator()
        writer.write_table()
        writer.write_value_row_separator()

        writer.is_write_closing_row = True
        writer.value_matrix = [
            [101, 102, 103],
            [1001, 1002, 1003],
        ]
        writer.write_table()

        out, _err = capsys.readouterr()
        assert out == expected

    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [
            [data.table, data.header, data.value, data.expected]
            for data in exception_test_data_list
        ]
    )
    def test_exception(self, capsys, table, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table()
