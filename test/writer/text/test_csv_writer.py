"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import collections
import itertools
from textwrap import dedent

import pytest

import pytablewriter as ptw

from ..._common import print_test_result
from ...data import (
    float_header_list,
    float_value_matrix,
    headers,
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
        header=headers,
        value=value_matrix,
        expected=dedent(
            """\
            "a","b","c","dd","e"
            1,123.1,"a",1,1
            2,2.2,"bb",2.2,2.2
            3,3.3,"ccc",3,"cccc"
            """
        ),
    ),
    Data(
        col_delim=",",
        header=headers,
        value=[],
        expected=dedent(
            """\
            "a","b","c","dd","e"
            """
        ),
    ),
    Data(
        col_delim=",",
        header=[],
        value=value_matrix,
        expected=dedent(
            """\
            1,123.1,"a",1,1
            2,2.2,"bb",2.2,2.2
            3,3.3,"ccc",3,"cccc"
            """
        ),
    ),
    Data(
        col_delim="\t",
        header=None,
        value=value_matrix,
        expected=dedent(
            """\
            1\t123.1\t"a"\t1\t1
            2\t2.2\t"bb"\t2.2\t2.2
            3\t3.3\t"ccc"\t3\t"cccc"
            """
        ),
    ),
    Data(
        col_delim=",",
        header=headers,
        value=value_matrix_with_none,
        expected=dedent(
            """\
            "a","b","c","dd","e"
            1,,"a",1,
            ,2.2,,2.2,2.2
            3,3.3,"ccc",,"cccc"
            ,,,,
            """
        ),
    ),
    Data(
        col_delim=",",
        header=mix_header_list,
        value=mix_value_matrix,
        expected=dedent(
            """\
            "i","f","c","if","ifc","bool","inf","nan","mix_num","time"
            1,1.1,"aa",1,1,True,Infinity,NaN,1,"2017-01-01T00:00:00"
            2,2.2,"bbb",2.2,2.2,False,Infinity,NaN,Infinity,"2017-01-02 03:04:05+09:00"
            3,3.33,"cccc",-3,"ccc",True,Infinity,NaN,NaN,"2017-01-01T00:00:00"
            """
        ),
    ),
    Data(
        col_delim=",",
        header=float_header_list,
        value=float_value_matrix,
        expected=dedent(
            """\
            "a","b","c"
            0.01,0.00125,0
            1,99.9,0.01
            1.2,999999.123,0.001
            """
        ),
    ),
    Data(
        col_delim=",",
        header=["a\nb", "c\n\nd", "e\r\nf"],
        value=[["v1\nv1", "v2\n\nv2", "v3\r\nv3"]],
        expected=dedent(
            """\
            "a b","c  d","e f"
            "v1 v1","v2  v2","v3 v3"
            """
        ),
    ),
]

exception_test_data_list = [
    Data(col_delim=",", header=header, value=value, expected=ptw.EmptyTableDataError)
    for header, value in itertools.product([None, [], ""], [None, [], ""])
]

table_writer_class = ptw.CsvTableWriter


class Test_CsvTableWriter_table_format:
    def test_normal(self):
        assert table_writer_class().table_format is ptw.TableFormat.CSV


class Test_CsvTableWriter_write_new_line:
    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_CsvTableWriter_from_csv:

    __CSV_TEXT_INPUT = dedent(
        """\
        "a","b","c","dd","e"
        1,1.1,"a",1.0,
        2,2.2,,2.2,"2.2"
        3,3.3,"ccc",,"cc\ncc"
        """
    )

    __CSV_EXPECTED = dedent(
        """\
        "a","b","c","dd","e"
        1,1.1,"a",1,
        2,2.2,,2.2,2.2
        3,3.3,"ccc",,"cc cc"
        """
    )

    def test_normal_from_text(self, capsys):
        writer = table_writer_class()
        writer.from_csv(self.__CSV_TEXT_INPUT)
        writer.write_table()

        out, _err = capsys.readouterr()

        assert writer.table_name == ""
        assert writer.headers == ["a", "b", "c", "dd", "e"]

        print_test_result(expected=self.__CSV_EXPECTED, actual=out)

        assert out == self.__CSV_EXPECTED

    def test_normal_from_file(self, capsys, tmpdir):
        file_path = str(tmpdir.join("test_data.csv"))
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(self.__CSV_TEXT_INPUT)

        writer = table_writer_class()
        writer.from_csv(file_path)
        writer.write_table()

        out, _err = capsys.readouterr()

        assert writer.table_name == "test_data"
        assert writer.headers == ["a", "b", "c", "dd", "e"]

        print_test_result(expected=self.__CSV_EXPECTED, actual=out)

        assert out == self.__CSV_EXPECTED


class Test_CsvTableWriter_write_table:
    @pytest.mark.parametrize(
        ["col_delim", "header", "value", "expected"],
        [
            [data.col_delim, data.header, data.value, data.expected]
            for data in normal_test_data_list
        ],
    )
    def test_normal(self, capsys, col_delim, header, value, expected):
        writer = table_writer_class(column_delimiter=col_delim, headers=header, value_matrix=value)
        writer.write_table()

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)
        assert out == expected
        assert writer.dumps() == expected
        assert str(writer) == expected

        # margin setting must be ignored
        writer.margin = 1
        out = writer.dumps()
        print_test_result(expected=expected, actual=out)
        assert out == expected

    def test_normal_escape_formula_injection(self, capsys):
        writer = table_writer_class(
            headers=["a", "b", "c", "d", "e"],
            value_matrix=[["a+b", "=a+b", "-a+b", "+a+b", "@a+b"]],
        )
        writer.update_preprocessor(is_escape_formula_injection=True)
        writer.write_table()
        expected = r""""a","b","c","d","e"
"a+b","\"=a+b","\"-a+b","\"+a+b","\"@a+b"
"""
        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected

    @pytest.mark.parametrize(
        ["header", "value", "expected"],
        [[data.header, data.value, data.expected] for data in exception_test_data_list],
    )
    def test_exception(self, header, value, expected):
        writer = table_writer_class(headers=header, value_matrix=value)

        assert writer.dumps() == ""
        assert str(writer) == ""


class Test_CsvTableWriter_write_table_iter:
    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [
            [
                "tablename",
                ["ha", "hb", "hc"],
                value_matrix_iter,
                dedent(
                    """\
                "ha","hb","hc"
                1,2,3
                11,12,13
                1,2,3
                11,12,13
                101,102,103
                1001,1002,1003
                """
                ),
            ]
        ],
    )
    def test_normal(self, capsys, table, header, value, expected):
        writer = table_writer_class(
            table_name=table, headers=header, value_matrix=value, iteration_length=len(value)
        )
        writer.write_table_iter()

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected

    @pytest.mark.parametrize(
        ["header", "value", "expected"],
        [[data.header, data.value, data.expected] for data in exception_test_data_list],
    )
    def test_smoke_empty(self, header, value, expected):
        writer = table_writer_class(headers=header, value_matrix=value)

        writer.write_table_iter()
