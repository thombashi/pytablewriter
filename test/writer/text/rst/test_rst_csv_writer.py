"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from textwrap import dedent

import pytest

import pytablewriter

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
    vut_style_tabledata,
    vut_styles,
)
from .._common import regexp_ansi_escape


normal_test_data_list = [
    Data(
        table="table name",
        indent=0,
        header=headers,
        value=value_matrix,
        expected=dedent(
            """\
            .. csv-table:: table name
                :header: "a", "b", "c", "dd", "e"
                :widths: 3, 5, 5, 4, 6

                1, 123.1, "a", 1.0, 1
                2, 2.2, "bb", 2.2, 2.2
                3, 3.3, "ccc", 3.0, "cccc"
            """
        ),
    ),
    Data(
        table="",
        indent=0,
        header=headers,
        value=None,
        expected=dedent(
            """\
            .. csv-table:: 
                :header: "a", "b", "c", "dd", "e"
                :widths: 3, 3, 3, 4, 3

            """
        ),
    ),
    Data(
        table=None,
        indent=0,
        header=None,
        value=value_matrix,
        expected=dedent(
            """\
            .. csv-table:: 
                :widths: 1, 5, 5, 3, 6

                1, 123.1, "a", 1.0, 1
                2, 2.2, "bb", 2.2, 2.2
                3, 3.3, "ccc", 3.0, "cccc"
            """
        ),
    ),
    Data(
        table="",
        indent=1,
        header=headers,
        value=value_matrix,
        expected="""    .. csv-table:: 
        :header: "a", "b", "c", "dd", "e"
        :widths: 3, 5, 5, 4, 6

        1, 123.1, "a", 1.0, 1
        2, 2.2, "bb", 2.2, 2.2
        3, 3.3, "ccc", 3.0, "cccc"
""",
    ),
    Data(
        table="table name",
        indent=0,
        header=headers,
        value=value_matrix_with_none,
        expected=dedent(
            """\
            .. csv-table:: table name
                :header: "a", "b", "c", "dd", "e"
                :widths: 3, 3, 5, 4, 6

                1, , "a", 1.0, 
                , 2.2, , 2.2, 2.2
                3, 3.3, "ccc", , "cccc"
                , , , , 
            """
        ),
    ),
    Data(
        table="table name",
        indent=0,
        header=mix_header_list,
        value=mix_value_matrix,
        expected=dedent(
            """\
            .. csv-table:: table name
                :header: "i", "f", "c", "if", "ifc", "bool", "inf", "nan", "mix_num", "time"
                :widths: 3, 4, 6, 4, 5, 6, 8, 5, 9, 27

                1, 1.10, "aa", 1.0, 1, True, Infinity, NaN, 1, 2017-01-01T00:00:00
                2, 2.20, "bbb", 2.2, 2.2, False, Infinity, NaN, Infinity, "2017-01-02 03:04:05+09:00"
                3, 3.33, "cccc", -3.0, "ccc", True, Infinity, NaN, NaN, 2017-01-01T00:00:00
            """
        ),
    ),
]

table_writer_class = pytablewriter.RstCsvTableWriter


class Test_RstCsvTableWriter_write_new_line:
    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_RstCsvTableWriter_write_table:
    @pytest.mark.parametrize(
        ["table", "indent", "header", "value", "expected"],
        [
            [data.table, data.indent, data.header, data.value, data.expected]
            for data in normal_test_data_list
        ],
    )
    def test_normal(self, table, indent, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.set_indent_level(indent)
        writer.headers = header
        writer.value_matrix = value

        out = writer.dumps()
        print_test_result(expected=expected, actual=out)

        assert out == expected

    def test_normal_styles(self):
        writer = table_writer_class()
        writer.from_tabledata(vut_style_tabledata)
        writer.column_styles = vut_styles

        expected = dedent(
            """\
            .. csv-table:: style test
                :header: "none", "empty", "tiny", "small", "medium", "large", "null w/ bold", "L bold", "S italic", "L bold italic"
                :widths: 6, 7, 6, 7, 8, 7, 14, 8, 10, 15

                111, 111, 111, 111, "111", 111, , **111**, *111*, **111**
                1234, 1234, 1234, 1234, "1,234", 1 234, , **1234**, *1234*, **1234**
            """
        )
        out = writer.dumps()
        print_test_result(expected=expected, actual=out)

        assert regexp_ansi_escape.search(out)
        assert regexp_ansi_escape.sub("", out) == expected

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

        assert writer.dumps() == ""
        assert str(writer) == ""


class Test_RstCsvTableWriter_write_table_iter:
    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [
            [
                "tablename",
                ["ha", "hb", "hc"],
                value_matrix_iter,
                dedent(
                    """\
                    .. csv-table:: tablename
                        :header: "ha", "hb", "hc"
                        :widths: 5, 5, 5

                        1, 2, 3
                        11, 12, 13
                        1, 2, 3
                        11, 12, 13
                        101, 102, 103
                        1001, 1002, 1003
                    """
                ),
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

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected

    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [[data.table, data.header, data.value, data.expected] for data in null_test_data_list],
    )
    def test_normal_smoke(self, table, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.headers = header
        writer.value_matrix = value

        writer.write_table_iter()
