"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import collections
from textwrap import dedent

import pytest

import pytablewriter as ptw

from ..._common import print_test_result
from ...data import (
    headers,
    mix_header_list,
    mix_value_matrix,
    null_test_data_list,
    value_matrix,
    value_matrix_iter,
    value_matrix_with_none,
)


Data = collections.namedtuple("Data", "table header value expected")

normal_test_data_list = [
    Data(
        table="test table",
        header=headers,
        value=value_matrix,
        expected=dedent(
            """\
            [cols=">1, >5, <3, >3, <4" options="header"]
            .test table
            |===
            ^|a
            ^|b
            ^|c
            ^|dd
            ^|e

            |1
            |123.1
            |a
            |1.0
            >|1

            |2
            |2.2
            |bb
            |2.2
            >|2.2

            |3
            |3.3
            |ccc
            |3.0
            |cccc
            |===
            """
        ),
    ),
    Data(
        table=None,
        header=headers,
        value=None,
        expected=dedent(
            """\
            [cols="<1, <1, <1, <2, <1" options="header"]
            |===
            ^|a
            ^|b
            ^|c
            ^|dd
            ^|e

            |===
            """
        ),
    ),
    Data(
        table=None,
        header=["ho ge", "foo - bar"],
        value=[
            [1, "\n".join([" # a b c", "# h o g e"])],
            [2, "\n".join([" *hoge", "* abc"])],
            [3, "\n".join([" a * b", "a # b ## c ###"])],
            [3, "\n".join([" a # b", "a * b ** c ***"])],
        ],
        expected=dedent(
            """\
            [cols=">5, <21" options="header"]
            |===
            ^|ho ge
            ^|foo - bar

            |1
            | # a b c
            # h o g e

            |2
            | *hoge
            * abc

            |3
            | a * b
            a # b ## c ###

            |3
            | a # b
            a * b ** c ***
            |===
            """
        ),
    ),
    Data(
        table=None,
        header=None,
        value=value_matrix,
        expected=dedent(
            """\
            [cols=">1, >5, <3, >3, <4" options="header"]
            |===
            |1
            |123.1
            |a
            |1.0
            >|1

            |2
            |2.2
            |bb
            |2.2
            >|2.2

            |3
            |3.3
            |ccc
            |3.0
            |cccc
            |===
            """
        ),
    ),
    Data(
        table="values with none",
        header=headers,
        value=value_matrix_with_none,
        expected=dedent(
            """\
            [cols=">1, >3, <3, >3, <4" options="header"]
            .values with none
            |===
            ^|a
            ^|b
            ^|c
            ^|dd
            ^|e

            |1
            <|
            |a
            |1.0
            |

            <|
            |2.2
            |
            |2.2
            >|2.2

            |3
            |3.3
            |ccc
            <|
            |cccc

            <|
            <|
            |
            <|
            |
            |===
            """
        ),
    ),
    Data(
        table="MIX VALUES",
        header=mix_header_list,
        value=mix_value_matrix,
        expected=dedent(
            """\
            [cols=">1, >4, <4, >4, <3, <5, <8, <3, >8, <25" options="header"]
            .MIX VALUES
            |===
            ^|i
            ^|f
            ^|c
            ^|if
            ^|ifc
            ^|bool
            ^|inf
            ^|nan
            ^|mix_num
            ^|time

            |1
            |1.10
            |aa
            |1.0
            >|1
            |True
            |Infinity
            |NaN
            |1
            |2017-01-01T00:00:00

            |2
            |2.20
            |bbb
            |2.2
            >|2.2
            |False
            |Infinity
            |NaN
            <|Infinity
            |2017-01-02 03:04:05+09:00

            |3
            |3.33
            |cccc
            |-3.0
            |ccc
            |True
            |Infinity
            |NaN
            <|NaN
            |2017-01-01T00:00:00
            |===
            """
        ),
    ),
]

table_writer_class = ptw.AsciiDocTableWriter


class Test_AsciiDocTableWriter_write_new_line:
    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_AsciiDocTableWriter_write_table:
    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [[data.table, data.header, data.value, data.expected] for data in normal_test_data_list],
    )
    def test_normal(self, capsys, table, header, value, expected):
        writer = table_writer_class(table_name=table, headers=header, value_matrix=value)
        writer.write_table()

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected
        assert writer.dumps() == expected
        assert str(writer) == expected

    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [[data.table, data.header, data.value, data.expected] for data in null_test_data_list],
    )
    def test_normal_empty(self, table, header, value, expected):
        writer = table_writer_class(table_name=table, headers=header, value_matrix=value)

        assert writer.dumps() == ""


def simple_write_callback(iter_count, iteration_length):
    print(f"{iter_count:d}/{iteration_length:d}")


class Test_AsciiDocTableWriter_write_table_iter:
    @pytest.mark.parametrize(
        ["table", "header", "value", "callback", "expected"],
        [
            [
                "iteration write",
                ["ha", "hb", "hc"],
                value_matrix_iter,
                lambda a, b: None,
                dedent(
                    """\
                    [cols=">3, >3, >3" options="header"]
                    .iteration write
                    |===
                    ^|ha
                    ^|hb
                    ^|hc

                    |1
                    |2
                    |3

                    |11
                    |12
                    |13

                    |1
                    |2
                    |3

                    |11
                    |12
                    |13

                    |101
                    |102
                    |103

                    |1001
                    |1002
                    |1003
                    |===
                    """
                ),
            ],
            [
                None,
                None,
                value_matrix_iter,
                simple_write_callback,
                dedent(
                    """\
                    [cols=">3, >3, >3" options="header"]
                    |===
                    |1
                    |2
                    |3

                    |11
                    |12
                    |13

                    1/3
                    |1
                    |2
                    |3

                    |11
                    |12
                    |13

                    2/3
                    |101
                    |102
                    |103

                    |1001
                    |1002
                    |1003
                    |===
                    3/3
                    """
                ),
            ],
        ],
    )
    def test_normal(self, capsys, table, header, value, callback, expected):
        writer = table_writer_class(
            table_name=table,
            headers=header,
            value_matrix=value,
            iteration_length=len(value),
            write_callback=callback,
        )
        writer.write_table_iter()

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)
        assert out == expected

    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [[data.table, data.header, data.value, data.expected] for data in null_test_data_list],
    )
    def test_smoke_empty(self, table, header, value, expected):
        writer = table_writer_class(table_name=table, headers=header, value_matrix=value)

        writer.write_table_iter()
