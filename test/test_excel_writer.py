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
        table="tablename",
        header=header_list,
        value=None,
        expected=TableData(
            "tablename",
            ["a", "b", "c", "dd", "e"],
            [
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

    @pytest.mark.parametrize(["writer_class", "table", "header", "expected"], [
        [
            table_writer_class,
            "tablename",
            ["ha", "hb", "hc"],
            TableData(
                table_name=u'tablename',
                header_list=[u'ha', u'hb', u'hc'],
                record_list=[
                    [1.0, 2.0, 3.0],
                    [11.0, 12.0, 13.0],
                    [1.0, 2.0, 3.0],
                    [11.0, 12.0, 13.0],
                    [101.0, 102.0, 103.0],
                    [1001.0, 1002.0, 1003.0],
                ]),
        ]
        for table_writer_class in table_writer_class_list
    ])
    def test_normal_multiple(
            self, tmpdir, writer_class, table, header, expected):
        test_file_path = tmpdir.join("test.xlsx")

        writer = writer_class()
        writer.open_workbook(str(test_file_path))
        writer.make_worksheet(table)
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

        writer.close()
        assert writer.first_data_row == 1
        assert writer.last_data_row == 7

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
