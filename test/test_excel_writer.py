# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import collections

import pytablewriter
import pytest
import simplesqlite.loader as sloader
from simplesqlite.loader.data import TableData

from .data import header_list
from .data import value_matrix


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
            ])
    ),
    Data(
        table="",
        header=header_list,
        value=value_matrix,
        expected=TableData(
            "Sheet1",
            ["a", "b", "c", "dd", "e"],
            [
                [1, 123.1, "a", 1,   1],
                [2, 2.2, "bb", 2.2, 2.2],
                [3, 3.3, "ccc", 3,   "cccc"],
            ])
    ),
]

invalid_test_data_list = [
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
    Data(
        table="",
        header=normal_test_data_list[0].header,
        value=[],
        expected=pytablewriter.EmptyValueError
    ),
    Data(
        table="",
        header=normal_test_data_list[0].header,
        value=None,
        expected=pytablewriter.EmptyValueError
    ),
]

table_writer_class = pytablewriter.ExcelTableWriter


class Test_ExcelTableWriter_write_table:

    @pytest.mark.parametrize(["table", "header", "value", "expected"], [
        [data.table, data.header, data.value, data.expected]
        for data in normal_test_data_list
    ])
    def test_normal(self, tmpdir, table, header, value, expected):
        test_file_path = tmpdir.join("test.xlsx")

        writer = table_writer_class()
        writer.open_workbook(str(test_file_path))
        writer.make_worksheet(table)
        writer.header_list = header
        writer.value_matrix = value
        writer.write_table()
        writer.close()

        loader = sloader.ExcelTableFileLoader(str(test_file_path))

        for tabledata in loader.load():
            assert tabledata == expected

    @pytest.mark.parametrize(["table", "header", "value", "expected"], [
        [data.table, data.header, data.value, data.expected]
        for data in invalid_test_data_list
    ])
    def test_exception(self, tmpdir, table, header, value, expected):
        test_file_path = tmpdir.join("test.xlsx")

        writer = table_writer_class()
        writer.open_workbook(str(test_file_path))
        writer.make_worksheet(table)
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table()

    @pytest.mark.parametrize(["table", "header", "value", "expected"], [
        [data.table, data.header, data.value, data.expected]
        for data in normal_test_data_list
    ])
    def test_exception_null_sheet(self, tmpdir, table, header, value, expected):
        test_file_path = tmpdir.join("test.xlsx")

        writer = table_writer_class()
        writer.open_workbook(str(test_file_path))
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(IOError):
            writer.write_table()
