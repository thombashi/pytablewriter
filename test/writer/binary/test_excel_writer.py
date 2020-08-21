"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import collections
import itertools
from decimal import Decimal

import pytest
from pytablereader import ExcelTableFileLoader
from tabledata import TableData

import pytablewriter as ptw

from ..._common import print_test_result
from ...data import headers, mix_header_list, mix_value_matrix, value_matrix, value_matrix_iter


try:
    import xlwt  # noqa: W0611

    HAS_XLWT = True
except ImportError:
    HAS_XLWT = False


inf = Decimal("Infinity")
nan = Decimal("NaN")

Data = collections.namedtuple("Data", "table header value expected")

normal_test_data_list = [
    Data(
        table="tablename",
        header=headers,
        value=value_matrix,
        expected=TableData(
            "tablename",
            ["a", "b", "c", "dd", "e"],
            [[1, 123.1, "a", 1, 1], [2, 2.2, "bb", 2.2, 2.2], [3, 3.3, "ccc", 3, "cccc"]],
        ),
    ),
    Data(
        table="tablename",
        header=headers,
        value=None,
        expected=TableData("tablename", ["a", "b", "c", "dd", "e"], []),
    ),
    Data(
        table="",
        header=mix_header_list,
        value=mix_value_matrix,
        expected=TableData(
            "Sheet1",
            ["i", "f", "c", "if", "ifc", "bool", "inf", "nan", "mix_num", "time"],
            [
                [1, "1.1", "aa", 1, 1, 1, inf, nan, 1, "2017-01-01T00:00:00"],
                [2, "2.2", "bbb", "2.2", "2.2", 0, inf, nan, inf, "2017-01-02 03:04:05+09:00"],
                [3, "3.33", "cccc", -3, "ccc", 1, inf, nan, nan, "2017-01-01T00:00:00"],
            ],
        ),
    ),
    Data(
        table="infnan",
        header=["inf", "nan"],
        value=[[inf, nan], ["inf", "nan"], ["INF", "NAN"], ["INFINITY", "inf"]],
        expected=TableData(
            "infnan", ["inf", "nan"], [[inf, nan], [inf, nan], [inf, nan], [inf, inf]]
        ),
    ),
    Data(
        table="line breaks",
        header=["a\nb", "\nc\n\nd\n", "e\r\nf"],
        value=[["v1\nv1", "v2\n\nv2", "v3\r\nv3"]],
        expected=TableData(
            "line breaks", ["a\nb", "\nc\n\nd\n", "e\r\nf"], [["v1\nv1", "v2\n\nv2", "v3\r\nv3"]]
        ),
    ),
]

invalid_test_data_list = [
    Data(table="", header=header, value=value, expected=ptw.EmptyTableDataError)
    for header, value in itertools.product([None, [], ""], [None, [], ""])
]

table_writer_class_list = [ptw.ExcelXlsTableWriter, ptw.ExcelXlsxTableWriter]


class Test_ExcelTableWriter_table_format:
    def test_normal(self):
        assert ptw.ExcelXlsTableWriter().table_format is ptw.TableFormat.EXCEL_XLSX


@pytest.mark.xfail(run=False)
class Test_ExcelTableWriter_write_table:
    @pytest.mark.parametrize(
        ["writer_class", "table", "header", "value", "expected"],
        [
            [writer_class, data.table, data.header, data.value, data.expected]
            for writer_class, data in itertools.product(
                table_writer_class_list, normal_test_data_list
            )
        ],
    )
    def test_normal(self, tmpdir, writer_class, table, header, value, expected):
        if writer_class == ptw.ExcelXlsTableWriter and not HAS_XLWT:
            pytest.skip()

        test_file_path = tmpdir.join("test.xlsx")

        writer = writer_class()
        writer.open(str(test_file_path))
        writer.make_worksheet(table)
        writer.headers = header
        writer.value_matrix = value
        writer.write_table()
        writer.close()

        for table_data in ExcelTableFileLoader(str(test_file_path)).load():
            expected_dump = ptw.dumps_tabledata(expected)
            actual_dump = ptw.dumps_tabledata(table_data)

            print_test_result(expected=expected_dump, actual=actual_dump)

            assert actual_dump == expected_dump

    @pytest.mark.parametrize(
        ["writer_class", "table", "header", "value", "expected"],
        [
            [writer_class, data.table, data.header, data.value, data.expected]
            for writer_class, data in itertools.product(
                table_writer_class_list, invalid_test_data_list
            )
        ],
    )
    def test_smoke_empty(self, tmpdir, writer_class, table, header, value, expected):
        if writer_class == ptw.ExcelXlsTableWriter and not HAS_XLWT:
            pytest.skip()

        test_file_path = tmpdir.join("test.xlsx")

        writer = writer_class()
        writer.open(str(test_file_path))
        writer.make_worksheet(table)
        writer.headers = header
        writer.value_matrix = value

        writer.write_table()

    @pytest.mark.parametrize(
        ["writer_class", "header", "value"],
        [
            [writer_class, data.header, data.value]
            for writer_class, data in itertools.product(
                table_writer_class_list, normal_test_data_list
            )
        ],
    )
    def test_exception_null_sheet(self, tmpdir, writer_class, header, value):
        if writer_class == ptw.ExcelXlsTableWriter and not HAS_XLWT:
            pytest.skip()

        test_file_path = tmpdir.join("test.xlsx")

        writer = writer_class()
        writer.open(str(test_file_path))
        writer.headers = header
        writer.value_matrix = value

        with pytest.raises(IOError):
            writer.write_table()


@pytest.mark.xfail(run=False)
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
                    "tablename",
                    ["ha", "hb", "hc"],
                    [
                        [1.0, 2.0, 3.0],
                        [11.0, 12.0, 13.0],
                        [1.0, 2.0, 3.0],
                        [11.0, 12.0, 13.0],
                        [101.0, 102.0, 103.0],
                        [1001.0, 1002.0, 1003.0],
                    ],
                ),
            ]
            for table_writer_class in table_writer_class_list
        ],
    )
    def test_normal(self, tmpdir, writer_class, table, header, value, expected):
        if writer_class == ptw.ExcelXlsTableWriter and not HAS_XLWT:
            pytest.skip()

        test_file_path = tmpdir.join("test.xlsx")

        writer = writer_class()
        writer.open(str(test_file_path))
        writer.make_worksheet(table)
        writer.headers = header
        writer.value_matrix = value
        writer.iteration_length = len(value)
        writer.write_table_iter()

        writer.close()
        assert writer.first_data_row == 1
        assert writer.last_data_row == 7

        for table_data in ExcelTableFileLoader(str(test_file_path)).load():
            assert table_data == expected

    @pytest.mark.parametrize(
        ["writer_class", "header", "value"],
        [
            [writer_class, data.header, data.value]
            for writer_class, data in itertools.product(
                table_writer_class_list, normal_test_data_list
            )
        ],
    )
    def test_exception_null_sheet(self, tmpdir, writer_class, header, value):
        if writer_class == ptw.ExcelXlsTableWriter and not HAS_XLWT:
            pytest.skip()

        test_file_path = tmpdir.join("test.xlsx")

        writer = writer_class()
        writer.open(str(test_file_path))
        writer.headers = header
        writer.value_matrix = value

        with pytest.raises(IOError):
            writer.write_table_iter()


@pytest.mark.xfail(run=False)
class Test_ExcelTableWriter_dump:
    def test_normal_single_sheet(self, tmpdir):
        for writer_class in table_writer_class_list:
            test_filepath = str(tmpdir.join("test.xlsx"))
            data = TableData(
                "tablename",
                ["ha", "hb", "hc"],
                [
                    [1.0, 2.0, 3.0],
                    [11.0, 12.0, 13.0],
                    [1.0, 2.0, 3.0],
                    [11.0, 12.0, 13.0],
                    [101.0, 102.0, 103.0],
                    [1001.0, 1002.0, 1003.0],
                ],
            )

            writer = writer_class()
            writer.from_tabledata(data)
            writer.dump(test_filepath)

            assert writer.first_data_row == 1
            assert writer.last_data_row == 7

            for expected in ExcelTableFileLoader(test_filepath).load():
                assert data == expected

    def test_normal_multi_sheet(self, tmpdir):
        for writer_class in table_writer_class_list:
            test_filepath = str(tmpdir.join("test.xlsx"))
            data_list = [
                TableData("first", ["ha1", "hb1", "hc1"], [[1.0, 2.0, 3.0], [11.0, 12.0, 13.0]]),
                TableData("second", ["ha2", "hb2", "hc2"], [[11.0, 12.0, 13.0], [1.0, 2.0, 3.0]]),
            ]

            writer = writer_class()

            for data in data_list:
                writer.from_tabledata(data)
                writer.dump(test_filepath, close_after_write=False)

            writer.close()

            for data, expected in zip(data_list, ExcelTableFileLoader(test_filepath).load()):
                assert data == expected


@pytest.mark.xfail(run=False)
class Test_ExcelTableWriter_dumps:
    def test_exception(self, tmpdir):
        for writer_class in table_writer_class_list:
            test_filepath = tmpdir.join("test.xlsx")

            writer = writer_class()
            writer.open(str(test_filepath))

            with pytest.raises(NotImplementedError):
                writer.dumps()
