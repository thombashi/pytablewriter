# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import collections
from decimal import Decimal
import io
import itertools

import pytest

import pytablewriter as ptw

from .data import (
    float_header_list,
    float_value_matrix,
    header_list,
    mix_header_list,
    mix_value_matrix,
    value_matrix,
    value_matrix_iter,
    value_matrix_with_none,
)


Data = collections.namedtuple("Data", "col_delim header value expected")

normal_test_data_list = [
    Data(
        col_delim=",",
        header=header_list,
        value=value_matrix,
        expected=""""a","b","c","dd","e"
1,123.1,"a",1,1
2,2.2,"bb",2.2,2.2
3,3.3,"ccc",3,"cccc"
"""),
    Data(
        col_delim=",",
        header=header_list,
        value=[],
        expected=""""a","b","c","dd","e"
"""),
    Data(
        col_delim=",",
        header=[],
        value=value_matrix,
        expected="""1,123.1,"a",1,1
2,2.2,"bb",2.2,2.2
3,3.3,"ccc",3,"cccc"
"""),
    Data(
        col_delim="\t",
        header=None,
        value=value_matrix,
        expected="""1\t123.1\t"a"\t1\t1
2\t2.2\t"bb"\t2.2\t2.2
3\t3.3\t"ccc"\t3\t"cccc"
"""),
    Data(
        col_delim=",",
        header=header_list,
        value=value_matrix_with_none,
        expected=""""a","b","c","dd","e"
1,,"a",1,
,2.2,,2.2,2.2
3,3.3,"ccc",,"cccc"
,,,,
"""),
    Data(
        col_delim=",",
        header=mix_header_list,
        value=mix_value_matrix,
        expected=""""i","f","c","if","ifc","bool","inf","nan","mix_num","time"
1,1.1,"aa",1,1,True,Infinity,NaN,1,"2017-01-01T00:00:00"
2,2.2,"bbb",2.2,2.2,False,Infinity,NaN,Infinity,"2017-01-02 03:04:05+09:00"
3,3.33,"cccc",-3,"ccc",True,Infinity,NaN,NaN,"2017-01-01T00:00:00"
"""),
    Data(
        col_delim=",",
        header=float_header_list,
        value=float_value_matrix,
        expected=""""a","b","c"
0.01,0.00125,0
1,99.9,0.01
1.2,999999.123,0.001
"""),
    Data(
        col_delim=",",
        header=["a\nb", "c\n\nd", "e\r\nf"],
        value=[["v1\nv1", "v2\n\nv2", "v3\r\nv3"]],
        expected=""""a b","c d","e f"
"v1 v1","v2 v2","v3 v3"
"""),
]

exception_test_data_list = [
    Data(
        col_delim=",",
        header=header,
        value=value,
        expected=ptw.EmptyTableDataError)
    for header, value in itertools.product([None, [], ""], [None, [], ""])
]

table_writer_class = ptw.CsvTableWriter


class Test_CsvTableWriter_write_new_line(object):

    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_CsvTableWriter_from_csv(object):

    __CSV_TEXT_INPUT = """"a","b","c","dd","e"
1,1.1,"a",1.0,
2,2.2,,2.2,"2.2"
3,3.3,"ccc",,"cc\ncc"
"""

    __CSV_EXPECTED = """"a","b","c","dd","e"
1,1.1,"a",1,
2,2.2,,2.2,2.2
3,3.3,"ccc",,"cc cc"
"""

    def test_normal_from_text(self, capsys):
        writer = table_writer_class()
        writer.from_csv(self.__CSV_TEXT_INPUT)
        writer.write_table()

        out, _err = capsys.readouterr()

        assert writer.table_name == "csv1"
        assert writer.header_list == ["a", "b", "c", "dd", "e"]
        assert writer.value_matrix == [
            [1, Decimal('1.1'), 'a', Decimal('1.0'), ''],
            [2, Decimal('2.2'), '', Decimal('2.2'), Decimal('2.2')],
            [3, Decimal('3.3'), 'ccc', '', 'cc\ncc']
        ]

        print("[expected]\n{}".format(self.__CSV_EXPECTED))
        print("[actual]\n{}".format(out))

        assert out == self.__CSV_EXPECTED

    def test_normal_from_file(self, capsys, tmpdir):
        file_path = str(tmpdir.join("test_data.csv"))
        with io.open(file_path, "w", encoding="utf-8") as f:
            f.write(self.__CSV_TEXT_INPUT)

        writer = table_writer_class()
        writer.from_csv(file_path)
        writer.write_table()

        out, _err = capsys.readouterr()

        assert writer.table_name == "test_data"
        assert writer.header_list == ["a", "b", "c", "dd", "e"]
        assert writer.value_matrix == [
            [1, Decimal('1.1'), 'a', Decimal('1'), ''],
            [2, Decimal('2.2'), '', Decimal('2.2'), Decimal('2.2')],
            [3, Decimal('3.3'), 'ccc', '', 'cc\ncc']
        ]

        print("[expected]\n{}".format(self.__CSV_EXPECTED))
        print("[actual]\n{}".format(out))

        assert out == self.__CSV_EXPECTED


class Test_CsvTableWriter_write_table(object):

    @pytest.mark.parametrize(["col_delim", "header", "value", "expected"], [
        [data.col_delim, data.header, data.value, data.expected]
        for data in normal_test_data_list
    ])
    def test_normal(self, capsys, col_delim, header, value, expected):
        writer = table_writer_class()
        writer.column_delimiter = col_delim
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
    def test_exception(self, header, value, expected):
        writer = table_writer_class()
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table()


class Test_CsvTableWriter_write_table_iter(object):

    @pytest.mark.parametrize(["table", "header", "value", "expected"], [
        [
            "tablename",
            ["ha", "hb", "hc"],
            value_matrix_iter,
            """"ha","hb","hc"
1,2,3
11,12,13
1,2,3
11,12,13
101,102,103
1001,1002,1003
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
        ["header", "value", "expected"],
        [
            [data.header, data.value, data.expected]
            for data in exception_test_data_list
        ])
    def test_exception(self, header, value, expected):
        writer = table_writer_class()
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table_iter()
