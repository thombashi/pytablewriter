# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import collections
import datetime
from decimal import Decimal
import json
import platform

import pytest
import six

import pytablewriter as ptw
from tabledata import TableData

from .data import (
    header_list,
    value_matrix,
    mix_header_list,
    mix_value_matrix,
)


inf = Decimal('Infinity')
nan = None

Data = collections.namedtuple("Data", "table header value expected")

normal_test_data_list = [
    Data(
        table="tablename",
        header=header_list,
        value=value_matrix,
        expected=TableData(
            "tablename",
            ["a", "b", "c", "dd", "e"],
            [
                [1, 123.1, "a", 1,   1],
                [2, 2.2, "bb", 2.2, 2.2],
                [3, 3.3, "ccc", 3,   "cccc"],
            ])),
    Data(
        table="mix_data",
        header=mix_header_list,
        value=mix_value_matrix,
        expected=TableData(
            "mix_data",
            [
                'i', 'f', 'c', 'if', 'ifc', 'bool',
                'inf', 'nan', 'mix_num', 'time',
            ],
            [
                [
                    1, "1.1", 'aa', 1, 1, 1, inf,
                    nan, 1, '2017-01-01T00:00:00',
                ],
                [
                    2, "2.2", 'bbb', "2.2", "2.2", 0, inf, nan,
                    inf, '2017-01-02 03:04:05+09:00',
                ],
                [
                    3, "3.33", 'cccc', -3, 'ccc', 1, inf,
                    nan, nan, '2017-01-01T00:00:00',
                ],
            ])),
    Data(
        table="infnan",
        header=["inf", "nan"],
        value=[
            [inf, float("nan")],
            ["inf", "nan"],
            ["INF", "NAN"],
            ["INFINITY", "inf"],
        ],
        expected=TableData(
            "infnan",
            ["inf", "nan"],
            [
                [inf, nan],
                [inf, nan],
                [inf, nan],
                [inf, inf],
            ])),
]

exception_test_data_list = [
    Data(
        table="",
        header=header_list,
        value=value_matrix,
        expected=ptw.EmptyTableNameError),
    Data(
        table="dummy",
        header=[],
        value=[],
        expected=ptw.EmptyTableDataError),
    Data(
        table="dummy",
        header=header_list,
        value=[],
        expected=ptw.EmptyValueError),
]

table_writer_class = ptw.ElasticsearchWriter


class Test_ElasticsearchWriter__get_mappings(object):

    @pytest.mark.skipif("platform.system() == 'Windows' and six.PY2")
    def test_normal(self):
        writer = table_writer_class()
        writer.table_name = "es mappings"
        writer.header_list = [
            "str", "byte", "short", "int", "long", "float",
            "date", "bool", "ip", "none", "inf", "nan",
        ]
        writer.value_matrix = [
            [
                "abc", 100, 10000, 2000000000, 200000000000, 0.1,
                datetime.datetime(2017, 1, 3, 4, 5, 6), True, "127.0.0.1",
                None, float("inf"), float("nan"),
            ],
            [
                "def", -10, -1000, -200000000, -20000000000, 100.1,
                datetime.datetime(2017, 1, 3, 4, 5, 6), False, "::1",
                None, float("inf"), float("nan"),
            ],
        ]

        # mappings w/o type hint ---
        writer._preprocess()
        mappings = writer._get_mappings()
        expected_mappings = {
            "mappings": {
                "table": {
                    "properties": {
                        "str": {"type": "string"},
                        "byte": {"type": "byte"},
                        "short": {"type": "short"},
                        "int": {"type": "integer"},
                        "long": {"type": "long"},
                        "float": {"type": "double"},
                        "date": {
                            "type": "date",
                            "format": "date_optional_time"
                        },
                        "bool": {"type": "boolean"},
                        "ip": {"type": "string"},
                        "none": {"type": "string"},
                        "inf": {"type": "keyword"},
                        "nan": {"type": "keyword"},
                    }
                }
            }
        }

        print("[expected]\n{}\n".format(expected_mappings))
        print("[actual]\n{}\n".format(json.dumps(mappings, indent=4)))
        assert mappings == expected_mappings

        # mappings w/ type hint ---
        writer.type_hint_list = [
            None, None, None, None, None, None, None, None, ptw.IpAddress]
        writer._preprocess()
        mappings = writer._get_mappings()
        expected_mappings = {
            "mappings": {
                "table": {
                    "properties": {
                        "str": {"type": "string"},
                        "byte": {"type": "byte"},
                        "short": {"type": "short"},
                        "int": {"type": "integer"},
                        "long": {"type": "long"},
                        "float": {"type": "double"},
                        "date": {
                            "type": "date",
                            "format": "date_optional_time"
                        },
                        "bool": {"type": "boolean"},
                        "ip": {"type": "ip"},
                        "none": {"type": "string"},
                        "inf": {"type": "keyword"},
                        "nan": {"type": "keyword"},
                    }
                }
            }
        }

        print("[expected]\n{}\n".format(expected_mappings))
        print("[actual]\n{}\n".format(json.dumps(mappings, indent=4)))
        assert mappings == expected_mappings

        # body ---
        body = list(writer._get_body())
        expected_body = [
            {
                'str': 'abc',
                'byte': 100, 'short': 10000, 'int': 2000000000,
                'long': 200000000000,
                'float': Decimal('0.1'),
                'date': '2017-01-03T04:05:06',
                'bool': True,
                'ip': '127.0.0.1',
                'none': None,
                'inf': 'Infinity',
                'nan': 'NaN',
            },
            {
                'str': 'def',
                'byte': -10, 'short': -1000, 'int': -200000000,
                'long': -20000000000,
                'float': Decimal('100.1'),
                'date': '2017-01-03T04:05:06',
                'bool': False,
                'ip': '::1',
                'none': None,
                'inf': 'Infinity',
                'nan': 'NaN',
            },
        ]

        print("[expected]\n{}\n".format(expected_body))
        print("[actual]\n{}\n".format(body))
        assert body == expected_body


class Test_ElasticsearchWriter_write_table(object):

    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [
            [data.table, data.header, data.value, data.expected]
            for data in exception_test_data_list
        ])
    def test_exception(self, table, header, value, expected):
        import elasticsearch

        writer = table_writer_class()
        writer.stream = elasticsearch.Elasticsearch()
        writer.table_name = table
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table()
