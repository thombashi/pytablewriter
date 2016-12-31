# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import collections
from decimal import Decimal

import pytablereader as ptr
import pytablewriter as ptw
import pytest

from .data import (
    header_list,
    value_matrix,
    value_matrix_with_none,
    mix_header_list,
    mix_value_matrix,
    float_header_list,
    float_value_matrix,
    value_matrix_iter
)


Data = collections.namedtuple(
    "Data", "table indent header value is_float_formatting expected")

normal_test_data_list = [
    Data(
        table="",
        indent=0,
        header=header_list,
        value=value_matrix,
        is_float_formatting=True,
        expected=""" a |  b  | c |dd | e  
--:|----:|---|--:|----
  1|123.1|a  |1.0|1   
  2|  2.2|bb |2.2|2.2 
  3|  3.3|ccc|3.0|cccc
"""),
    Data(
        table="",
        indent=0,
        header=header_list,
        value=None,
        is_float_formatting=True,
        expected=""" a | b | c |dd | e 
---|---|---|---|---
"""),
    Data(
        table="",
        indent=0,
        header=header_list,
        value=[
            ["1", 123.09999999999999, "a", "1",   1],
            [2, 2.2000000000000002, "bb", "2.2", 2.2000000000000002],
            [3, 3.2999999999999998, "ccc", "3.2999999999999998",   "cccc"],
        ],
        is_float_formatting=True,
        expected=""" a |  b  | c |dd | e  
--:|----:|---|--:|----
  1|123.1|a  |1.0|1   
  2|  2.2|bb |2.2|2.2 
  3|  3.3|ccc|3.3|cccc
"""),
    Data(
        table="tablename",
        indent=0,
        header=header_list,
        value=value_matrix,
        is_float_formatting=True,
        expected="""# tablename
 a |  b  | c |dd | e  
--:|----:|---|--:|----
  1|123.1|a  |1.0|1   
  2|  2.2|bb |2.2|2.2 
  3|  3.3|ccc|3.0|cccc
"""),
    Data(
        table="tablename",
        indent=0,
        header=header_list,
        value=value_matrix,
        is_float_formatting=False,
        expected="""# tablename
 a |  b  | c |dd | e  
--:|----:|---|--:|----
  1|123.1|a  |  1|1   
  2|  2.2|bb |2.2|2.2 
  3|  3.3|ccc|  3|cccc
"""),
    Data(
        table="tablename",
        indent=1,
        header=header_list,
        value=value_matrix,
        is_float_formatting=True,
        expected="""## tablename
 a |  b  | c |dd | e  
--:|----:|---|--:|----
  1|123.1|a  |1.0|1   
  2|  2.2|bb |2.2|2.2 
  3|  3.3|ccc|3.0|cccc
"""),
    Data(
        table="",
        indent=0,
        header=header_list,
        value=value_matrix_with_none,
        is_float_formatting=True,
        expected=""" a | b | c |dd | e  
--:|--:|---|--:|----
  1|   |a  |1.0|    
   |2.2|   |2.2|2.2 
  3|3.3|ccc|   |cccc
   |   |   |   |    
"""),
    Data(
        table="",
        indent=0,
        header=mix_header_list,
        value=mix_value_matrix,
        is_float_formatting=True,
        expected=""" i | f  | c  | if |ifc|bool |  inf   |nan|mix_num |          time           
--:|---:|----|---:|---|-----|--------|---|-------:|-------------------------
  1|1.10|aa  | 1.0|1  |True |Infinity|NaN|       1|2017-01-01 00:00:00      
  2|2.20|bbb | 2.2|2.2|False|Infinity|NaN|Infinity|2017-01-02 03:04:05+09:00
  3|3.33|cccc|-3.0|ccc|True |Infinity|NaN|     NaN|2017-01-01 00:00:00      
"""),
    Data(
        table="",
        indent=0,
        header=float_header_list,
        value=float_value_matrix,
        is_float_formatting=True,
        expected=""" a  |   b   |  c  
---:|------:|----:
0.01|  9.123|0.000
1.00| 99.123|0.010
1.20|999.123|0.001
"""),
    Data(
        table="",
        indent=0,
        header=[u'Name', u'xUnit', u'Source', u'Remarks'],
        value=[
            [
                u'Crotest',
                u'',
                u'[160]',
                u'MIT License. A tiny and simple test framework for Crystal\nwith common assertions and no pollution into Object class.',
                u'',
            ]
        ],
        is_float_formatting=True,
        expected=""" Name  |xUnit|Source|                                                      Remarks                                                       
-------|-----|------|--------------------------------------------------------------------------------------------------------------------
Crotest|     |[160] |MIT License. A tiny and simple test framework for Crystal with common assertions and no pollution into Object class.
"""),
    Data(
        table="",
        indent=0,
        header=["姓", "名", "生年月日", "郵便番号", "住所", "電話番号"],
        value=[
            ["山田", "太郎", "2001/1/1", "100-0002",
             "東京都千代田区皇居外苑", "03-1234-5678"],
            ["山田", "次郎", "2001/1/2", "251-0036",
             "神奈川県藤沢市江の島１丁目", "03-9999-9999"],
        ],
        is_float_formatting=True,
        expected=""" 姓 | 名 |生年月日|郵便番号|           住所           |  電話番号  
----|----|--------|--------|--------------------------|------------
山田|太郎|2001/1/1|100-0002|東京都千代田区皇居外苑    |03-1234-5678
山田|次郎|2001/1/2|251-0036|神奈川県藤沢市江の島１丁目|03-9999-9999
"""),
    Data(
        table="quoted values",
        indent=0,
        header=['"quote"', '"abc efg"'],
        value=[
            ['"1"', '"abc"'],
            ['"-1"', '"efg"'],
        ],
        is_float_formatting=True,
        expected="""# quoted values
quote|abc efg
----:|-------
    1|abc    
   -1|efg    
"""),
]

exception_test_data_list = [
    Data(
        table="",
        indent=0,
        header=[],
        value=[],
        is_float_formatting=True,
        expected=ptw.EmptyTableDataError
    ),
    Data(
        table="",
        indent=0,
        header=[],
        value=value_matrix,
        is_float_formatting=True,
        expected=ptw.EmptyHeaderError
    ),
    Data(
        table="",
        indent=0,
        header=None,
        value=value_matrix,
        is_float_formatting=True,
        expected=ptw.EmptyHeaderError
    ),
]

table_writer_class = ptw.MarkdownTableWriter


class Test_MarkdownTableWriter_write_new_line:

    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_MarkdownTableWriter_set_table_data:

    def test_normal(self, capsys):
        writer = table_writer_class()

        tabledata = ptr.TableData(
            "tmp",
            ["attr_a", "attr_b", "attr_c"],
            [
                ["1", "4", "a"],
                ["2", "2.1", "bb"],
                ["3", "120.9", "ccc"],
            ])

        writer.from_tabledata(tabledata)

        assert writer.table_name == "tmp"
        assert writer.header_list == ["attr_a", "attr_b", "attr_c"]
        assert writer.value_matrix == [
            [1, 4, "a"],
            [2, Decimal("2.1"), "bb"],
            [3, Decimal("120.9"), "ccc"],
        ]


class Test_MarkdownTableWriter_write_table:

    @pytest.mark.parametrize(
        ["table", "indent", "header", "value",
            "is_float_formatting", "expected"],
        [
            [
                data.table, data.indent, data.header, data.value,
                data.is_float_formatting, data.expected
            ]
            for data in normal_test_data_list
        ]
    )
    def test_normal(
            self, capsys, table, indent, header, value,
            is_float_formatting, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.set_indent_level(indent)
        writer.header_list = header
        writer.value_matrix = value
        writer.is_float_formatting = is_float_formatting
        writer.write_table()

        out, _err = capsys.readouterr()

        print("expected:\n{}".format(expected))
        print("actual:\n{}".format(out))

        assert out == expected

    def test_normal_tabledata(self, capsys):
        writer = table_writer_class()

        tabledata = ptr.TableData(
            table_name="loader_mapping",
            header_list=['Format name', 'Loader'],
            record_list=[
                ['csv', 'CsvTableFileLoader'],
                ['excel', 'ExcelTableFileLoader'],
                ['html', 'HtmlTableFileLoader'],
                ['markdown', 'MarkdownTableFileLoader'],
                ['mediawiki', 'MediaWikiTableFileLoader'],
                ['json', 'JsonTableFileLoader'],
            ])
        writer.from_tabledata(tabledata)
        writer.write_table()

        expected = """# loader_mapping
Format name|         Loader         
-----------|------------------------
csv        |CsvTableFileLoader      
excel      |ExcelTableFileLoader    
html       |HtmlTableFileLoader     
markdown   |MarkdownTableFileLoader 
mediawiki  |MediaWikiTableFileLoader
json       |JsonTableFileLoader     
"""
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


class Test_MarkdownTableWriter_write_table_iter:

    @pytest.mark.parametrize(["table", "header", "value", "expected"], [
        [
            "tablename",
            ["ha", "hb", "hc"],
            value_matrix_iter,
            """# tablename
ha |hb |hc 
--:|--:|--:
  1|  2|  3
 11| 12| 13
  1|  2|  3
 11| 12| 13
 101| 102| 103
1001|1002|1003
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
        ["table", "header", "value", "expected"],
        [
            [data.table, data.header, data.value, data.expected]
            for data in exception_test_data_list
        ]
    )
    def test_exception(self, capsys, table, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table_iter()
