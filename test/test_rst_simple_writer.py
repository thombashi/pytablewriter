# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, print_function, unicode_literals

from textwrap import dedent

import pytablewriter
import pytest

from ._common import print_test_result
from .data import (
    Data,
    header_list,
    mix_header_list,
    mix_value_matrix,
    null_test_data_list,
    style_list,
    style_tabledata,
    value_matrix,
    value_matrix_with_none,
)


normal_test_data_list = [
    Data(
        table="tablename",
        indent=0,
        header=header_list,
        value=value_matrix,
        expected=dedent(
            """\
            .. table:: tablename

                =  =====  ===  ===  ====
                a    b     c   dd    e  
                =  =====  ===  ===  ====
                1  123.1  a    1.0     1
                2    2.2  bb   2.2   2.2
                3    3.3  ccc  3.0  cccc
                =  =====  ===  ===  ====
            """
        ),
    ),
    Data(
        table="",
        indent=0,
        header=header_list,
        value=None,
        expected=dedent(
            """\
            .. table:: 

                =  =  =  ==  =
                a  b  c  dd  e
                =  =  =  ==  =
                =  =  =  ==  =
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
            .. table:: 

                =  =====  ===  ===  ====
                1  123.1  a    1.0     1
                2    2.2  bb   2.2   2.2
                3    3.3  ccc  3.0  cccc
                =  =====  ===  ===  ====
            """
        ),
    ),
    Data(
        table="",
        indent=1,
        header=header_list,
        value=value_matrix,
        expected="""    .. table:: 

        =  =====  ===  ===  ====
        a    b     c   dd    e  
        =  =====  ===  ===  ====
        1  123.1  a    1.0     1
        2    2.2  bb   2.2   2.2
        3    3.3  ccc  3.0  cccc
        =  =====  ===  ===  ====
""",
    ),
    Data(
        table="table name",
        indent=0,
        header=header_list,
        value=value_matrix_with_none,
        expected=dedent(
            """\
            .. table:: table name

                =  ===  ===  ===  ====
                a   b    c   dd    e  
                =  ===  ===  ===  ====
                1       a    1.0      
                   2.2       2.2   2.2
                3  3.3  ccc       cccc

                =  ===  ===  ===  ====
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
            .. table:: table name

                =  ====  ====  ====  ===  =====  ========  ===  ========  =========================
                i   f     c     if   ifc  bool     inf     nan  mix_num             time           
                =  ====  ====  ====  ===  =====  ========  ===  ========  =========================
                1  1.10  aa     1.0    1  True   Infinity  NaN         1  2017-01-01T00:00:00      
                2  2.20  bbb    2.2  2.2  False  Infinity  NaN  Infinity  2017-01-02 03:04:05+09:00
                3  3.33  cccc  -3.0  ccc  True   Infinity  NaN       NaN  2017-01-01T00:00:00      
                =  ====  ====  ====  ===  =====  ========  ===  ========  =========================
            """
        ),
    ),
]

table_writer_class = pytablewriter.RstSimpleTableWriter


class Test_RstSimpleTableWriter_write_new_line(object):
    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_RstSimpleTableWriter_write_table(object):
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
        writer.header_list = header
        writer.value_matrix = value
        writer.write_table()

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected

    def test_normal_style_list(self):
        writer = table_writer_class()
        writer.from_tabledata(style_tabledata)
        writer.style_list = style_list

        expected = dedent(
            """\
            .. table:: style test

                ====  =====  ====  =====  ======  =====  ============  ========  ========  =============
                none  empty  tiny  small  medium  large  null w/ bold   L bold   S italic  L bold italic
                ====  =====  ====  =====  ======  =====  ============  ========  ========  =============
                 111    111   111    111     111    111                 **111**     *111*        **111**
                1234   1234  1234   1234   1,234  1 234                **1234**    *1234*       **1234**
                ====  =====  ====  =====  ======  =====  ============  ========  ========  =============
            """
        )
        out = writer.dumps()
        print_test_result(expected=expected, actual=out)

        assert out == expected

    @pytest.mark.parametrize(
        ["table", "indent", "header", "value", "expected"],
        [
            [data.table, data.indent, data.header, data.value, data.expected]
            for data in null_test_data_list
        ],
    )
    def test_exception(self, table, indent, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.set_indent_level(indent)
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table()


class Test_RstSimpleTableWriter_write_table_iter(object):
    def test_exception(self):
        writer = table_writer_class()

        with pytest.raises(pytablewriter.NotSupportedError):
            writer.write_table_iter()
