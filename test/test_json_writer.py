# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import print_function
import collections
import json

import pytablewriter
import pytest

from .data import header_list
from .data import value_matrix
from .data import value_matrix_with_none
from .data import mix_header_list
from .data import mix_value_matrix
from .data import value_matrix_iter


Data = collections.namedtuple("Data", "table header value expected")

normal_test_data_list = [
    Data(
        table="",
        header=header_list,
        value=value_matrix,
        expected=json.loads("""[
            {
                "a": 1,
                "b": 123.1,
                "c": "a",
                "dd": 1,
                "e": 1
            },
            {
                "a": 2,
                "b": 2.2,
                "c": "bb",
                "dd": 2.2,
                "e": 2.2
            },
            {
                "a": 3,
                "b": 3.3,
                "c": "ccc",
                "dd": 3,
                "e": "cccc"
            }
        ]
        """)
    ),
    Data(
        table="",
        header=header_list,
        value=None,
        expected=json.loads("[]")
    ),
    Data(
        table="tablename",
        header=header_list,
        value=value_matrix,
        expected=json.loads("""{
            "tablename": [
                {
                    "a": 1,
                    "b": 123.1,
                    "c": "a",
                    "dd": 1,
                    "e": 1
                },
                {
                    "a": 2,
                    "b": 2.2,
                    "c": "bb",
                    "dd": 2.2,
                    "e": 2.2
                },
                {
                    "a": 3,
                    "b": 3.3,
                    "c": "ccc",
                    "dd": 3,
                    "e": "cccc"
                }
            ]
        }
        """)
    ),
    Data(
        table="table name",
        header=header_list,
        value=value_matrix_with_none,
        expected=json.loads("""{
            "table name": [
                {
                    "a": 1,
                    "b": null,
                    "c": "a",
                    "dd": 1,
                    "e": null
                },
                {
                    "a": null,
                    "b": 2.2,
                    "c": null,
                    "dd": 2.2,
                    "e": 2.2
                },
                {
                    "a": 3,
                    "b": 3.3,
                    "c": "ccc",
                    "dd": null,
                    "e": "cccc"
                },
                {
                    "a": null,
                    "b": null,
                    "c": null,
                    "dd": null,
                    "e": null
                }
            ]
        }
        """)
    ),
    Data(
        table="table name",
        header=mix_header_list,
        value=mix_value_matrix,
        expected=json.loads("""{ "table name" : [
            {
                "bool": true,
                "c": "aa",
                "f": 1.1,
                "i": 1,
                "if": 1,
                "ifc": 1,
                "inf": "Infinity",
                "mix_num": 1.0,
                "nan": "NaN",
                "time": "2017-01-01 00:00:00"
            },
            {
                "bool": false,
                "c": "bbb",
                "f": 2.2,
                "i": 2,
                "if": 2.2,
                "ifc": 2.2,
                "inf": "Infinity",
                "mix_num": "Infinity",
                "nan": "NaN",
                "time": "2017-01-02 03:04:05+09:00"
            },
            {
                "bool": true,
                "c": "cccc",
                "f": 3.33,
                "i": 3,
                "if": -3,
                "ifc": "ccc",
                "inf": "Infinity",
                "mix_num": "NaN",
                "nan": "NaN",
                "time": "2017-01-01 00:00:00"
            }]}
        """)
    ),
]

exception_test_data_list = [
    Data(
        table="",
        header=[],
        value=[],
        expected=pytablewriter.EmptyTableDataError
    ),
    Data(
        table="",
        header=[],
        value=normal_test_data_list[0].value,
        expected=pytablewriter.EmptyHeaderError
    ),
]

table_writer_class = pytablewriter.JsonTableWriter


class Test_JsonTableWriter_write_new_line:

    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_JsonTableWriter_write_table:

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
        assert json.loads(out) == expected

    @pytest.mark.parametrize(["table", "header", "value", "expected"], [
        [data.table, data.header, data.value, data.expected]
        for data in exception_test_data_list
    ])
    def test_exception(self, capsys, table, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table()


class Test_JsonTableWriter_write_table_iter:

    @pytest.mark.parametrize(["table", "header", "value", "expected"], [
        [
            "tablename",
            ["ha", "hb", "hc"],
            value_matrix_iter,
            json.loads("""{ "tablename" : [
                {
                    "ha": 1,
                    "hb": 2,
                    "hc": 3
                },
                {
                    "ha": 11,
                    "hb": 12,
                    "hc": 13
                },
                {
                    "ha": 1,
                    "hb": 2,
                    "hc": 3
                },
                {
                    "ha": 11,
                    "hb": 12,
                    "hc": 13
                },
                {
                    "ha": 101,
                    "hb": 102,
                    "hc": 103
                },
                {
                    "ha": 1001,
                    "hb": 1002,
                    "hc": 1003
                }]}"""),
        ],
    ])
    def test_normal(self, capsys, table, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.header_list = header
        writer.value_matrix = value
        writer.iteration_length = len(value)
        writer.write_table_iter()

        out, _err = capsys.readouterr()
        assert json.loads(out) == expected

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
            writer.write_table_iter()
