# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import collections
import json

import pytablewriter
import pytest

from .data import (
    float_header_list,
    float_value_matrix,
    header_list,
    mix_header_list,
    mix_value_matrix,
    value_matrix,
    value_matrix_iter,
    value_matrix_with_none,
)


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
        """)),
    Data(
        table="",
        header=header_list,
        value=None,
        expected=json.loads("[]")),
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
        """)),
    Data(
        table="with none values",
        header=header_list,
        value=value_matrix_with_none,
        expected=json.loads("""{
            "with none values": [
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
        """)),
    Data(
        table="mixed values",
        header=mix_header_list,
        value=mix_value_matrix,
        expected=json.loads("""{ "mixed values" : [
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
                "time": "2017-01-01T00:00:00"
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
                "time": "2017-01-01T00:00:00"
            }]}
        """)),
    Data(
        table="float",
        header=float_header_list,
        value=float_value_matrix,
        expected=json.loads("""{ "float" : [
{
    "a": 0.01,
    "b": 0.00125,
    "c": 0
},
{
    "a": 1,
    "b": 99.9,
    "c": 0.01
},
{
    "a": 1.2,
    "b": 999999.123,
    "c": 0.001
}]}

""")),
]

exception_test_data_list = [
    Data(
        table="",
        header=[],
        value=[],
        expected=pytablewriter.EmptyTableDataError),
    Data(
        table="",
        header=[],
        value=normal_test_data_list[0].value,
        expected=pytablewriter.EmptyHeaderError),
]

table_writer_class = pytablewriter.JsonTableWriter


class Test_JsonTableWriter_write_new_line(object):

    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_JsonTableWriter_write_table(object):

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

        print("[expected]\n{}".format(json.dumps(expected)))
        print("[actual]\n{}".format(out))

        assert json.loads(out) == expected

    @pytest.mark.parametrize(["table", "header", "value", "expected"], [
        [data.table, data.header, data.value, data.expected]
        for data in exception_test_data_list
    ])
    def test_exception(self, table, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table()


class Test_JsonTableWriter_write_table_iter(object):

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
        ])
    def test_exception(self, table, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table_iter()
