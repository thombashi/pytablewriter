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


normal_test_data_list = [
    Data(
        table="Table-Name ho'ge",
        indent=0,
        header=headers,
        value=value_matrix,
        expected="""table_name_ho_ge = [
    ["a", "b", "c", "dd", "e"],
    [1, 123.1, "a", 1, 1],
    [2, 2.2, "bb", 2.2, 2.2],
    [3, 3.3, "ccc", 3, "cccc"],
]
""",
    ),
    Data(
        table="TABLENAME",
        indent=0,
        header=headers,
        value=None,
        expected="""tablename = [
    ["a", "b", "c", "dd", "e"],
]
""",
    ),
    Data(
        table="TableName",
        indent=1,
        header=headers,
        value=value_matrix,
        expected="""    tablename = [
        ["a", "b", "c", "dd", "e"],
        [1, 123.1, "a", 1, 1],
        [2, 2.2, "bb", 2.2, 2.2],
        [3, 3.3, "ccc", 3, "cccc"],
    ]
""",
    ),
    Data(
        table="TABLE Name",
        indent=0,
        header=headers,
        value=value_matrix_with_none,
        expected="""table_name = [
    ["a", "b", "c", "dd", "e"],
    [1, None, "a", 1, None],
    [None, 2.2, None, 2.2, 2.2],
    [3, 3.3, "ccc", None, "cccc"],
    [None, None, None, None, None],
]
""",
    ),
    Data(
        table="tablename",
        indent=0,
        header=mix_header_list,
        value=mix_value_matrix,
        expected="""tablename = [
    ["i", "f", "c", "if", "ifc", "bool", "inf", "nan", "mix_num", "time"],
    [1, 1.1, "aa", 1, 1, True, float("inf"), float("nan"), 1, dateutil.parser.parse("2017-01-01T00:00:00")],
    [2, 2.2, "bbb", 2.2, 2.2, False, float("inf"), float("nan"), float("inf"), "2017-01-02 03:04:05+09:00"],
    [3, 3.33, "cccc", -3, "ccc", True, float("inf"), float("nan"), float("nan"), dateutil.parser.parse("2017-01-01T00:00:00")],
]
""",
    ),
    Data(
        table="quoted values",
        indent=0,
        header=['"quote"', '"abc efg"'],
        value=[['"1', '"abc"'], ['"-1', '"efg"']],
        expected="""quoted_values = [
    ["quote", "abc efg"],
    [1, "abc"],
    [-1, "efg"],
]
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
        expected="""float_with_null = [
    ["a", "b"],
    [0.03785679191278808, 826.21158713263],
    [None, 826.21158713263],
    [0.1, 1.0499675627886724],
]
""",
    ),
]

table_writer_class = ptw.PythonCodeTableWriter


class Test_PythonCodeTableWriter_write_new_line:
    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_PythonCodeTableWriter_write_table:
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

    def test_normal_not_strict(self, capsys):
        writer = table_writer_class()
        writer.table_name = "tablename"
        writer.headers = mix_header_list
        writer.value_matrix = mix_value_matrix
        writer.write_table()

        expected = """tablename = [
    ["i", "f", "c", "if", "ifc", "bool", "inf", "nan", "mix_num", "time"],
    [1, 1.1, "aa", 1, 1, True, float("inf"), float("nan"), 1, dateutil.parser.parse("2017-01-01T00:00:00")],
    [2, 2.2, "bbb", 2.2, 2.2, False, float("inf"), float("nan"), float("inf"), "2017-01-02 03:04:05+09:00"],
    [3, 3.33, "cccc", -3, "ccc", True, float("inf"), float("nan"), float("nan"), dateutil.parser.parse("2017-01-01T00:00:00")],
]
"""

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
    def test_normal_empty(self, table, indent, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.set_indent_level(indent)
        writer.headers = header
        writer.value_matrix = value

        assert writer.dumps() == expected
        assert str(writer) == expected

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
                    expected=ptw.EmptyTableNameError,
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


class Test_PythonCodeTableWriter_write_table_iter:
    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [
            [
                "tablename",
                ["ha", "hb", "hc"],
                value_matrix_iter,
                """tablename = [
    ["ha", "hb", "hc"],
    [1, 2, 3],
    [11, 12, 13],
    [1, 2, 3],
    [11, 12, 13],
    [101, 102, 103],
    [1001, 1002, 1003],
]
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
    def test_smoke(self, table, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.headers = header
        writer.value_matrix = value

        writer.write_table_iter()
