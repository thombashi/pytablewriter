# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import collections
try:
    import json
except ImportError:
    import simplejson as json

import pytablewriter
import pytest

from .data import header_list
from .data import value_matrix


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
]

table_writer_class = pytablewriter.JsonTableWriter


class Test_JsonTableWriter_write_new_line:

    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, err = capsys.readouterr()
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

        out, err = capsys.readouterr()
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
