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
        expected=""".. table:: 

    +-+-----+---+---+----+
    |a|  b  | c |dd | e  |
    +=+=====+===+===+====+
    |1|123.1|a  |1.0|1   |
    +-+-----+---+---+----+
    |2|  2.2|bb |2.2|2.2 |
    +-+-----+---+---+----+
    |3|  3.3|ccc|3.0|cccc|
    +-+-----+---+---+----+
"""
    ),
    Data(
        table="tablename",
        indent=0,
        header=header_list,
        value=value_matrix,
        expected=""".. table:: tablename

    +-+-----+---+---+----+
    |a|  b  | c |dd | e  |
    +=+=====+===+===+====+
    |1|123.1|a  |1.0|1   |
    +-+-----+---+---+----+
    |2|  2.2|bb |2.2|2.2 |
    +-+-----+---+---+----+
    |3|  3.3|ccc|3.0|cccc|
    +-+-----+---+---+----+
"""
    ),
    Data(
        table=None,
        indent=1,
        header=header_list,
        value=value_matrix,
        expected="""    .. table:: 
    
        +-+-----+---+---+----+
        |a|  b  | c |dd | e  |
        +=+=====+===+===+====+
        |1|123.1|a  |1.0|1   |
        +-+-----+---+---+----+
        |2|  2.2|bb |2.2|2.2 |
        +-+-----+---+---+----+
        |3|  3.3|ccc|3.0|cccc|
        +-+-----+---+---+----+
"""
    ),
    Data(
        table="zone",
        indent=0,
        header=["zone_id", "country_code", "zone_name"],
        value=[
            ["1", "AD", "Europe/Andorra"],
            ["2", "AE", "Asia/Dubai"],
            ["3", "AF", "Asia/Kabul"],
            ["4", "AG", "America/Antigua"],
            ["5", "AI", "America/Anguilla"],
        ],
        expected=""".. table:: zone

    +-------+------------+----------------+
    |zone_id|country_code|   zone_name    |
    +=======+============+================+
    |      1|AD          |Europe/Andorra  |
    +-------+------------+----------------+
    |      2|AE          |Asia/Dubai      |
    +-------+------------+----------------+
    |      3|AF          |Asia/Kabul      |
    +-------+------------+----------------+
    |      4|AG          |America/Antigua |
    +-------+------------+----------------+
    |      5|AI          |America/Anguilla|
    +-------+------------+----------------+
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

table_writer_class = pytablewriter.RstGridTableWriter


class Test_RstGridTableWriter_write_new_line:

    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, err = capsys.readouterr()
        assert out == "\n"


class Test_RstGridTableWriter_write_table:

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
