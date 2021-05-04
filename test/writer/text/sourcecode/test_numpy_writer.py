"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import pytest

import pytablewriter as ptw

from ...._common import print_test_result
from ....data import (
    Data,
    headers,
    mix_header_list,
    mix_value_matrix,
    null_test_data_list,
    value_matrix,
    value_matrix_iter,
    value_matrix_with_none,
)


try:
    import numpy as np  # noqa: W0611

    SKIP_DATAFRAME_TEST = False
except ImportError:
    SKIP_DATAFRAME_TEST = True


normal_test_data_list = [
    Data(
        table="table-name ho'ge",
        indent=0,
        header=headers,
        value=value_matrix,
        expected="""table_name_ho_ge = np.array([
    ["a", "b", "c", "dd", "e"],
    [1, 123.1, "a", 1, 1],
    [2, 2.2, "bb", 2.2, 2.2],
    [3, 3.3, "ccc", 3, "cccc"],
])
""",
    ),
    Data(
        table="empty value",
        indent=0,
        header=headers,
        value=None,
        expected="""empty_value = np.array([
    ["a", "b", "c", "dd", "e"],
])
""",
    ),
    Data(
        table="table with%null-value",
        indent=0,
        header=headers,
        value=value_matrix_with_none,
        expected="""table_with_null_value = np.array([
    ["a", "b", "c", "dd", "e"],
    [1, None, "a", 1, None],
    [None, 2.2, None, 2.2, 2.2],
    [3, 3.3, "ccc", None, "cccc"],
    [None, None, None, None, None],
])
""",
    ),
    Data(
        table="mix data types",
        indent=0,
        header=mix_header_list,
        value=mix_value_matrix,
        expected="""mix_data_types = np.array([
    ["i", "f", "c", "if", "ifc", "bool", "inf", "nan", "mix_num", "time"],
    [1, 1.1, "aa", 1, 1, True, np.inf, np.nan, 1, dateutil.parser.parse("2017-01-01T00:00:00")],
    [2, 2.2, "bbb", 2.2, 2.2, False, np.inf, np.nan, np.inf, "2017-01-02 03:04:05+09:00"],
    [3, 3.33, "cccc", -3, "ccc", True, np.inf, np.nan, np.nan, dateutil.parser.parse("2017-01-01T00:00:00")],
])
""",
    ),
    Data(
        table="mix data types wo header",
        indent=0,
        header=None,
        value=mix_value_matrix,
        expected="""mix_data_types_wo_header = np.array([
    [1, 1.1, "aa", 1, 1, True, np.inf, np.nan, 1, dateutil.parser.parse("2017-01-01T00:00:00")],
    [2, 2.2, "bbb", 2.2, 2.2, False, np.inf, np.nan, np.inf, "2017-01-02 03:04:05+09:00"],
    [3, 3.33, "cccc", -3, "ccc", True, np.inf, np.nan, np.nan, dateutil.parser.parse("2017-01-01T00:00:00")],
])
""",
    ),
    Data(
        table="float-with-null",
        indent=0,
        header=["a", "b"],
        value=[
            ["0.03785679191278808", "826.21158713263"],
            [None, "826.21158713263"],
            [0.1, "1.0499675627886724"],
        ],
        expected="""float_with_null = np.array([
    ["a", "b"],
    [0.03785679191278808, 826.21158713263],
    [None, 826.21158713263],
    [0.1, 1.0499675627886724],
])
""",
    ),
]


table_writer_class = ptw.NumpyTableWriter


class Test_NumpyTableWriter_write_new_line:
    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()

        assert out == "\n"


class Test_NumpyTableWriter_write_table:
    @pytest.mark.parametrize(
        ["table", "indent", "header", "value", "expected"],
        [
            [data.table, data.indent, data.header, data.value, data.expected]
            for data in normal_test_data_list
        ],
    )
    def test_normal(self, capsys, table, indent, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.set_indent_level(indent)
        writer.headers = header
        writer.value_matrix = value
        writer.write_table()

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected

    @pytest.mark.parametrize(
        ["table", "indent", "header", "value", "expected"],
        [
            [data.table, data.indent, data.header, data.value, data.expected]
            for data in null_test_data_list
        ],
    )
    def test_exception_null(self, table, indent, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.set_indent_level(indent)
        writer.headers = header
        writer.value_matrix = value

        assert writer.dumps() == ""

    @pytest.mark.parametrize(
        ["table", "indent", "header", "value", "expected"],
        [
            [data.table, data.indent, data.header, data.value, data.expected]
            for data in [
                Data(
                    table=None,
                    indent=0,
                    header=headers,
                    value=value_matrix,
                    expected="",
                )
            ]
        ],
    )
    def test_exception(self, table, indent, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.set_indent_level(indent)
        writer.headers = header
        writer.value_matrix = value

        with pytest.raises(ptw.EmptyTableNameError):
            writer.write_table()


class Test_NumpyTableWriter_write_table_iter:
    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [
            [
                "tablename",
                ["ha", "hb", "hc"],
                value_matrix_iter,
                """tablename = np.array([
    ["ha", "hb", "hc"],
    [1, 2, 3],
    [11, 12, 13],
    [1, 2, 3],
    [11, 12, 13],
    [101, 102, 103],
    [1001, 1002, 1003],
])
""",
            ]
        ],
    )
    def test_normal(self, capsys, table, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.headers = header
        writer.value_matrix = value
        writer.iteration_length = len(value)
        writer.write_table_iter()

        out, _err = capsys.readouterr()

        assert out == expected

    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [[data.table, data.header, data.value, data.expected] for data in null_test_data_list],
    )
    def test_normal_empty(self, table, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.headers = header
        writer.value_matrix = value

        writer.write_table_iter()
