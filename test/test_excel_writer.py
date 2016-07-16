# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import collections
import itertools

import pytablewriter
import pytest
import simplesqlite.loader as sloader
from simplesqlite.loader.data import TableData

from .data import header_list
from .data import value_matrix
from .data import mix_header_list
from .data import mix_value_matrix


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
    Data(
        table="",
        header=mix_header_list,
        value=mix_value_matrix,
        expected=TableData(
            "Sheet1",
            [
                'i', 'f', 'c', 'if', 'ifc', 'bool',
                'inf', 'nan', 'mix_num', 'time',
            ],
            [
                [
                    1.0, 1.1, 'aa', 1.0, 1.0, 'True', 'Inf',
                    'NaN', 1.0, '2017-01-01T00:00:00',
                ],
                [
                    2.0, 2.2, 'bbb', 2.2, 2.2, 'False', 'Inf', 'NaN',
                    'Inf', '2017-01-02T03:04:05+0900',
                ],
                [
                    3.0, 3.33, 'cccc', -3.0, 'ccc', 'True', 'Inf',
                    'NaN', 'NaN', '2017-01-01T00:00:00',
                ],
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

table_writer_class_list = [
    pytablewriter.ExcelXlsTableWriter,
    pytablewriter.ExcelXlsxTableWriter,
]


class Test_ExcelTableWriter_write_table:

    @pytest.mark.parametrize(
        ["writer_class", "table", "header", "value", "expected"],
        [
            [writer_class, data.table, data.header, data.value, data.expected]
            for writer_class, data in itertools.product(
                table_writer_class_list, normal_test_data_list)
        ]
    )
    def test_normal(
            self, tmpdir, writer_class, table, header, value, expected):
        test_file_path = tmpdir.join("test.xlsx")

        writer = writer_class()
        writer.open_workbook(str(test_file_path))
        writer.make_worksheet(table)
        writer.header_list = header
        writer.value_matrix = value
        writer.write_table()
        writer.close()

        loader = sloader.ExcelTableFileLoader(str(test_file_path))

        for tabledata in loader.load():
            assert tabledata == expected

    @pytest.mark.parametrize(
        ["writer_class", "table", "header", "value", "expected"],
        [
            [writer_class, data.table, data.header, data.value, data.expected]
            for writer_class, data in itertools.product(
                table_writer_class_list, invalid_test_data_list)
        ]
    )
    def test_exception(self, tmpdir, writer_class, table, header, value, expected):
        test_file_path = tmpdir.join("test.xlsx")

        writer = writer_class()
        writer.open_workbook(str(test_file_path))
        writer.make_worksheet(table)
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table()

    @pytest.mark.parametrize(
        ["writer_class", "table", "header", "value", "expected"],
        [
            [writer_class, data.table, data.header, data.value, data.expected]
            for writer_class, data in itertools.product(
                table_writer_class_list, normal_test_data_list)
        ]
    )
    def test_exception_null_sheet(
            self, tmpdir, writer_class, table, header, value, expected):
        test_file_path = tmpdir.join("test.xlsx")

        writer = writer_class()
        writer.open_workbook(str(test_file_path))
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(IOError):
            writer.write_table()
