"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import collections
import itertools
import json

import pytest

import pytablewriter as ptw

from ..._common import print_test_result
from ...data import float_header_list, float_value_matrix, headers, value_matrix


Data = collections.namedtuple("Data", "header value expected_list")

normal_test_data_list = [
    Data(
        header=headers,
        value=value_matrix,
        expected_list=[
            {"a": 1, "b": 123.1, "c": "a", "dd": 1, "e": 1},
            {"a": 2, "b": 2.2, "c": "bb", "dd": 2.2, "e": 2.2},
            {"a": 3, "b": 3.3, "c": "ccc", "dd": 3, "e": "cccc"},
        ],
    ),
    Data(
        header=headers,
        value=[
            ["1", "", "a", "1", None],
            [None, 2.2, None, "2.2", 2.2],
            [None, None, None, None, None],
            [3, 3.3, "ccc", None, "cccc"],
            [None, None, None, None, None],
        ],
        expected_list=[
            {"a": 1, "b": "", "c": "a", "dd": 1, "e": "null"},
            {"a": "null", "b": 2.2, "c": "null", "dd": 2.2, "e": 2.2},
            {"a": "null", "b": "null", "c": "null", "dd": "null", "e": "null"},
            {"a": 3, "b": 3.3, "c": "ccc", "dd": "null", "e": "cccc"},
            {"a": "null", "b": "null", "c": "null", "dd": "null", "e": "null"},
        ],
    ),
    Data(
        header=float_header_list,
        value=float_value_matrix,
        expected_list=[
            {"a": 0.01, "b": 0.00125, "c": 0},
            {"a": 1, "b": 99.9, "c": 0.01},
            {"a": 1.2, "b": 999999.123, "c": 0.001},
        ],
    ),
]
exception_test_data_list = [
    Data(header=header, value=value, expected_list=ptw.EmptyTableDataError)
    for header, value in itertools.product([None, [], ""], [None, [], ""])
] + [Data(header=None, value=value_matrix, expected_list=ptw.EmptyHeaderError)]
table_writer_class = ptw.JsonLinesTableWriter


class Test_JsonLinesTableWriter_write_new_line:
    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_JsonLinesTableWriter_write_table:
    @pytest.mark.parametrize(
        ["header", "value", "expected_list"],
        [[data.header, data.value, data.expected_list] for data in normal_test_data_list],
    )
    def test_normal(self, capsys, header, value, expected_list):
        writer = table_writer_class()
        writer.headers = header
        writer.value_matrix = value
        writer.write_table()

        out, err = capsys.readouterr()
        for actual, expected in zip(out.splitlines(), expected_list):
            print_test_result(expected=expected, actual=actual, error=err)
            assert json.loads(actual) == expected

    @pytest.mark.parametrize(
        ["header", "value", "expected_list"],
        [[data.header, data.value, data.expected_list] for data in exception_test_data_list],
    )
    def test_exception(self, header, value, expected_list):
        writer = table_writer_class()
        writer.headers = header
        writer.value_matrix = value

        with pytest.raises(expected_list):
            writer.write_table()
