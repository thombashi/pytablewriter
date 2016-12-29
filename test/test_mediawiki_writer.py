# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import collections

import pytablewriter
import pytest

from .data import null_test_data_list
from .data import header_list
from .data import value_matrix
from .data import value_matrix_with_none
from .data import mix_header_list
from .data import mix_value_matrix
from .data import value_matrix_iter


Data = collections.namedtuple("Data", "table header value expected")

normal_test_data_list = [
    Data(
        table="test table",
        header=header_list,
        value=value_matrix,
        expected="""{| class="wikitable"
|+test table
! a
! b
! c
! dd
! e
|-
| style="text-align:right"| 1
| style="text-align:right"| 123.1
| a
| style="text-align:right"| 1.0
| style="text-align:right"| 1
|-
| style="text-align:right"| 2
| style="text-align:right"| 2.2
| bb
| style="text-align:right"| 2.2
| style="text-align:right"| 2.2
|-
| style="text-align:right"| 3
| style="text-align:right"| 3.3
| ccc
| style="text-align:right"| 3.0
| cccc
|}
"""),
    Data(
        table=None,
        header=header_list,
        value=None,
        expected="""{| class="wikitable"
! a
! b
! c
! dd
! e
|-
|}
"""),
    Data(
        table=None,
        header=["ho ge", "foo - bar"],
        value=[
            [1, "\n".join([" # a b c", "# h o g e"])],
            [2, "\n".join([" *hoge", "* abc"])],
            [3, "\n".join([" a * b", "a # b ## c ###"])],
            [3, "\n".join([" a # b", "a * b ** c ***"])],
        ],
        expected="""{| class="wikitable"
! ho ge
! foo - bar
|-
| style="text-align:right"| 1
| 
# a b c
# h o g e
|-
| style="text-align:right"| 2
| 
*hoge
* abc
|-
| style="text-align:right"| 3
|  a * b
a # b ## c ###
|-
| style="text-align:right"| 3
|  a # b
a * b ** c ***
|}
"""),
    Data(
        table=None,
        header=None,
        value=value_matrix,
        expected="""{| class="wikitable"
| style="text-align:right"| 1
| style="text-align:right"| 123.1
| a
| style="text-align:right"| 1.0
| style="text-align:right"| 1
|-
| style="text-align:right"| 2
| style="text-align:right"| 2.2
| bb
| style="text-align:right"| 2.2
| style="text-align:right"| 2.2
|-
| style="text-align:right"| 3
| style="text-align:right"| 3.3
| ccc
| style="text-align:right"| 3.0
| cccc
|}
"""),
    Data(
        table="test table",
        header=header_list,
        value=value_matrix_with_none,
        expected="""{| class="wikitable"
|+test table
! a
! b
! c
! dd
! e
|-
| style="text-align:right"| 1
| 
| a
| style="text-align:right"| 1.0
| 
|-
| 
| style="text-align:right"| 2.2
| 
| style="text-align:right"| 2.2
| style="text-align:right"| 2.2
|-
| style="text-align:right"| 3
| style="text-align:right"| 3.3
| ccc
| 
| cccc
|-
| 
| 
| 
| 
| 
|}
"""),
    Data(
        table="test table",
        header=mix_header_list,
        value=mix_value_matrix,
        expected="""{| class="wikitable"
|+test table
! i
! f
! c
! if
! ifc
! bool
! inf
! nan
! mix_num
! time
|-
| style="text-align:right"| 1
| style="text-align:right"| 1.10
| aa
| style="text-align:right"| 1.0
| style="text-align:right"| 1
| True
| Infinity
| NaN
| style="text-align:right"| 1
| 2017-01-01 00:00:00
|-
| style="text-align:right"| 2
| style="text-align:right"| 2.20
| bbb
| style="text-align:right"| 2.2
| style="text-align:right"| 2.2
| False
| Infinity
| NaN
| Infinity
| 2017-01-02 03:04:05+09:00
|-
| style="text-align:right"| 3
| style="text-align:right"| 3.33
| cccc
| style="text-align:right"| -3.0
| ccc
| True
| Infinity
| NaN
| NaN
| 2017-01-01 00:00:00
|}
"""),
]

table_writer_class = pytablewriter.MediaWikiTableWriter


class Test_MediaWikiTableWriter_write_new_line:

    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_MediaWikiTableWriter_write_table:

    @pytest.mark.parametrize(["table", "header", "value", "expected"], [
        [data.table, data.header, data.value, data.expected]
        for data in normal_test_data_list
    ])
    def test_normal(self, capsys, table, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.header_list = header
        writer.value_matrix = value
        writer.write_table()

        out, _err = capsys.readouterr()

        print("[expected]\n{}".format(expected))
        print("[actual]\n{}".format(out))

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
            writer.write_table()


def simple_write_callback(iter_count, iteration_length):
    import six

    six.print_("{:d}/{:d}".format(iter_count, iteration_length))


class Test_MediaWikiTableWriter_write_table_iter:

    @pytest.mark.parametrize(["table", "header", "value", "callback", "expected"], [
        [
            "tablename",
            ["ha", "hb", "hc"],
            value_matrix_iter,
            None,
            """{| class="wikitable"
|+tablename
! ha
! hb
! hc
|-
| style="text-align:right"| 1
| style="text-align:right"| 2
| style="text-align:right"| 3
|-
| style="text-align:right"| 11
| style="text-align:right"| 12
| style="text-align:right"| 13
|-
| style="text-align:right"| 1
| style="text-align:right"| 2
| style="text-align:right"| 3
|-
| style="text-align:right"| 11
| style="text-align:right"| 12
| style="text-align:right"| 13
|-
| style="text-align:right"| 101
| style="text-align:right"| 102
| style="text-align:right"| 103
|-
| style="text-align:right"| 1001
| style="text-align:right"| 1002
| style="text-align:right"| 1003
|}
""",
        ],
        [
            None,
            None,
            value_matrix_iter,
            simple_write_callback,
            """{| class="wikitable"
| style="text-align:right"| 1
| style="text-align:right"| 2
| style="text-align:right"| 3
|-
| style="text-align:right"| 11
| style="text-align:right"| 12
| style="text-align:right"| 13
|-
1/3
| style="text-align:right"| 1
| style="text-align:right"| 2
| style="text-align:right"| 3
|-
| style="text-align:right"| 11
| style="text-align:right"| 12
| style="text-align:right"| 13
|-
2/3
| style="text-align:right"| 101
| style="text-align:right"| 102
| style="text-align:right"| 103
|-
| style="text-align:right"| 1001
| style="text-align:right"| 1002
| style="text-align:right"| 1003
|}
3/3
""",
        ],
    ])
    def test_normal(self, capsys, table, header, value, callback, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.header_list = header
        writer.value_matrix = value
        writer.iteration_length = len(value)
        writer.write_callback = callback
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
