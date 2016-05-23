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


Data = collections.namedtuple("Data", "table indent header value expected")

normal_test_data_list = [
    Data(
        table="",
        indent=0,
        header=header_list,
        value=value_matrix,
        expected="""<table>
  <thead>
    <tr>
      <th>a</th>
      <th>b</th>
      <th>c</th>
      <th>dd</th>
      <th>e</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="right">1</td>
      <td align="right">123.1</td>
      <td align="left">a</td>
      <td align="right">1.0</td>
      <td align="right">1</td>
    </tr>
    <tr>
      <td align="right">2</td>
      <td align="right">2.2</td>
      <td align="left">bb</td>
      <td align="right">2.2</td>
      <td align="right">2.2</td>
    </tr>
    <tr>
      <td align="right">3</td>
      <td align="right">3.3</td>
      <td align="left">ccc</td>
      <td align="right">3.0</td>
      <td align="left">cccc</td>
    </tr>
  </tbody>
</table>
"""
    ),
    Data(
        table="tablename",
        indent=0,
        header=header_list,
        value=value_matrix,
        expected="""<table id="tablename">
  <caption>tablename</caption>
  <thead>
    <tr>
      <th>a</th>
      <th>b</th>
      <th>c</th>
      <th>dd</th>
      <th>e</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="right">1</td>
      <td align="right">123.1</td>
      <td align="left">a</td>
      <td align="right">1.0</td>
      <td align="right">1</td>
    </tr>
    <tr>
      <td align="right">2</td>
      <td align="right">2.2</td>
      <td align="left">bb</td>
      <td align="right">2.2</td>
      <td align="right">2.2</td>
    </tr>
    <tr>
      <td align="right">3</td>
      <td align="right">3.3</td>
      <td align="left">ccc</td>
      <td align="right">3.0</td>
      <td align="left">cccc</td>
    </tr>
  </tbody>
</table>
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
    Data(
        table="",
        indent=normal_test_data_list[0].indent,
        header=normal_test_data_list[0].header,
        value=[],
        expected=pytablewriter.EmptyValueError
    ),
    Data(
        table="",
        indent=normal_test_data_list[0].indent,
        header=normal_test_data_list[0].header,
        value=None,
        expected=pytablewriter.EmptyValueError,
    ),
]

table_writer_class = pytablewriter.HtmlTableWriter


class Test_HtmlTableWriter_write_new_line:

    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, err = capsys.readouterr()
        assert out == "\n"


class Test_HtmlTableWriter_write_table:

    @pytest.mark.parametrize(["table", "indent", "header", "value", "expected"], [
        [data.table, data.indent, data.header, data.value, data.expected]
        for data in normal_test_data_list
    ])
    def test_normal(self, capsys, table, indent, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.set_indent_level(indent)
        writer.header_list = header
        writer.value_matrix = value
        writer.write_table()

        out, err = capsys.readouterr()
        assert out == expected

    @pytest.mark.parametrize(["table", "indent", "header", "value", "expected"], [
        [data.table, data.indent, data.header, data.value, data.expected]
        for data in exception_test_data_list
    ])
    def test_exception(self, capsys, table, indent, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.set_indent_level(indent)
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table()
