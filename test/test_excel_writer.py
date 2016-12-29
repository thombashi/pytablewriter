# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import collections
from decimal import Decimal
import itertools

import pytablewriter as ptw
import pytest
import pytablereader as ptr
from pytablereader import TableData

from .data import (
    header_list,
    value_matrix,
    mix_header_list,
    mix_value_matrix,
    value_matrix_iter
)


inf = Decimal('Infinity')
nan = Decimal('NaN')

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
            []
        )
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
                    1, "1.1", 'aa', 1, 1, 'True', inf,
                    nan, 1, '2017-01-01T00:00:00',
                ],
                [
                    2, "2.2", 'bbb', "2.2", "2.2", 'False', inf, nan,
                    inf, '2017-01-02 03:04:05+09:00',
                ],
                [
                    3, "3.33", 'cccc', -3, 'ccc', 'True', inf,
                    nan, nan, '2017-01-01T00:00:00',
                ],
            ])
    ),
]

invalid_test_data_list = [
    Data(
        table="",
        header=header,
        value=value,
        expected=ptw.EmptyTableDataError
    )
    for header, value in itertools.product([None, [], ""], [None, [], ""])
]

table_writer_class_list = [
    ptw.ExcelXlsTableWriter,
    ptw.ExcelXlsxTableWriter,
]


class Test_ExcelTableWriter_write_new_line:

    @pytest.mark.parametrize(["writer_class"], [
        [writer_class] for writer_class in table_writer_class_list
    ])
    def test_smoke(self, writer_class):
        writer = writer_class()
        writer.write_null_line()


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

        loader = ptr.ExcelTableFileLoader(str(test_file_path))

        for tabledata in loader.load():
            print("expected: {}".format(ptw.dump_tabledata(expected)))
            print("actual: {}".format(ptw.dump_tabledata(tabledata)))

            assert tabledata == expected

    @pytest.mark.parametrize(
        ["writer_class", "table", "header", "value", "expected"],
        [
            [writer_class, data.table, data.header, data.value, data.expected]
            for writer_class, data in itertools.product(
                table_writer_class_list, invalid_test_data_list)
        ]
    )
    def test_exception(
            self, tmpdir, writer_class, table, header, value, expected):
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


class Test_ExcelTableWriter_write_table_iter:

    @pytest.mark.parametrize(
        ["writer_class", "table", "header", "value", "expected"],
        [
            [
                table_writer_class,
                "tablename",
                ["ha", "hb", "hc"],
                value_matrix_iter,
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
    def test_normal(
            self, tmpdir, writer_class, table, header, value, expected):
        test_file_path = tmpdir.join("test.xlsx")

        writer = writer_class()
        writer.open_workbook(str(test_file_path))
        writer.make_worksheet(table)
        writer.header_list = header
        writer.value_matrix = value
        writer.iteration_length = len(value)
        writer.write_table_iter()

        writer.close()
        assert writer.first_data_row == 1
        assert writer.last_data_row == 7

        loader = ptr.ExcelTableFileLoader(str(test_file_path))

        for tabledata in loader.load():
            assert tabledata == expected

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
            writer.write_table_iter()
