# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import collections

import pytablewriter
import pytest

from .data import header_list
from .data import value_matrix
from .data import value_matrix_with_none
from .data import mix_header_list
from .data import mix_value_matrix


Data = collections.namedtuple("Data", "table indent header value expected")

normal_test_data_list = [
    Data(
        table="",
        indent=0,
        header=header_list,
        value=value_matrix,
        expected="""pandas.DataFrame(
    {'a': [1, 2, 3],
     'b': [123.1, 2.2, 3.3],
     'c': ['a', 'bb', 'ccc'],
     'dd': [1, 2.2, 3],
     'e': [1, 2.2, 'cccc']}
)
"""
    ),
    Data(
        table="tablename",
        indent=0,
        header=header_list,
        value=None,
        expected="""tablename = pandas.DataFrame(
    {}
)
"""
    ),
    Data(
        table="tablename",
        indent=0,
        header=header_list,
        value=value_matrix,
        expected="""tablename = pandas.DataFrame(
    {'a': [1, 2, 3],
     'b': [123.1, 2.2, 3.3],
     'c': ['a', 'bb', 'ccc'],
     'dd': [1, 2.2, 3],
     'e': [1, 2.2, 'cccc']}
)
"""
    ),
    Data(
        table="table name",
        indent=0,
        header=header_list,
        value=value_matrix,
        expected="""table_name = pandas.DataFrame(
    {'a': [1, 2, 3],
     'b': [123.1, 2.2, 3.3],
     'c': ['a', 'bb', 'ccc'],
     'dd': [1, 2.2, 3],
     'e': [1, 2.2, 'cccc']}
)
"""
    ),
    Data(
        table="",
        indent=1,
        header=header_list,
        value=value_matrix,
        expected="""    pandas.DataFrame(
        {'a': [1, 2, 3],
         'b': [123.1, 2.2, 3.3],
         'c': ['a', 'bb', 'ccc'],
         'dd': [1, 2.2, 3],
         'e': [1, 2.2, 'cccc']}
    )
"""
    ),
    Data(
        table="table with%null-value",
        indent=0,
        header=header_list,
        value=value_matrix_with_none,
        expected="""table_with_null_value = pandas.DataFrame(
    {'a': [1, None, 3, None],
     'b': [None, 2.2, 3.3, None],
     'c': ['a', None, 'ccc', None],
     'dd': [1, 2.2, None, None],
     'e': [None, 2.2, 'cccc', None]}
)
"""
    ),
    Data(
        table="tablename",
        indent=0,
        header=mix_header_list,
        value=mix_value_matrix,
        expected="""tablename = pandas.DataFrame(
    {'bool': [True, False, True],
     'c': ['aa', 'bbb', 'cccc'],
     'f': [1.1, 2.2, 3.33],
     'i': [1, 2, 3],
     'if': [1, 2.2, -3],
     'ifc': [1, 2.2, 'ccc'],
     'inf': [numpy.inf, numpy.inf, numpy.inf],
     'mix_num': [1.0, numpy.inf, numpy.nan],
     'nan': [numpy.nan, numpy.nan, numpy.nan],
     'time': ['2017-01-01 00:00:00',
              '2017-01-02 03:04:05+0900',
              '2017-01-01 00:00:00']}
)
"""
    ),
]

exception_test_data_list = [
    Data(
        table="",
        indent=normal_test_data_list[0].indent,
        header=[],
        value=[],
        expected=pytablewriter.EmptyHeaderError
    ),
    Data(
        table="",
        indent=normal_test_data_list[0].indent,
        header=[],
        value=normal_test_data_list[0].value,
        expected=pytablewriter.EmptyHeaderError
    ),
    Data(
        table="",
        indent=normal_test_data_list[0].indent,
        header=None,
        value=normal_test_data_list[0].value,
        expected=pytablewriter.EmptyHeaderError
    ),
]

table_writer_class = pytablewriter.PandasDataFrameWriter


class Test_PandasDataFrameWriter_write_new_line:

    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_PandasDataFrameWriter_write_table:

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
        assert out == expected

    @pytest.mark.parametrize(
        ["table", "indent", "header", "value", "expected"],
        [
            [data.table, data.indent, data.header, data.value, data.expected]
            for data in exception_test_data_list
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
