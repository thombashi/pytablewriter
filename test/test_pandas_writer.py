# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pytablewriter
import pytest

from .data import (
    Data,
    null_test_data_list,
    header_list,
    value_matrix,
    value_matrix_with_none,
    mix_header_list,
    mix_value_matrix,
    value_matrix_iter
)

try:
    import numpy
    import pandas
    SKIP_DATAFRAME_TEST = False
except ImportError:
    SKIP_DATAFRAME_TEST = True


normal_test_data_list = [
    Data(
        table="table-name ho'ge",
        indent=0,
        header=header_list,
        value=value_matrix,
        expected="""table_name_ho_ge = pandas.DataFrame([
    [1, 123.1, "a", 1.0, "1"],
    [2, 2.2, "bb", 2.2, "2.2"],
    [3, 3.3, "ccc", 3.0, "cccc"],
])
table_name_ho_ge.columns = [
    "a",
    "b",
    "c",
    "dd",
    "e",
]
"""),
    Data(
        table="tablename",
        indent=0,
        header=header_list,
        value=None,
        expected="""tablename = pandas.DataFrame([
])
"""),
    Data(
        table="table with%null-value",
        indent=0,
        header=header_list,
        value=value_matrix_with_none,
        expected="""table_with_null_value = pandas.DataFrame([
    [1, None, "a", 1.0, None],
    [None, 2.2, None, 2.2, "2.2"],
    [3, 3.3, "ccc", None, "cccc"],
    [None, None, None, None, None],
])
table_with_null_value.columns = [
    "a",
    "b",
    "c",
    "dd",
    "e",
]
"""),
    Data(
        table="tablename",
        indent=0,
        header=mix_header_list,
        value=mix_value_matrix,
        expected="""tablename = pandas.DataFrame([
    [1, 1.10, "aa", 1.0, "1", True, numpy.inf, numpy.nan, 1, dateutil.parser.parse("2017-01-01T00:00:00")],
    [2, 2.20, "bbb", 2.2, "2.2", False, numpy.inf, numpy.nan, numpy.inf, dateutil.parser.parse("2017-01-02T03:04:05+0900")],
    [3, 3.33, "cccc", -3.0, "ccc", True, numpy.inf, numpy.nan, numpy.nan, dateutil.parser.parse("2017-01-01T00:00:00")],
])
tablename.columns = [
    "i",
    "f",
    "c",
    "if",
    "ifc",
    "bool",
    "inf",
    "nan",
    "mix_num",
    "time",
]
"""),
]

exception_test_data_list = [
    Data(
        table="dummy",
        indent=normal_test_data_list[0].indent,
        header=[],
        value=[],
        expected=pytablewriter.EmptyTableDataError
    ),
    Data(
        table="dummy",
        indent=normal_test_data_list[0].indent,
        header=[],
        value=normal_test_data_list[0].value,
        expected=pytablewriter.EmptyHeaderError
    ),
    Data(
        table="dummy",
        indent=normal_test_data_list[0].indent,
        header=None,
        value=normal_test_data_list[0].value,
        expected=pytablewriter.EmptyHeaderError
    ),
    Data(
        table="",
        indent=normal_test_data_list[0].indent,
        header=normal_test_data_list[0].header,
        value=normal_test_data_list[0].value,
        expected=pytablewriter.EmptyTableNameError
    ),
]

table_writer_class = pytablewriter.PandasDataFrameWriter


class Test_PandasDataFrameWriter_write_new_line:

    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_PandasDataFrameWriter_write_table:

    @pytest.mark.parametrize(
        ["table", "indent", "header", "value", "expected"],
        [
            [data.table, data.indent, data.header, data.value, data.expected]
            for data in normal_test_data_list
        ]
    )
    def test_normal(self, capsys, table, indent, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.set_indent_level(indent)
        writer.header_list = header
        writer.value_matrix = value
        writer.write_table()

        out, _err = capsys.readouterr()

        print("[expected]\n{}".format(expected))
        print("[actual]\n{}".format(out))

        assert out == expected

    @pytest.mark.parametrize(
        ["table", "indent", "header", "value", "expected"],
        [
            [data.table, data.indent, data.header, data.value, data.expected]
            for data in exception_test_data_list
        ]
    )
    def test_exception(self, capsys, table, indent, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.set_indent_level(indent)
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table()


class Test_PandasDataFrameWriter_write_table_iter:

    @pytest.mark.parametrize(["table", "header", "value", "expected"], [
        [
            "tablename",
            ["ha", "hb", "hc"],
            value_matrix_iter,
            """tablename = pandas.DataFrame([
    [1, 2, 3],
    [11, 12, 13],
    [1, 2, 3],
    [11, 12, 13],
    [101, 102, 103],
    [1001, 1002, 1003],
])
tablename.columns = [
    "ha",
    "hb",
    "hc",
]
""",
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
        assert out == expected

    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [
            [data.table, data.header, data.value, data.expected]
            for data in null_test_data_list
        ]
    )
    def test_exception(self, capsys, table, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table_iter()


@pytest.mark.skipif("SKIP_DATAFRAME_TEST is True")
class Test_PandasDataFrameWriter_from_dataframe:

    @pytest.mark.parametrize(["table", "header", "value", "expected"], [
        [
            "tablename",
            ["ha", "hb", "hc"],
            value_matrix_iter,
            """tablename = pandas.DataFrame([
    [1, 1.10, "aa", 1.0, "1", True, numpy.inf, numpy.nan, 1, dateutil.parser.parse("2017-01-01T00:00:00")],
    [2, 2.20, "bbb", 2.2, "2.2", False, numpy.inf, numpy.nan, numpy.inf, dateutil.parser.parse("2017-01-02T03:04:05+0900")],
    [3, 3.33, "cccc", -3.0, "ccc", True, numpy.inf, numpy.nan, numpy.nan, dateutil.parser.parse("2017-01-01T00:00:00")],
])
tablename.columns = [
    "i",
    "f",
    "c",
    "if",
    "ifc",
    "bool",
    "inf",
    "nan",
    "mix_num",
    "time",
]
""",
        ],
    ])
    def test_normal(self, capsys, table, header, value, expected):
        import dateutil

        df = pandas.DataFrame([
            [1, 1.10, "aa", 1.0, "1", True, numpy.inf, numpy.nan,
                1, dateutil.parser.parse("2017-01-01T00:00:00")],
            [2, 2.20, "bbb", 2.2, "2.2", False, numpy.inf, numpy.nan,
                numpy.inf, dateutil.parser.parse("2017-01-02T03:04:05+0900")],
            [3, 3.33, "cccc", -3.0, "ccc", True, numpy.inf, numpy.nan,
                numpy.nan, dateutil.parser.parse("2017-01-01T00:00:00")],
        ])
        df.columns = [
            "i",
            "f",
            "c",
            "if",
            "ifc",
            "bool",
            "inf",
            "nan",
            "mix_num",
            "time",
        ]

        writer = table_writer_class()
        writer.table_name = table
        writer.from_dataframe(df)
        writer.write_table()

        out, _err = capsys.readouterr()

        print("[expected]\n{}".format(expected))
        print("[actual]\n{}".format(out))

        assert out == expected
