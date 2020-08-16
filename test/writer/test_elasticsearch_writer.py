"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import collections
import datetime
import json
from decimal import Decimal

import elasticsearch
import pytest

import pytablewriter as ptw

from .._common import print_test_result
from ..data import headers, value_matrix


inf = Decimal("Infinity")
nan = None

Data = collections.namedtuple("Data", "table header value expected")

empty_test_data_list = [
    Data(table="dummy", header=[], value=[], expected=None),
    Data(table="dummy", header=headers, value=[], expected=None),
]
exception_test_data_list = [
    Data(table="", header=headers, value=value_matrix, expected=ptw.EmptyTableNameError),
]

table_writer_class = ptw.ElasticsearchWriter


class Test_ElasticsearchWriter__get_mappings:
    def test_normal(self):
        writer = table_writer_class()
        writer.table_name = "es mappings"
        writer.headers = [
            "text",
            "byte",
            "short",
            "int",
            "long",
            "float",
            "date",
            "bool",
            "ip",
            "none",
            "inf",
            "nan",
        ]
        writer.value_matrix = [
            [
                "This is XXX",
                100,
                10000,
                2000000000,
                200000000000,
                0.1,
                datetime.datetime(2017, 1, 3, 4, 5, 6),
                True,
                "127.0.0.1",
                None,
                float("inf"),
                float("nan"),
            ],
            [
                "What is it",
                -10,
                -1000,
                -200000000,
                -20000000000,
                100.1,
                datetime.datetime(2017, 1, 3, 4, 5, 6),
                False,
                "::1",
                None,
                float("inf"),
                float("nan"),
            ],
        ]

        # mappings w/o type hint ---
        writer._preprocess()
        mappings = writer._get_mappings()
        expected_mappings = {
            "mappings": {
                "table": {
                    "properties": {
                        "text": {"type": "text"},
                        "byte": {"type": "byte"},
                        "short": {"type": "short"},
                        "int": {"type": "integer"},
                        "long": {"type": "long"},
                        "float": {"type": "double"},
                        "date": {"type": "date", "format": "date_optional_time"},
                        "bool": {"type": "boolean"},
                        "ip": {"type": "text"},
                        "none": {"type": "keyword"},
                        "inf": {"type": "keyword"},
                        "nan": {"type": "keyword"},
                    }
                }
            }
        }

        print_test_result(expected=expected_mappings, actual=json.dumps(mappings, indent=4))
        assert mappings == expected_mappings

        # mappings w/ type hint ---
        writer.type_hints = [None, None, None, None, None, None, None, None, ptw.IpAddress]
        writer._preprocess()
        mappings = writer._get_mappings()
        expected_mappings = {
            "mappings": {
                "table": {
                    "properties": {
                        "text": {"type": "text"},
                        "byte": {"type": "byte"},
                        "short": {"type": "short"},
                        "int": {"type": "integer"},
                        "long": {"type": "long"},
                        "float": {"type": "double"},
                        "date": {"type": "date", "format": "date_optional_time"},
                        "bool": {"type": "boolean"},
                        "ip": {"type": "ip"},
                        "none": {"type": "keyword"},
                        "inf": {"type": "keyword"},
                        "nan": {"type": "keyword"},
                    }
                }
            }
        }

        print_test_result(expected=expected_mappings, actual=json.dumps(mappings, indent=4))
        assert mappings == expected_mappings

        # body ---
        body = list(writer._get_body())
        expected_body = [
            {
                "text": "This is XXX",
                "byte": 100,
                "short": 10000,
                "int": 2000000000,
                "long": 200000000000,
                "float": Decimal("0.1"),
                "date": "2017-01-03T04:05:06",
                "bool": True,
                "ip": "127.0.0.1",
                "none": None,
                "inf": "Infinity",
                "nan": "NaN",
            },
            {
                "text": "What is it",
                "byte": -10,
                "short": -1000,
                "int": -200000000,
                "long": -20000000000,
                "float": Decimal("100.1"),
                "date": "2017-01-03T04:05:06",
                "bool": False,
                "ip": "::1",
                "none": None,
                "inf": "Infinity",
                "nan": "NaN",
            },
        ]

        print_test_result(expected=expected_body, actual=body)
        assert body == expected_body


class Test_ElasticsearchWriter_write_table:
    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [[data.table, data.header, data.value, data.expected] for data in empty_test_data_list],
    )
    def test_smoke_empty(self, table, header, value, expected):
        writer = table_writer_class()
        writer.stream = elasticsearch.Elasticsearch()
        writer.table_name = table
        writer.headers = header
        writer.value_matrix = value

        writer.write_table()

    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [[data.table, data.header, data.value, data.expected] for data in exception_test_data_list],
    )
    def test_exception(self, table, header, value, expected):
        writer = table_writer_class()
        writer.stream = elasticsearch.Elasticsearch()
        writer.table_name = table
        writer.headers = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table()
