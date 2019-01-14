# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, print_function, unicode_literals

import collections
import re
from textwrap import dedent

import pytablewriter as ptw
import pytest
import six  # noqa: W0611
from pytablewriter.style import Align, FontSize, Style, ThousandSeparator
from tabledata import TableData
from termcolor import colored

from ._common import print_test_result
from .data import (
    float_header_list,
    float_value_matrix,
    header_list,
    mix_header_list,
    mix_value_matrix,
    style_list,
    style_tabledata,
    value_matrix,
    value_matrix_iter,
    value_matrix_iter_1,
    value_matrix_with_none,
)


Data = collections.namedtuple("Data", "table indent header value is_formatting_float expected")

normal_test_data_list = [
    Data(
        table="",
        indent=0,
        header=header_list,
        value=value_matrix,
        is_formatting_float=True,
        expected=dedent(
            """\
            | a |  b  | c |dd | e  |
            |--:|----:|---|--:|----|
            |  1|123.1|a  |1.0|   1|
            |  2|  2.2|bb |2.2| 2.2|
            |  3|  3.3|ccc|3.0|cccc|
            """
        ),
    ),
    Data(
        table="",
        indent=0,
        header=header_list,
        value=None,
        is_formatting_float=True,
        expected=dedent(
            """\
            | a | b | c |dd | e |
            |---|---|---|---|---|
            """
        ),
    ),
    Data(
        table="floating point",
        indent=0,
        header=header_list,
        value=[
            ["1", 123.09999999999999, "a", "1", 1],
            [2, 2.2000000000000002, "bb", "2.2", 2.2000000000000002],
            [3, 3.2999999999999998, "ccc", "3.2999999999999998", "cccc"],
        ],
        is_formatting_float=True,
        expected=dedent(
            """\
            # floating point
            | a |  b  | c |dd | e  |
            |--:|----:|---|--:|----|
            |  1|123.1|a  |1.0|   1|
            |  2|  2.2|bb |2.2| 2.2|
            |  3|  3.3|ccc|3.3|cccc|
            """
        ),
    ),
    Data(
        table="tablename",
        indent=1,
        header=header_list,
        value=value_matrix,
        is_formatting_float=True,
        expected=dedent(
            """\
            ## tablename
            | a |  b  | c |dd | e  |
            |--:|----:|---|--:|----|
            |  1|123.1|a  |1.0|   1|
            |  2|  2.2|bb |2.2| 2.2|
            |  3|  3.3|ccc|3.0|cccc|
            """
        ),
    ),
    Data(
        table="",
        indent=0,
        header=header_list,
        value=value_matrix_with_none,
        is_formatting_float=True,
        expected=dedent(
            """\
            | a | b | c |dd | e  |
            |--:|--:|---|--:|----|
            |  1|   |a  |1.0|    |
            |   |2.2|   |2.2| 2.2|
            |  3|3.3|ccc|   |cccc|
            |   |   |   |   |    |
            """
        ),
    ),
    Data(
        table="",
        indent=0,
        header=mix_header_list,
        value=mix_value_matrix,
        is_formatting_float=True,
        expected=dedent(
            """\
            | i | f  | c  | if |ifc|bool |  inf   |nan|mix_num |          time           |
            |--:|---:|----|---:|---|-----|--------|---|-------:|-------------------------|
            |  1|1.10|aa  | 1.0|  1|True |Infinity|NaN|       1|2017-01-01T00:00:00      |
            |  2|2.20|bbb | 2.2|2.2|False|Infinity|NaN|Infinity|2017-01-02 03:04:05+09:00|
            |  3|3.33|cccc|-3.0|ccc|True |Infinity|NaN|     NaN|2017-01-01T00:00:00      |
            """
        ),
    ),
    Data(
        table="formatting float 1",
        indent=0,
        header=header_list,
        value=value_matrix,
        is_formatting_float=True,
        expected=dedent(
            """\
            # formatting float 1
            | a |  b  | c |dd | e  |
            |--:|----:|---|--:|----|
            |  1|123.1|a  |1.0|   1|
            |  2|  2.2|bb |2.2| 2.2|
            |  3|  3.3|ccc|3.0|cccc|
            """
        ),
    ),
    Data(
        table="formatting float 2",
        indent=0,
        header=float_header_list,
        value=float_value_matrix,
        is_formatting_float=True,
        expected=dedent(
            """\
            # formatting float 2
            | a  |     b     |  c  |
            |---:|----------:|----:|
            |0.01|     0.0012|0.000|
            |1.00|    99.9000|0.010|
            |1.20|999999.1230|0.001|
            """
        ),
    ),
    Data(
        table="not formatting float 1",
        indent=0,
        header=header_list,
        value=value_matrix,
        is_formatting_float=False,
        expected=dedent(
            """\
            # not formatting float 1
            | a |  b  | c |dd | e  |
            |--:|----:|---|--:|----|
            |  1|123.1|a  |  1|   1|
            |  2|  2.2|bb |2.2| 2.2|
            |  3|  3.3|ccc|  3|cccc|
            """
        ),
    ),
    Data(
        table="not formatting float 2",
        indent=0,
        header=float_header_list,
        value=float_value_matrix,
        is_formatting_float=False,
        expected=dedent(
            """\
            # not formatting float 2
            | a  |    b     |  c  |
            |---:|---------:|----:|
            |0.01|   0.00125|    0|
            |   1|      99.9| 0.01|
            | 1.2|999999.123|0.001|
            """
        ),
    ),
    Data(
        table="",
        indent=0,
        header=["Name", "xUnit", "Source", "Remarks"],
        value=[
            [
                "Crotest",
                "",
                "[160]",
                "MIT License. A tiny and simple test framework for Crystal\nwith common assertions and no pollution into Object class.",
                "",
            ]
        ],
        is_formatting_float=True,
        expected=dedent(
            """\
            | Name  |xUnit|Source|                                                      Remarks                                                       |
            |-------|-----|------|--------------------------------------------------------------------------------------------------------------------|
            |Crotest|     |[160] |MIT License. A tiny and simple test framework for Crystal with common assertions and no pollution into Object class.|
            """
        ),
    ),
    Data(
        table="",
        indent=0,
        header=["姓", "名", "生年月日", "郵便番号", "住所", "電話番号"],
        value=[
            ["山田", "太郎", "2001/1/1", "100-0002", "東京都千代田区皇居外苑", "03-1234-5678"],
            ["山田", "次郎", "2001/1/2", "251-0036", "神奈川県藤沢市江の島１丁目", "03-9999-9999"],
        ],
        is_formatting_float=True,
        expected=dedent(
            """\
            | 姓 | 名 |生年月日|郵便番号|           住所           |  電話番号  |
            |----|----|--------|--------|--------------------------|------------|
            |山田|太郎|2001/1/1|100-0002|東京都千代田区皇居外苑    |03-1234-5678|
            |山田|次郎|2001/1/2|251-0036|神奈川県藤沢市江の島１丁目|03-9999-9999|
            """
        ),
    ),
    Data(
        table="quoted values",
        indent=0,
        header=['"quote"', '"abc efg"'],
        value=[['"1"', '"abc"'], ['"-1"', '"efg"']],
        is_formatting_float=True,
        expected=dedent(
            """\
            # quoted values
            |quote|abc efg|
            |----:|-------|
            |    1|abc    |
            |   -1|efg    |
            """
        ),
    ),
    Data(
        table="not str headers",
        indent=0,
        header=[None, 1, 0.1],
        value=[[None, 1, 0.1]],
        is_formatting_float=True,
        expected=dedent(
            """\
            # not str headers
            |   | 1 |0.1|
            |---|--:|--:|
            |   |  1|0.1|
            """
        ),
    ),
    Data(
        table="no uniform matrix",
        indent=0,
        header=["a", "b", "c"],
        value=[["a", 0], ["b", 1, "bb"], ["c", 2, "ccc", 0.1]],
        is_formatting_float=True,
        expected=dedent(
            """\
            # no uniform matrix
            | a | b | c |
            |---|--:|---|
            |a  |  0|   |
            |b  |  1|bb |
            |c  |  2|ccc|
            """
        ),
    ),
    Data(
        table="line breaks",
        indent=0,
        header=["a\nb", "\nc\n\nd\n", "e\r\nf"],
        value=[["v1\nv1", "v2\n\nv2", "v3\r\nv3"]],
        is_formatting_float=True,
        expected=dedent(
            """\
            # line breaks
            | a b | c d | e f |
            |-----|-----|-----|
            |v1 v1|v2 v2|v3 v3|
            """
        ),
    ),
    Data(
        table="empty header",
        indent=0,
        header=[],
        value=value_matrix,
        is_formatting_float=True,
        expected=dedent(
            """\
            # empty header
            | A |  B  | C | D | E  |
            |--:|----:|---|--:|----|
            |  1|123.1|a  |1.0|   1|
            |  2|  2.2|bb |2.2| 2.2|
            |  3|  3.3|ccc|3.0|cccc|
            """
        ),
    ),
    Data(
        table="vertical bar",
        indent=1,
        header=["a|b", "|c||d|"],
        value=[["|v1|v1|", "v2|v2"]],
        is_formatting_float=True,
        expected=r"""## vertical bar
|  a\|b  |\|c\|\|d\||
|-------|------|
|\|v1\|v1\||v2\|v2 |
""",
    ),
    Data(
        table="mixed value types",
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
        expected=dedent(
            """\
            # mixed value types
            |  data   |   v    |
            |---------|-------:|
            |    3.437|   65.54|
            |   65.540|  127.64|
            |  189.744|  189.74|
            |10064.010|10001.91|
            |next     |10250.32|
            """
        ),
    ),
    Data(
        table="list of dict",
        indent=0,
        header=["A", "B", "C"],
        value=[
            {"A": 1},
            {"B": 2.1, "C": "hoge"},
            {"A": 0, "B": 0.1, "C": "foo"},
            {},
            {"A": -1, "B": -0.1, "C": "bar", "D": "extra"},
        ],
        is_formatting_float=False,
        expected=dedent(
            """\
            # list of dict
            | A | B  | C  |
            |--:|---:|----|
            |  1|    |    |
            |   | 2.1|hoge|
            |  0| 0.1|foo |
            |   |    |    |
            | -1|-0.1|bar |
            """
        ),
    ),
]

exception_test_data_list = [
    Data(
        table="",
        indent=0,
        header=[],
        value=[],
        is_formatting_float=True,
        expected=ptw.EmptyTableDataError,
    )
]

table_writer_class = ptw.MarkdownTableWriter


class Test_MarkdownTableWriter_write_new_line(object):
    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_MarkdownTableWriter_write_table(object):
    @pytest.mark.parametrize(
        ["table", "indent", "header", "value", "is_formatting_float", "expected"],
        [
            [
                data.table,
                data.indent,
                data.header,
                data.value,
                data.is_formatting_float,
                data.expected,
            ]
            for data in normal_test_data_list
        ],
    )
    def test_normal(self, capsys, table, indent, header, value, is_formatting_float, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.set_indent_level(indent)
        writer.header_list = header
        writer.value_matrix = value
        writer.is_formatting_float = is_formatting_float
        writer.write_table()

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected
        assert writer.dumps() == expected

    def test_normal_single_tabledata(self, capsys):
        writer = table_writer_class()
        writer.from_tabledata(
            TableData(
                table_name="loader_mapping",
                header_list=["Name", "Loader"],
                row_list=[
                    ["csv", "CsvTableFileLoader"],
                    ["excel", "ExcelTableFileLoader"],
                    ["html", "HtmlTableFileLoader"],
                    ["markdown", "MarkdownTableFileLoader"],
                    ["mediawiki", "MediaWikiTableFileLoader"],
                    ["json", "JsonTableFileLoader"],
                    ["Long Format Name", "Loader"],
                ],
            )
        )
        writer.write_table()

        expected = dedent(
            """\
            # loader_mapping
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
        )

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected

    def test_normal_multiple_write(self, capsys):
        writer = table_writer_class()
        writer.is_write_null_line_after_table = True
        writer.from_tabledata(
            TableData(
                table_name="first",
                header_list=["Name", "Loader"],
                row_list=[["csv", "CsvTableFileLoader"], ["excel", "ExcelTableFileLoader"]],
            )
        )
        writer.write_table()

        writer.from_tabledata(
            TableData(
                table_name="second",
                header_list=["a", "b", "c"],
                row_list=[["1", "AA", "abc"], ["2", "BB", "zzz"]],
            )
        )
        writer.write_table()

        expected = dedent(
            """\
            # first
            |Name |       Loader       |
            |-----|--------------------|
            |csv  |CsvTableFileLoader  |
            |excel|ExcelTableFileLoader|

            # second
            | a | b | c |
            |--:|---|---|
            |  1|AA |abc|
            |  2|BB |zzz|

            """
        )

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected

    def test_normal_style_align(self):
        writer = table_writer_class()
        writer.from_tabledata(
            TableData(
                table_name="auto align",
                header_list=["left", "right", "center", "auto", "auto", "None"],
                row_list=[
                    [0, "r", "center align", 0, "a", "n"],
                    [11, "right align", "bb", 11, "auto", "none (auto)"],
                ],
            )
        )
        expected = dedent(
            """\
            # auto align
            |left|   right   |   center   |auto|auto|   None    |
            |---:|-----------|------------|---:|----|-----------|
            |   0|r          |center align|   0|a   |n          |
            |  11|right align|bb          |  11|auto|none (auto)|
            """
        )
        out = writer.dumps()
        print_test_result(expected=expected, actual=out)
        assert out == expected

        writer.table_name = "specify alignment for each column manually"
        writer.style_list = [
            Style(align=Align.LEFT),
            Style(align=Align.RIGHT),
            Style(align=Align.CENTER),
            Style(align=Align.AUTO),
            Style(align=Align.AUTO),
            None,
        ]
        expected = dedent(
            """\
            # specify alignment for each column manually
            |left|   right   |   center   |auto|auto|   None    |
            |----|----------:|:----------:|---:|----|-----------|
            |0   |          r|center align|   0|a   |n          |
            |11  |right align|     bb     |  11|auto|none (auto)|
            """
        )
        out = writer.dumps()
        print_test_result(expected=expected, actual=out)
        assert out == expected

        # test for backward compatibility
        writer.style_list = None
        writer.align_list = [Align.LEFT, Align.RIGHT, Align.CENTER, Align.AUTO, Align.AUTO, None]
        out = writer.dumps()
        print_test_result(expected=expected, actual=out)
        assert out == expected

    def test_normal_style_thousand_separator(self, capsys):
        writer = table_writer_class()
        writer.from_tabledata(
            TableData(
                table_name="",
                header_list=[
                    "none_format",
                    "thousand_separator_i",
                    "thousand_separator_f",
                    "f",
                    "wo_f",
                ],
                row_list=[
                    [1000, 1234567, 1234567.8, 1234.5678, 1234567.8],
                    [1000, 1234567, 1234567.8, 1234.5678, 1234567.8],
                ],
            )
        )

        writer.style_list = [
            Style(thousand_separator=ThousandSeparator.NONE),
            Style(thousand_separator=ThousandSeparator.COMMA),
            Style(thousand_separator=ThousandSeparator.COMMA),
            Style(thousand_separator=ThousandSeparator.SPACE),
        ]
        out = writer.dumps()
        expected = dedent(
            """\
            |none_format|thousand_separator_i|thousand_separator_f|   f   |  wo_f   |
            |----------:|-------------------:|-------------------:|------:|--------:|
            |       1000|           1,234,567|         1,234,567.8|1 234.6|1234567.8|
            |       1000|           1,234,567|         1,234,567.8|1 234.6|1234567.8|
            """
        )
        print_test_result(expected=expected, actual=out)
        assert out == expected

        writer.style_list = None
        writer.format_list = [
            ptw.Format.NONE,
            ptw.Format.THOUSAND_SEPARATOR,
            ptw.Format.THOUSAND_SEPARATOR,
            ptw.Format.THOUSAND_SEPARATOR,
        ]
        out = writer.dumps()
        expected = dedent(
            """\
            |none_format|thousand_separator_i|thousand_separator_f|   f   |  wo_f   |
            |----------:|-------------------:|-------------------:|------:|--------:|
            |       1000|           1,234,567|         1,234,567.8|1,234.6|1234567.8|
            |       1000|           1,234,567|         1,234,567.8|1,234.6|1234567.8|
            """
        )
        print_test_result(expected=expected, actual=out)
        assert out == expected

    def test_normal_style_font_size(self):
        writer = table_writer_class()
        writer.table_name = "style test: font size will not be affected"
        writer.header_list = ["none", "empty_style", "tiny", "small", "medium", "large"]
        writer.value_matrix = [[111, 111, 111, 111, 111, 111], [1234, 1234, 1234, 1234, 1234, 1234]]
        writer.style_list = [
            None,
            Style(),
            Style(font_size=FontSize.TINY),
            Style(font_size=FontSize.SMALL),
            Style(font_size=FontSize.MEDIUM),
            Style(font_size=FontSize.LARGE),
        ]

        expected = dedent(
            """\
            # style test: font size will not be affected
            |none|empty_style|tiny|small|medium|large|
            |---:|----------:|---:|----:|-----:|----:|
            | 111|        111| 111|  111|   111|  111|
            |1234|       1234|1234| 1234|  1234| 1234|
            """
        )
        out = writer.dumps()
        print_test_result(expected=expected, actual=out)

        assert out == expected

    def test_normal_style_font_weight(self):
        writer = table_writer_class()
        writer.table_name = "style test: bold"
        writer.header_list = ["normal", "bold"]
        writer.value_matrix = [[11, 11], [123456, 123456]]
        writer.style_list = [Style(font_weight="normal"), Style(font_weight="bold")]

        expected = dedent(
            """\
            # style test: bold
            |normal|   bold   |
            |-----:|---------:|
            |    11|    **11**|
            |123456|**123456**|
            """
        )
        out = writer.dumps()
        print_test_result(expected=expected, actual=out)

        assert out == expected

    def test_normal_style_mix(self):
        writer = table_writer_class()
        writer.from_tabledata(style_tabledata)
        writer.style_list = style_list

        expected = dedent(
            """\
            # style test
            |none|empty|tiny|small|medium|large|null w/ bold| L bold |S italic|L bold italic|
            |---:|----:|---:|----:|-----:|----:|------------|-------:|-------:|------------:|
            | 111|  111| 111|  111|   111|  111|            | **111**|   _111_|    _**111**_|
            |1234| 1234|1234| 1234| 1,234|1 234|            |**1234**|  _1234_|   _**1234**_|
            """
        )
        out = writer.dumps()
        print_test_result(expected=expected, actual=out)

        assert out == expected

    def test_normal_set_style(self):
        writer = table_writer_class()
        writer.table_name = "set style method"
        writer.header_list = ["normal", "style by idx", "style by header"]
        writer.value_matrix = [[11, 11, 11], [123456, 123456, 123456]]

        writer.set_style(1, Style(font_weight="bold", thousand_separator=","))
        writer.set_style(
            "style by header", Style(align="center", font_weight="bold", thousand_separator=" ")
        )
        expected = dedent(
            """\
            # set style method
            |normal|style by idx|style by header|
            |-----:|-----------:|:-------------:|
            |    11|      **11**|    **11**     |
            |123456| **123,456**|  **123 456**  |
            """
        )
        output = writer.dumps()
        print_test_result(expected=expected, actual=output)
        assert output == expected

        writer.table_name = "change style"
        writer.set_style(1, Style(align="right", font_style="italic"))
        writer.set_style("style by header", Style())
        expected = dedent(
            """\
            # change style
            |normal|style by idx|style by header|
            |-----:|-----------:|--------------:|
            |    11|        _11_|             11|
            |123456|    _123456_|         123456|
            """
        )
        output = writer.dumps()
        print_test_result(expected=expected, actual=output)
        assert output == expected

    def test_normal_ansi_color(self, capsys):
        writer = table_writer_class()
        writer.table_name = "ANCI escape sequence"
        writer.header_list = ["colored_i", "colored_f", "colored_s", "wo_anci"]
        writer.value_matrix = [
            [colored(111, "red"), colored(1.1, "green"), colored("abc", "blue"), "abc"],
            [colored(0, "red"), colored(0.12, "green"), colored("abcdef", "blue"), "abcdef"],
        ]
        writer.write_table()

        expected = dedent(
            """\
            # ANCI escape sequence
            |colored_i|colored_f|colored_s|wo_anci|
            |--------:|--------:|---------|-------|
            |      111|      1.1|abc      |abc    |
            |        0|     0.12|abcdef   |abcdef |
            """
        )
        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        _ansi_escape = re.compile(r"(\x9b|\x1b\[)[0-?]*[ -\/]*[@-~]", re.IGNORECASE)

        assert _ansi_escape.sub("", out) == expected

    def test_normal_margin_1(self, capsys):
        writer = table_writer_class()
        writer.from_tabledata(
            TableData(table_name="", header_list=header_list, row_list=value_matrix)
        )
        writer.margin = 1
        writer.write_table()

        expected = dedent(
            """\
            |  a  |   b   |  c  | dd  |  e   |
            |----:|------:|-----|----:|------|
            |   1 | 123.1 | a   | 1.0 |    1 |
            |   2 |   2.2 | bb  | 2.2 |  2.2 |
            |   3 |   3.3 | ccc | 3.0 | cccc |
            """
        )

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected

    def test_normal_margin_2(self, capsys):
        writer = table_writer_class()
        writer.from_tabledata(
            TableData(table_name="", header_list=header_list, row_list=value_matrix)
        )
        writer.margin = 2
        writer.write_table()

        expected = dedent(
            """\
            |   a   |    b    |   c   |  dd   |   e    |
            |------:|--------:|-------|------:|--------|
            |    1  |  123.1  |  a    |  1.0  |     1  |
            |    2  |    2.2  |  bb   |  2.2  |   2.2  |
            |    3  |    3.3  |  ccc  |  3.0  |  cccc  |
            """
        )

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected

    def test_normal_value_map(self):
        writer = table_writer_class()
        writer.header_list = ["a", "b"]
        writer.value_matrix = [["foo", True], ["bar", False]]
        writer.value_map = {True: "X", False: ""}

        expected = dedent(
            """\
            | a | b |
            |---|---|
            |foo|X  |
            |bar|   |
            """
        )

        output = writer.dumps()
        print_test_result(expected=expected, actual=output)

        assert output == expected

    def test_normal_avoid_overwrite_stream_by_dumps(self):
        writer = table_writer_class()
        writer.header_list = ["a", "b"]
        writer.value_matrix = [["foo", "bar"]]
        writer.stream = six.StringIO()

        expected = dedent(
            """\
            | a | b |
            |---|---|
            |foo|bar|
            """
        )

        output = writer.dumps()
        print_test_result(expected=expected, actual=output)
        assert output == expected

        print("--------------------")

        writer.write_table()
        output = writer.stream.getvalue()
        print_test_result(expected=expected, actual=output)
        assert output == expected

    @pytest.mark.skipif("six.PY2")
    def test_normal_escape_html_tag(self, capsys):
        writer = table_writer_class()
        writer.header_list = ["no", "text"]
        writer.value_matrix = [[1, "<caption>Table 'formatting for Jupyter Notebook.</caption>"]]
        writer.is_escape_html_tag = True
        writer.write_table()

        expected = dedent(
            """\
            |no |                                   text                                    |
            |--:|---------------------------------------------------------------------------|
            |  1|&lt;caption&gt;Table &#x27;formatting for Jupyter Notebook.&lt;/caption&gt;|
            """
        )

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected

    @pytest.mark.skipif("six.PY2")
    def test_normal_escape_html_tag_from_tabledata(self, capsys):
        writer = table_writer_class()
        writer.from_tabledata(
            TableData(
                table_name="",
                header_list=["no", "text"],
                row_list=[[1, "<caption>Table 'formatting for Jupyter Notebook.</caption>"]],
            )
        )
        writer.is_escape_html_tag = True
        writer.write_table()

        expected = dedent(
            """\
            |no |                                   text                                    |
            |--:|---------------------------------------------------------------------------|
            |  1|&lt;caption&gt;Table &#x27;formatting for Jupyter Notebook.&lt;/caption&gt;|
            """
        )

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected

    @pytest.mark.parametrize(
        ["table", "indent", "header", "value", "expected"],
        [
            [data.table, data.indent, data.header, data.value, data.expected]
            for data in exception_test_data_list
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


class Test_MarkdownTableWriter_write_table_iter(object):
    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [
            [
                "tablename",
                ["ha", "hb", "hc"],
                value_matrix_iter,
                dedent(
                    """\
                    # tablename
                    | ha | hb | hc |
                    |---:|---:|---:|
                    |   1|   2|   3|
                    |  11|  12|  13|
                    |   1|   2|   3|
                    |  11|  12|  13|
                    | 101| 102| 103|
                    |1001|1002|1003|
                    """
                ),
            ],
            [
                "mix length",
                ["string", "hb", "hc"],
                value_matrix_iter_1,
                dedent(
                    """\
                    # mix length
                    |           string            | hb  | hc |
                    |-----------------------------|----:|---:|
                    |a b c d e f g h i jklmn      |  2.1|   3|
                    |aaaaa                        | 12.1|  13|
                    |bbb                          |    2|   3|
                    |cc                           |   12|  13|
                    |a                            |  102| 103|
                    |                             | 1002|1003|
                    """
                ),
            ],
        ],
    )
    def test_normal(self, capsys, table, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.header_list = header
        writer.value_matrix = value
        writer.iteration_length = len(value)
        writer.write_table_iter()

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected

    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [[data.table, data.header, data.value, data.expected] for data in exception_test_data_list],
    )
    def test_exception(self, table, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table_iter()


class Test_MarkdownTableWriter_dump(object):
    def test_normal(self, tmpdir):
        test_filepath = str(tmpdir.join("test.sqlite"))

        writer = table_writer_class()
        writer.header_list = ["a", "b"]
        writer.value_matrix = [["foo", "bar"]]
        writer.dump(test_filepath)

        expected = dedent(
            """\
            | a | b |
            |---|---|
            |foo|bar|
            """
        )

        with open(test_filepath) as f:
            output = f.read()

        print_test_result(expected=expected, actual=output)
        assert output == expected


class Test_MarkdownTableWriter_from_tablib(object):
    def test_normal_multiple_write(self, capsys):
        import tablib

        data = tablib.Dataset()
        data.headers = ["a", "b", "c"]
        data.append(["1", "AA", "abc"])
        data.append(["2", "BB", "zzz"])

        writer = table_writer_class()
        writer.from_tablib(data)
        writer.write_table()

        expected = dedent(
            """\
            | a | b | c |
            |--:|---|---|
            |  1|AA |abc|
            |  2|BB |zzz|
            """
        )

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected


class Test_MarkdownTableWriter_line_break_handling(object):
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            [
                ptw.LineBreakHandling.REPLACE,
                dedent(
                    """\
                    |no |    text    |
                    |--:|------------|
                    |  1|first second|
                    """
                ),
            ],
            [
                ptw.LineBreakHandling.ESCAPE,
                r"""|no |    text     |
|--:|-------------|
|  1|first\nsecond|
""",
            ],
            [
                "escape",
                r"""|no |    text     |
|--:|-------------|
|  1|first\nsecond|
""",
            ],
        ],
    )
    def test_normal_line(self, value, expected):
        writer = table_writer_class()
        writer.header_list = ["no", "text"]
        writer.value_matrix = [[1, "first\nsecond"]]
        writer.line_break_handling = value

        out = writer.dumps()
        print_test_result(expected=expected, actual=out)

        assert out == expected
