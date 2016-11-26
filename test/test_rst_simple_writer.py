# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import print_function

import pytablewriter
import pytest

from .data import Data
from .data import null_test_data_list
from .data import header_list
from .data import value_matrix
from .data import value_matrix_with_none
from .data import mix_header_list
from .data import mix_value_matrix


normal_test_data_list = [
    Data(
        table="tablename",
        indent=0,
        header=header_list,
        value=value_matrix,
        expected=""".. table:: tablename

    =  =====  ===  ===  ====
    a    b     c   dd    e  
    =  =====  ===  ===  ====
    1  123.1  a    1.0  1   
    2    2.2  bb   2.2  2.2 
    3    3.3  ccc  3.0  cccc
    =  =====  ===  ===  ====
"""),
    Data(
        table="",
        indent=0,
        header=header_list,
        value=None,
        expected=""".. table:: 

    =  =  =  ==  =
    a  b  c  dd  e
    =  =  =  ==  =
    =  =  =  ==  =
"""),
    Data(
        table=None,
        indent=0,
        header=None,
        value=value_matrix,
        expected=""".. table:: 

    =  =====  ===  ===  ====
    1  123.1  a    1.0  1   
    2    2.2  bb   2.2  2.2 
    3    3.3  ccc  3.0  cccc
    =  =====  ===  ===  ====
"""),
    Data(
        table="",
        indent=1,
        header=header_list,
        value=value_matrix,
        expected="""    .. table:: 
    
        =  =====  ===  ===  ====
        a    b     c   dd    e  
        =  =====  ===  ===  ====
        1  123.1  a    1.0  1   
        2    2.2  bb   2.2  2.2 
        3    3.3  ccc  3.0  cccc
        =  =====  ===  ===  ====
"""),
    Data(
        table="table name",
        indent=0,
        header=header_list,
        value=value_matrix_with_none,
        expected=""".. table:: table name

    =  ===  ===  ===  ====
    a   b    c   dd    e  
    =  ===  ===  ===  ====
    1       a    1.0      
       2.2       2.2  2.2 
    3  3.3  ccc       cccc
                          
    =  ===  ===  ===  ====
"""),
    Data(
        table="table name",
        indent=0,
        header=mix_header_list,
        value=mix_value_matrix,
        expected=""".. table:: table name

    =  ====  ====  ====  ===  =====  ========  ===  ========  =========================
    i   f     c     if   ifc  bool     inf     nan  mix_num             time           
    =  ====  ====  ====  ===  =====  ========  ===  ========  =========================
    1  1.10  aa     1.0  1    True   Infinity  NaN         1  2017-01-01 00:00:00      
    2  2.20  bbb    2.2  2.2  False  Infinity  NaN  Infinity  2017-01-02 03:04:05+09:00
    3  3.33  cccc  -3.0  ccc  True   Infinity  NaN       NaN  2017-01-01 00:00:00      
    =  ====  ====  ====  ===  =====  ========  ===  ========  =========================
"""),
]

table_writer_class = pytablewriter.RstSimpleTableWriter


class Test_RstSimpleTableWriter_write_new_line:

    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_RstSimpleTableWriter_write_table:

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
            for data in null_test_data_list
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


class Test_RstSimpleTableWriter_write_table_iter:

    def test_exception(self):
        writer = table_writer_class()

        with pytest.raises(pytablewriter.NotSupportedError):
            writer.write_table_iter()
