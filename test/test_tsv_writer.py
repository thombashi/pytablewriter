# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import collections
import itertools

import pytablewriter as ptw
import pytest

from .data import (
    header_list,
    value_matrix,
    value_matrix_with_none,
    mix_header_list,
    mix_value_matrix,
    value_matrix_iter
)


Data = collections.namedtuple("Data", "header value expected")

normal_test_data_list = [
    Data(
        header=mix_header_list,
        value=mix_value_matrix,
        expected=""""i"\t"f"\t"c"\t"if"\t"ifc"\t"bool"\t"inf"\t"nan"\t"mix_num"\t"time"
1\t1.10\t"aa"\t1.0\t"1"\tTrue\tInfinity\tNaN\t1\t"2017-01-01 00:00:00"
2\t2.20\t"bbb"\t2.2\t"2.2"\tFalse\tInfinity\tNaN\tInfinity\t"2017-01-02 03:04:05+09:00"
3\t3.33\t"cccc"\t-3.0\t"ccc"\tTrue\tInfinity\tNaN\tNaN\t"2017-01-01 00:00:00"
"""),
    Data(
        header=None,
        value=value_matrix,
        expected="""1\t123.1\t"a"\t1.0\t"1"
2\t2.2\t"bb"\t2.2\t"2.2"
3\t3.3\t"ccc"\t3.0\t"cccc"
"""),
]

exception_test_data_list = [
    Data(
        header=header,
        value=value,
        expected=ptw.EmptyTableDataError
    )
    for header, value in itertools.product([None, [], ""], [None, [], ""])
]

table_writer_class = ptw.TsvTableWriter


class Test_TsvTableWriter_write_new_line:

    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_TsvTableWriter_write_table:

    @pytest.mark.parametrize(["header", "value", "expected"], [
        [data.header, data.value, data.expected]
        for data in normal_test_data_list
    ])
    def test_normal(self, capsys, header, value, expected):
        writer = table_writer_class()
        writer.header_list = header
        writer.value_matrix = value
        writer.write_table()

        out, _err = capsys.readouterr()

        print("[expected]\n{}".format(expected))
        print("[actual]\n{}".format(out))

        assert out == expected

    @pytest.mark.parametrize(["header", "value", "expected"], [
        [data.header, data.value, data.expected]
        for data in exception_test_data_list
    ])
    def test_exception(self, capsys, header, value, expected):
        writer = table_writer_class()
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table()
