"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import collections
from collections import OrderedDict
from decimal import Decimal

import pytest
from pytablereader import SqliteFileLoader
from sqliteschema import SQLiteSchemaExtractor
from tabledata import TableData

import pytablewriter as ptw

from ..._common import print_test_result
from ...data import headers, mix_header_list, mix_value_matrix, value_matrix, value_matrix_iter


inf = Decimal("Infinity")
nan = None

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
        table="mix_data",
        header=mix_header_list,
        value=mix_value_matrix,
        expected=TableData(
            "mix_data",
            ["i", "f", "c", "if", "ifc", "bool", "inf", "nan", "mix_num", "time"],
            [
                [1, "1.1", "aa", 1, 1, 1, inf, nan, 1, "2017-01-01 00:00:00"],
                [2, "2.2", "bbb", "2.2", "2.2", 0, inf, nan, inf, "2017-01-02 03:04:05+09:00"],
                [3, "3.33", "cccc", -3, "ccc", 1, inf, nan, nan, "2017-01-01 00:00:00"],
            ],
        ),
    ),
    Data(
        table="infnan",
        header=["inf", "nan"],
        value=[[inf, float("nan")], ["inf", "nan"], ["INF", "NAN"], ["INFINITY", "inf"]],
        expected=TableData(
            "infnan", ["inf", "nan"], [[inf, nan], [inf, nan], [inf, nan], [inf, inf]]
        ),
    ),
    Data(
        table="line breaks",
        header=["a\nb", "\nc\n\nd\n", "e\r\nf"],
        value=[["v1\nv1", "v2\n\nv2", "v3\r\nv3"]],
        expected=TableData(
            "line_breaks", ["a_b", "_c__d_", "e__f"], [["v1\nv1", "v2\n\nv2", "v3\r\nv3"]]
        ),
    ),
    Data(
        table="empty header",
        header=[],
        value=value_matrix,
        expected=TableData(
            "empty_header",
            ["A", "B", "C", "D", "E"],
            [[1, 123.1, "a", 1, 1], [2, 2.2, "bb", 2.2, 2.2], [3, 3.3, "ccc", 3, "cccc"]],
        ),
    ),
]

empty_test_data_list = [
    Data(table="dummy", header=[], value=[], expected=None),
    Data(table="dummy", header=headers, value=[], expected=None),
]
exception_test_data_list = [
    Data(table="", header=headers, value=value_matrix, expected=ptw.EmptyTableNameError),
]


@pytest.mark.xfail(run=False)
class Test_SqliteTableWriter_write_table:
    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [[data.table, data.header, data.value, data.expected] for data in normal_test_data_list],
    )
    def test_normal(self, tmpdir, table, header, value, expected):
        test_file_path = tmpdir.join("test.sqlite")

        writer = ptw.SqliteTableWriter()
        writer.open(str(test_file_path))
        writer.table_name = table
        writer.headers = header
        writer.value_matrix = value
        writer.write_table()
        writer.close()

        for table_data in SqliteFileLoader(str(test_file_path)).load():
            expected_dump = ptw.dumps_tabledata(expected)
            actual_dump = ptw.dumps_tabledata(table_data)

            print_test_result(expected=expected_dump, actual=actual_dump)

            assert actual_dump == expected_dump

    def test_normal_type_hints(self, tmpdir):
        test_file_path = str(tmpdir.join("test.sqlite"))

        writer = ptw.SqliteTableWriter()
        writer.open(test_file_path)
        writer.table_name = "hoge"
        writer.headers = ["a", "b"]
        writer.value_matrix = [[1, 2], [11, 12]]
        writer.type_hints = [ptw.String]
        writer.write_table()
        writer.close()

        schema = SQLiteSchemaExtractor(test_file_path).fetch_database_schema_as_dict()

        assert schema[writer.table_name] == [
            OrderedDict(
                [
                    ("Field", "a"),
                    ("Index", False),
                    ("Type", "TEXT"),
                    ("Null", "YES"),
                    ("Key", ""),
                    ("Default", "NULL"),
                    ("Extra", ""),
                ]
            ),
            OrderedDict(
                [
                    ("Field", "b"),
                    ("Index", False),
                    ("Type", "INTEGER"),
                    ("Null", "YES"),
                    ("Key", ""),
                    ("Default", "NULL"),
                    ("Extra", ""),
                ]
            ),
        ]

    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [[data.table, data.header, data.value, data.expected] for data in empty_test_data_list],
    )
    def test_smoke_empty(self, tmpdir, table, header, value, expected):
        writer = ptw.SqliteTableWriter()
        writer.open(":memory:")
        writer.table_name = table
        writer.headers = header
        writer.value_matrix = value

        writer.write_table()

    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [[data.table, data.header, data.value, data.expected] for data in exception_test_data_list],
    )
    def test_exception(self, table, header, value, expected):
        writer = ptw.SqliteTableWriter()
        writer.open(":memory:")
        writer.table_name = table
        writer.headers = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table()


@pytest.mark.xfail(run=False)
class Test_SqliteTableWriter_dump:
    def test_normal_single_table(self, tmpdir):
        test_filepath = str(tmpdir.join("test.sqlite"))
        data = TableData(
            "tablename", ["ha", "hb", "hc"], [[1.0, 2.0, 3.0], [11.0, 12.0, 13.0], [1.0, 2.0, 3.0]]
        )

        writer = ptw.SqliteTableWriter()
        writer.from_tabledata(data)
        writer.dump(test_filepath)

        for expected in SqliteFileLoader(test_filepath).load():
            assert data == expected

    def test_normal_multi_table(self, tmpdir):
        test_filepath = str(tmpdir.join("test.sqlite"))
        data_list = [
            TableData("first", ["ha1", "hb1", "hc1"], [[1.0, 2.0, 3.0], [11.0, 12.0, 13.0]]),
            TableData("second", ["ha2", "hb2", "hc2"], [[11.0, 12.0, 13.0], [1.0, 2.0, 3.0]]),
        ]

        writer = ptw.SqliteTableWriter()

        for data in data_list:
            writer.from_tabledata(data)
            writer.dump(test_filepath, close_after_write=False)

        writer.close()

        count = 0
        for data, expected in zip(data_list, SqliteFileLoader(test_filepath).load()):
            assert data == expected
            count += 1

        assert count == 2


@pytest.mark.xfail(run=False)
class Test_SqliteTableWriter_write_table_iter:
    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [
            [
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
        ],
    )
    def test_normal(self, tmpdir, table, header, value, expected):
        test_file_path = tmpdir.join("test.sqlite")

        writer = ptw.SqliteTableWriter()
        writer.open(str(test_file_path))
        writer.table_name = table
        writer.headers = header
        writer.value_matrix = value
        writer.iteration_length = len(value)
        writer.write_table_iter()

        writer.close()

        for table_data in SqliteFileLoader(str(test_file_path)).load():
            assert table_data == expected


@pytest.mark.xfail(run=False)
class Test_SqliteTableWriter_dumps:
    def test_exception(self, tmpdir):
        writer = ptw.SqliteTableWriter()
        writer.open(":memory:")

        with pytest.raises(NotImplementedError):
            writer.dumps()
