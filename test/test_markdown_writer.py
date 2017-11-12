# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import collections
from decimal import Decimal

import pytest

import pytablewriter as ptw
from tabledata import TableData

from .data import (
    header_list,
    value_matrix,
    value_matrix_with_none,
    mix_header_list,
    mix_value_matrix,
    float_header_list,
    float_value_matrix,
    value_matrix_iter,
    value_matrix_iter_1,
)


Data = collections.namedtuple(
    "Data", "table indent header value is_formatting_float expected")

normal_test_data_list = [
    Data(table="",
         indent=0,
         header=header_list,
         value=value_matrix,
         is_formatting_float=True,
         expected="""| a |  b  | c |dd | e  |
|--:|----:|---|--:|----|
|  1|123.1|a  |1.0|   1|
|  2|  2.2|bb |2.2| 2.2|
|  3|  3.3|ccc|3.0|cccc|

"""),
    Data(table="",
         indent=0,
         header=header_list,
         value=None,
         is_formatting_float=True,
         expected="""| a | b | c |dd | e |
|---|---|---|---|---|

"""),
    Data(table="floating point",
         indent=0,
         header=header_list,
         value=[
             ["1", 123.09999999999999, "a", "1",   1],
             [2, 2.2000000000000002, "bb", "2.2", 2.2000000000000002],
             [3, 3.2999999999999998, "ccc", "3.2999999999999998",   "cccc"],
         ],
         is_formatting_float=True,
         expected="""# floating point
| a |  b  | c |dd | e  |
|--:|----:|---|--:|----|
|  1|123.1|a  |1.0|   1|
|  2|  2.2|bb |2.2| 2.2|
|  3|  3.3|ccc|3.3|cccc|

"""),
    Data(table="tablename",
         indent=1,
         header=header_list,
         value=value_matrix,
         is_formatting_float=True,
         expected="""## tablename
| a |  b  | c |dd | e  |
|--:|----:|---|--:|----|
|  1|123.1|a  |1.0|   1|
|  2|  2.2|bb |2.2| 2.2|
|  3|  3.3|ccc|3.0|cccc|

"""),
    Data(table="",
         indent=0,
         header=header_list,
         value=value_matrix_with_none,
         is_formatting_float=True,
         expected="""| a | b | c |dd | e  |
|--:|--:|---|--:|----|
|  1|   |a  |1.0|    |
|   |2.2|   |2.2| 2.2|
|  3|3.3|ccc|   |cccc|
|   |   |   |   |    |

"""),
    Data(table="",
         indent=0,
         header=mix_header_list,
         value=mix_value_matrix,
         is_formatting_float=True,
         expected="""| i | f  | c  | if |ifc|bool |  inf   |nan|mix_num |          time           |
|--:|---:|----|---:|---|-----|--------|---|-------:|-------------------------|
|  1|1.10|aa  | 1.0|  1|True |Infinity|NaN|       1|2017-01-01 00:00:00      |
|  2|2.20|bbb | 2.2|2.2|False|Infinity|NaN|Infinity|2017-01-02 03:04:05+09:00|
|  3|3.33|cccc|-3.0|ccc|True |Infinity|NaN|     NaN|2017-01-01 00:00:00      |

"""),
    Data(table="formatting float 1",
         indent=0,
         header=header_list,
         value=value_matrix,
         is_formatting_float=True,
         expected="""# formatting float 1
| a |  b  | c |dd | e  |
|--:|----:|---|--:|----|
|  1|123.1|a  |1.0|   1|
|  2|  2.2|bb |2.2| 2.2|
|  3|  3.3|ccc|3.0|cccc|

"""),
    Data(table="formatting float 2",
         indent=0,
         header=float_header_list,
         value=float_value_matrix,
         is_formatting_float=True,
         expected="""# formatting float 2
| a  |     b     |  c  |
|---:|----------:|----:|
|0.01|     0.0012|0.000|
|1.00|    99.9000|0.010|
|1.20|999999.1230|0.001|

"""),
    Data(table="not formatting float 1",
         indent=0,
         header=header_list,
         value=value_matrix,
         is_formatting_float=False,
         expected="""# not formatting float 1
| a |  b  | c |dd | e  |
|--:|----:|---|--:|----|
|  1|123.1|a  |  1|   1|
|  2|  2.2|bb |2.2| 2.2|
|  3|  3.3|ccc|  3|cccc|

"""),
    Data(table="not formatting float 2",
         indent=0,
         header=float_header_list,
         value=float_value_matrix,
         is_formatting_float=False,
         expected="""# not formatting float 2
| a  |    b     |  c  |
|---:|---------:|----:|
|0.01|   0.00125|    0|
|   1|      99.9| 0.01|
| 1.2|999999.123|0.001|

"""),
    Data(table="",
         indent=0,
         header=['Name', 'xUnit', 'Source', 'Remarks'],
         value=[
             [
                 'Crotest',
                 '',
                 '[160]',
                 'MIT License. A tiny and simple test framework for Crystal\nwith common assertions and no pollution into Object class.',
                 '',
             ]
         ],
         is_formatting_float=True,
         expected="""| Name  |xUnit|Source|                                                      Remarks                                                       |
|-------|-----|------|--------------------------------------------------------------------------------------------------------------------|
|Crotest|     |[160] |MIT License. A tiny and simple test framework for Crystal with common assertions and no pollution into Object class.|

"""),
    Data(table="",
         indent=0,
         header=["姓", "名", "生年月日", "郵便番号", "住所", "電話番号"],
         value=[
             ["山田", "太郎", "2001/1/1", "100-0002",
              "東京都千代田区皇居外苑", "03-1234-5678"],
             ["山田", "次郎", "2001/1/2", "251-0036",
                 "神奈川県藤沢市江の島１丁目", "03-9999-9999"],
         ],
         is_formatting_float=True,
         expected="""| 姓 | 名 |生年月日|郵便番号|           住所           |  電話番号  |
|----|----|--------|--------|--------------------------|------------|
|山田|太郎|2001/1/1|100-0002|東京都千代田区皇居外苑    |03-1234-5678|
|山田|次郎|2001/1/2|251-0036|神奈川県藤沢市江の島１丁目|03-9999-9999|

"""),
    Data(table="quoted values",
         indent=0,
         header=['"quote"', '"abc efg"'],
         value=[
             ['"1"', '"abc"'],
             ['"-1"', '"efg"'],
         ],
         is_formatting_float=True,
         expected="""# quoted values
|quote|abc efg|
|----:|-------|
|    1|abc    |
|   -1|efg    |

"""),
    Data(table="not str headers",
         indent=0,
         header=[None, 1, 0.1],
         value=[
             [None, 1, 0.1],
         ],
         is_formatting_float=True,
         expected="""# not str headers
|   | 1 |0.1|
|---|--:|--:|
|   |  1|0.1|

"""),
    Data(table="no uniform matrix",
         indent=0,
         header=["a", "b", "c"],
         value=[
             ["a", 0],
             ["b", 1, "bb"],
             ["c", 2, "ccc", 0.1],
         ],
         is_formatting_float=True,
         expected="""# no uniform matrix
| a | b | c |
|---|--:|---|
|a  |  0|   |
|b  |  1|bb |
|c  |  2|ccc|

"""),
    Data(table="line breaks",
         indent=0,
         header=["a\nb", "\nc\n\nd\n", "e\r\nf"],
         value=[["v1\nv1", "v2\n\nv2", "v3\r\nv3"]],
         is_formatting_float=True,
         expected="""# line breaks
| a b | c d  | e f  |
|-----|------|------|
|v1 v1|v2 v2 |v3 v3 |

"""),
    Data(table="empty header",
         indent=0,
         header=[],
         value=value_matrix,
         is_formatting_float=True,
         expected="""# empty header
| A |  B  | C | D | E  |
|--:|----:|---|--:|----|
|  1|123.1|a  |1.0|   1|
|  2|  2.2|bb |2.2| 2.2|
|  3|  3.3|ccc|3.0|cccc|

"""),
    Data(table="vertical bar",
         indent=1,
         header=["a|b", "|c||d|"],
         value=[["|v1|v1|", "v2|v2"]],
         is_formatting_float=True,
         expected="""## vertical bar
|  a\|b  |\|c\|\|d\||
|-------|------|
|\|v1\|v1\||v2\|v2 |

"""),
    Data(table="mixed value types",
         indent=0,
         header=["data", "v"],
         value=[
             [3.4375, 65.5397978633],
             [65.5397978633, 127.642095727],
             [189.74439359, 189.74439359],
             [10064.0097539, 10001.907456],
             ["next", 10250.3166474],
         ],
         is_formatting_float=True,
         expected="""# mixed value types
|  data   |   v    |
|---------|-------:|
|    3.437|   65.54|
|   65.540|  127.64|
|  189.744|  189.74|
|10064.010|10001.91|
|next     |10250.32|

"""),
]

exception_test_data_list = [
    Data(
        table="",
        indent=0,
        header=[],
        value=[],
        is_formatting_float=True,
        expected=ptw.EmptyTableDataError),
]

table_writer_class = ptw.MarkdownTableWriter


class Test_MarkdownTableWriter_write_new_line(object):

    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_MarkdownTableWriter_set_table_data(object):

    def test_normal(self):
        writer = table_writer_class()
        writer.from_tabledata(TableData(
            "tmp",
            ["attr_a", "attr_b", "attr_c"],
            [
                ["1", "4", "a"],
                ["2", "2.1", "bb"],
                ["3", "120.9", "ccc"],
            ]))

        assert writer.table_name == "tmp"
        assert writer.header_list == ["attr_a", "attr_b", "attr_c"]
        assert writer.value_matrix == [
            [1, 4, "a"],
            [2, Decimal("2.1"), "bb"],
            [3, Decimal("120.9"), "ccc"],
        ]


class Test_MarkdownTableWriter_write_table(object):

    @pytest.mark.parametrize(
        ["table", "indent", "header", "value",
            "is_formatting_float", "expected"],
        [
            [
                data.table, data.indent, data.header, data.value,
                data.is_formatting_float, data.expected
            ]
            for data in normal_test_data_list
        ])
    def test_normal(
            self, capsys, table, indent, header, value,
            is_formatting_float, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.set_indent_level(indent)
        writer.header_list = header
        writer.value_matrix = value
        writer.is_formatting_float = is_formatting_float
        writer.write_table()

        out, _err = capsys.readouterr()

        print("[expected]\n{}".format(expected))
        print("[actual]\n{}".format(out))

        assert out == expected

    def test_normal_tabledata(self, capsys):
        writer = table_writer_class()
        writer.from_tabledata(TableData(
            table_name="loader_mapping",
            header_list=['Name', 'Loader'],
            record_list=[
                ['csv', 'CsvTableFileLoader'],
                ['excel', 'ExcelTableFileLoader'],
                ['html', 'HtmlTableFileLoader'],
                ['markdown', 'MarkdownTableFileLoader'],
                ['mediawiki', 'MediaWikiTableFileLoader'],
                ['json', 'JsonTableFileLoader'],
                ['Long Format Name', 'Loader'],
            ]))
        writer.write_table()

        expected = """# loader_mapping
|      Name      |         Loader         |
|----------------|------------------------|
|csv             |CsvTableFileLoader      |
|excel           |ExcelTableFileLoader    |
|html            |HtmlTableFileLoader     |
|markdown        |MarkdownTableFileLoader |
|mediawiki       |MediaWikiTableFileLoader|
|json            |JsonTableFileLoader     |
|Long Format Name|Loader                  |

"""
        out, _err = capsys.readouterr()

        print("[expected]\n{}".format(expected))
        print("[actual]\n{}".format(out))

        assert out == expected

    @pytest.mark.parametrize(
        ["table", "indent", "header", "value", "expected"],
        [
            [data.table, data.indent, data.header, data.value, data.expected]
            for data in exception_test_data_list
        ])
    def test_exception(self, table, indent, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.set_indent_level(indent)
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table()


class Test_MarkdownTableWriter_write_table_iter(object):

    @pytest.mark.parametrize(["table", "header", "value", "expected"], [
        [
            "tablename",
            ["ha", "hb", "hc"],
            value_matrix_iter,
            """# tablename
| ha | hb | hc |
|---:|---:|---:|
|   1|   2|   3|
|  11|  12|  13|
|   1|   2|   3|
|  11|  12|  13|
| 101| 102| 103|
|1001|1002|1003|

""",
        ],
        [
            "mix length",
            ["string", "hb", "hc"],
            value_matrix_iter_1,
            """# mix length
|           string            | hb  | hc |
|-----------------------------|----:|---:|
|a b c d e f g h i jklmn      |  2.1|   3|
|aaaaa                        | 12.1|  13|
|bbb                          |    2|   3|
|cc                           |   12|  13|
|a                            |  102| 103|
|                             | 1002|1003|

"""
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

        print("[expected]\n{}".format(expected))
        print("[actual]\n{}".format(out))

        assert out == expected

    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [
            [data.table, data.header, data.value, data.expected]
            for data in exception_test_data_list
        ])
    def test_exception(self, table, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table_iter()
