"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import collections
import io
from textwrap import dedent
from typing import Optional

import pytest
from tabledata import TableData
from tcolorpy import tcolor

import pytablewriter as ptw
from pytablewriter.style import Align, Cell, FontSize, Style, ThousandSeparator

from ..._common import print_test_result
from ...data import (
    float_header_list,
    float_value_matrix,
    headers,
    mix_header_list,
    mix_value_matrix,
    value_matrix,
    value_matrix_iter,
    value_matrix_iter_1,
    value_matrix_with_none,
    vut_style_tabledata,
    vut_styles,
)
from ._common import regexp_ansi_escape


try:
    import pandas as pd

    SKIP_DATAFRAME_TEST = False
except ImportError:
    SKIP_DATAFRAME_TEST = True


Data = collections.namedtuple("Data", "table indent header value is_formatting_float expected")

normal_test_data_list = [
    Data(
        table="",
        indent=0,
        header=headers,
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
        header=headers,
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
        header=headers,
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
        header=headers,
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
        header=headers,
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
            | i | f  | c  | if |ifc|bool|  inf   |nan|mix_num |          time           |
            |--:|---:|----|---:|---|----|--------|---|-------:|-------------------------|
            |  1|1.10|aa  | 1.0|  1|X   |Infinity|NaN|       1|2017-01-01T00:00:00      |
            |  2|2.20|bbb | 2.2|2.2|    |Infinity|NaN|Infinity|2017-01-02 03:04:05+09:00|
            |  3|3.33|cccc|-3.0|ccc|X   |Infinity|NaN|     NaN|2017-01-01T00:00:00      |
            """
        ),
    ),
    Data(
        table="formatting float 1",
        indent=0,
        header=headers,
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
        header=headers,
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
            | a b | c  d | e f |
            |-----|------|-----|
            |v1 v1|v2  v2|v3 v3|
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
    Data(
        table="",
        indent=0,
        header=[],
        value=[],
        is_formatting_float=True,
        expected="",
    ),
]

table_writer_class = ptw.MarkdownTableWriter


def trans_func(value):
    if value is None:
        return ""
    if value is True:
        return "X"
    if value is False:
        return ""
    return value


class Test_MarkdownTableWriter_write_new_line:
    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_MarkdownTableWriter_constructor:
    def test_normal_kwargs(self):
        writer = table_writer_class(
            headers=["w/ strike", "w/ line through"],
            value_matrix=[["strike", "line-through"]],
            column_styles=[
                Style(decoration_line="strike"),
                Style(decoration_line="line-through"),
            ],
        )

        expected = dedent(
            """\
            |w/ strike|w/ line through|
            |---------|---------------|
            |strike   |line-through   |
            """
        )

        out = str(writer)
        print_test_result(expected=expected, actual=out)

        assert regexp_ansi_escape.search(out)
        assert regexp_ansi_escape.sub("", out) == expected


class Test_MarkdownTableWriter_repr:
    def test_normal_empty(self):
        writer = table_writer_class()
        assert str(writer).strip() == ""

    def test_normal_ansi(self):
        writer = table_writer_class()
        writer.column_styles = [
            Style(decoration_line="strike"),
            Style(decoration_line="line-through"),
        ]
        writer.headers = ["w/ strike", "w/ line through"]
        writer.value_matrix = [["strike", "line-through"]]

        expected = dedent(
            """\
            |w/ strike|w/ line through|
            |---------|---------------|
            |strike   |line-through   |
            """
        )

        out = str(writer)
        print_test_result(expected=expected, actual=out)

        assert regexp_ansi_escape.search(out)
        assert regexp_ansi_escape.sub("", out) == expected


class Test_MarkdownTableWriter_table_format:
    def test_normal(self):
        assert table_writer_class().table_format is ptw.TableFormat.MARKDOWN


class Test_MarkdownTableWriter_write_table:
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
        writer = table_writer_class(
            table_name=table,
            headers=header,
            value_matrix=value,
            is_formatting_float=is_formatting_float,
        )
        """
        writer.table_name = table
        writer.set_indent_level(indent)
        writer.headers = header
        writer.value_matrix = value
        writer.is_formatting_float = is_formatting_float
        """
        writer.set_indent_level(indent)
        writer.register_trans_func(trans_func)
        writer.write_table()

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected
        assert writer.dumps() == expected
        assert str(writer) == expected

        writer = table_writer_class(
            table_name=table,
            headers=header,
            value_matrix=value,
            indent_level=indent,
            is_formatting_float=is_formatting_float,
        )
        writer.register_trans_func(trans_func)
        assert writer.dumps() == expected

    def test_normal_single_tabledata(self, capsys):
        writer = table_writer_class()
        writer.from_tabledata(
            TableData(
                "loader_mapping",
                ["Name", "Loader"],
                [
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
        writer = table_writer_class(is_write_null_line_after_table=True)
        writer.from_tabledata(
            TableData(
                "first",
                ["Name", "Loader"],
                [["csv", "CsvTableFileLoader"], ["excel", "ExcelTableFileLoader"]],
            )
        )
        writer.write_table()

        writer.from_tabledata(
            TableData("second", ["a", "b", "c"], [["1", "AA", "abc"], ["2", "BB", "zzz"]])
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
                "auto align",
                ["left", "right", "center", "auto", "auto", "None"],
                [
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
        writer.column_styles = [
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

    def test_normal_style_thousand_separator(self, capsys):
        writer = table_writer_class()
        writer.from_tabledata(
            TableData(
                "",
                ["none_format", "thousand_separator_i", "thousand_separator_f", "f", "wo_f"],
                [
                    [1000, 1234567, 1234567.8, 1234.5678, 1234567.8],
                    [1000, 1234567, 1234567.8, 1234.5678, 1234567.8],
                ],
            )
        )

        writer.column_styles = [
            Style(thousand_separator=ThousandSeparator.NONE),
            Style(thousand_separator=ThousandSeparator.COMMA),
            Style(thousand_separator=ThousandSeparator.UNDERSCORE),
            Style(thousand_separator=ThousandSeparator.SPACE),
        ]
        out = writer.dumps()
        expected = dedent(
            """\
            |none_format|thousand_separator_i|thousand_separator_f|   f   |  wo_f   |
            |----------:|-------------------:|-------------------:|------:|--------:|
            |       1000|           1,234,567|         1_234_567.8|1 234.6|1234567.8|
            |       1000|           1,234,567|         1_234_567.8|1 234.6|1234567.8|
            """
        )
        print_test_result(expected=expected, actual=out)
        assert out == expected

    def test_normal_style_font_size(self):
        writer = table_writer_class()
        writer.table_name = "style test: font size will not be affected"
        writer.headers = ["none", "empty_style", "tiny", "small", "medium", "large"]
        writer.value_matrix = [[111, 111, 111, 111, 111, 111], [1234, 1234, 1234, 1234, 1234, 1234]]
        writer.column_styles = [
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
        writer.headers = ["normal", "bold"]
        writer.value_matrix = [[11, 11], [123456, 123456]]
        writer.column_styles = [Style(font_weight="normal"), Style(font_weight="bold")]

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

        assert regexp_ansi_escape.search(out)
        assert regexp_ansi_escape.sub("", out) == expected

    def test_normal_style_mix(self):
        writer = table_writer_class(column_styles=vut_styles)
        writer.from_tabledata(vut_style_tabledata)

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

        assert regexp_ansi_escape.search(out)
        assert regexp_ansi_escape.sub("", out) == expected

    def test_normal_style_filter(self):
        def style_filter(cell: Cell, **kwargs) -> Optional[Style]:
            if isinstance(cell.value, int):
                return Style(align="left")

            if cell.value == "c":
                return Style(align="center")

            if cell.value == "r":
                return Style(align="right")

            return None

        writer = table_writer_class(
            table_name="style filter",
            headers=["left", "center", "right", "overwrite l", "overwrite c", "overwrite r"],
            value_matrix=[
                [1, "c", "r", 1, "c", "r"],
                [2.2, "left", "left", 2.2, "right", "center"],
            ],
            margin=1,
            column_styles=[
                None,
                None,
                None,
                Style(align="center"),
                Style(align="right"),
                Style(align="center"),
            ],
        )
        output_wo_theme = writer.dumps()

        writer.add_style_filter(style_filter)

        expected = dedent(
            """\
            # style filter
            | left | center | right | overwrite l | overwrite c | overwrite r |
            | ---: | ------ | ----- | :---------: | ----------: | :---------: |
            | 1.0  |   c    |     r | 1.0         |      c      |           r |
            |  2.2 | left   | left  |     2.2     |       right |   center    |
            """
        )
        output_w_theme = writer.dumps()
        print_test_result(expected=expected, actual=output_w_theme)

        assert output_w_theme != output_wo_theme
        assert output_w_theme == expected

        assert (
            table_writer_class(
                table_name="style filter",
                headers=["left", "center", "right", "overwrite l", "overwrite c", "overwrite r"],
                value_matrix=[
                    [1, "c", "r", 1, "c", "r"],
                    [2.2, "left", "left", 2.2, "right", "center"],
                ],
                margin=1,
                column_styles=[
                    None,
                    None,
                    None,
                    Style(align="center"),
                    Style(align="right"),
                    Style(align="center"),
                ],
            ).dumps()
            == output_wo_theme
        )

    def test_normal_clear_theme(self):
        writer = table_writer_class()
        writer.table_name = "style test: bold"
        writer.headers = ["normal", "bold"]
        writer.value_matrix = [[11, 11], [123456, 123456]]
        out_wo_theme = writer.dumps()

        writer.set_theme("altrow")
        out_w_theme = writer.dumps()
        assert out_w_theme != out_wo_theme

        # set theme at constructor
        writer = table_writer_class(
            table_name="style test: bold",
            headers=["normal", "bold"],
            value_matrix=[[11, 11], [123456, 123456]],
            theme="altrow",
        )
        assert writer.dumps() == out_w_theme

        writer.clear_theme()
        out_wo_theme = writer.dumps()
        assert out_w_theme != out_wo_theme
        assert regexp_ansi_escape.search(out_wo_theme) is None

    def test_except_set_theme(self):
        writer = table_writer_class()

        with pytest.raises(RuntimeError):
            writer.set_theme("not_existing_theme")

    def test_normal_set_style(self):
        writer = table_writer_class(
            table_name="set style method",
            headers=["normal", "style by idx", "style by header"],
            value_matrix=[[11, 11, 11], [123456, 123456, 123456]],
        )

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
        assert regexp_ansi_escape.search(output)
        assert regexp_ansi_escape.sub("", output) == expected

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
        assert regexp_ansi_escape.sub("", output) == expected

    def test_normal_ansi_color(self, capsys):
        writer = table_writer_class()
        writer.table_name = "ANCI escape sequence"
        writer.headers = ["colored_i", "colored_f", "colored_s", "wo_anci"]
        writer.value_matrix = [
            [
                tcolor("111", color="red"),
                tcolor("1.1", color="green"),
                tcolor("abc", color="blue"),
                "abc",
            ],
            [
                tcolor("0", color="red"),
                tcolor("0.12", color="green"),
                tcolor("abcdef", color="blue"),
                "abcdef",
            ],
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

        assert regexp_ansi_escape.search(out)
        assert regexp_ansi_escape.sub("", out) == expected

    def test_normal_ansi_style(self):
        writer = table_writer_class(
            headers=["w/ strike", "w/ line through"],
            value_matrix=[["strike", "line-through"]],
            column_styles=[
                Style(decoration_line="strike"),
                Style(decoration_line="line-through"),
            ],
        )

        expected = dedent(
            """\
            |w/ strike|w/ line through|
            |---------|---------------|
            |strike   |line-through   |
            """
        )

        out = writer.dumps()
        print_test_result(expected=expected, actual=out)

        assert regexp_ansi_escape.search(out)
        assert regexp_ansi_escape.sub("", out) == expected

    def test_normal_colorize_terminal(self):
        column_styles = [
            Style(color="red"),
            Style(bg_color="white"),
        ]
        writer = table_writer_class(
            column_styles=column_styles,
            headers=["fg color", "bg color"],
            value_matrix=[["hoge", "foo"]],
            colorize_terminal=True,
        )

        out = writer.dumps()
        assert regexp_ansi_escape.search(out)
        assert (
            table_writer_class(
                headers=["fg color", "bg color"],
                value_matrix=[["hoge", "foo"]],
                column_styles=column_styles,
                colorize_terminal=True,
            ).dumps()
            == out
        )

        writer.colorize_terminal = False
        out = writer.dumps()
        assert regexp_ansi_escape.search(out) is None
        assert (
            table_writer_class(
                headers=["fg color", "bg color"],
                value_matrix=[["hoge", "foo"]],
                column_styles=column_styles,
                colorize_terminal=False,
            ).dumps()
            == out
        )

    def test_normal_enable_ansi_escape(self):
        writer = table_writer_class(
            column_styles=[
                Style(font_weight="bold"),
                Style(decoration_line="line-through"),
            ],
            headers=["w/ bold", "w/ line through"],
            value_matrix=[["hoge", "foo"]],
            colorize_terminal=True,
            enable_ansi_escape=True,
        )

        out = writer.dumps()
        assert regexp_ansi_escape.search(out)

        writer.enable_ansi_escape = False
        out = writer.dumps()
        assert regexp_ansi_escape.search(out) is None

        writer.colorize_terminal = False
        writer.enable_ansi_escape = True
        out = writer.dumps()
        assert regexp_ansi_escape.search(out)

    def test_normal_margin_1(self, capsys):
        writer = table_writer_class(margin=1)
        writer.from_tabledata(TableData("", headers, value_matrix))
        writer.write_table()

        expected = dedent(
            """\
            |  a  |   b   |  c  | dd  |  e   |
            | --: | ----: | --- | --: | ---- |
            |   1 | 123.1 | a   | 1.0 |    1 |
            |   2 |   2.2 | bb  | 2.2 |  2.2 |
            |   3 |   3.3 | ccc | 3.0 | cccc |
            """
        )

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected

    def test_normal_margin_2(self, capsys):
        writer = table_writer_class(margin=2)
        writer.from_tabledata(TableData("", headers, value_matrix))
        writer.write_table()

        expected = dedent(
            """\
            |   a   |    b    |   c   |  dd   |   e    |
            |  --:  |  ----:  |  ---  |  --:  |  ----  |
            |    1  |  123.1  |  a    |  1.0  |     1  |
            |    2  |    2.2  |  bb   |  2.2  |   2.2  |
            |    3  |    3.3  |  ccc  |  3.0  |  cccc  |
            """
        )

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected

    def test_normal_register_trans_func(self):
        writer = table_writer_class(
            headers=["a", "b"], value_matrix=[["foo", True], ["bar", False]]
        )
        writer.register_trans_func(trans_func)

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

    def test_normal_flavor(self):
        writer = table_writer_class(
            enable_ansi_escape=False,
            column_styles=[
                None,
                Style(decoration_line="strike"),
                Style(decoration_line="line-through"),
            ],
            headers=["w/o style", "w/ strike", "w/ line through"],
            value_matrix=[["no", "strike", "line-through"]],
        )

        expected = dedent(
            """\
            |w/o style|w/ strike |w/ line through |
            |---------|----------|----------------|
            |no       |~~strike~~|~~line-through~~|
            """
        )

        output = writer.dumps(flavor="gfm")
        print_test_result(expected=expected, actual=output)

        assert output == expected

    def test_normal_avoid_overwrite_stream_by_dumps(self):
        writer = table_writer_class(headers=["a", "b"], value_matrix=[["foo", "bar"]])
        writer.stream = io.StringIO()

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

    def test_normal_escape_html_tag(self, capsys):
        writer = table_writer_class(
            headers=["no", "text"],
            value_matrix=[[1, "<caption>Table 'formatting for Jupyter Notebook.</caption>"]],
        )
        writer.update_preprocessor(is_escape_html_tag=True)
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

    def test_normal_escape_html_tag_from_tabledata(self, capsys):
        writer = table_writer_class()
        writer.from_tabledata(
            TableData(
                "",
                ["no", "text"],
                [[1, "<caption>Table 'formatting for Jupyter Notebook.</caption>"]],
            )
        )
        writer.update_preprocessor(is_escape_html_tag=True)
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


class Test_MarkdownTableWriter_write_table_iter:
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
        writer = table_writer_class(
            table_name=table, headers=header, value_matrix=value, iteration_length=len(value)
        )
        writer.write_table_iter()

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected


class Test_MarkdownTableWriter_dump:
    def test_normal(self, tmpdir):
        test_filepath = str(tmpdir.join("test.sqlite"))

        writer = table_writer_class(
            headers=["a", "b"],
            value_matrix=[["foo", "bar"]],
            column_styles=[
                Style(color="red"),
                Style(bg_color="white"),
            ],
        )
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


class Test_MarkdownTableWriter_from_writer:
    def test_normal(self):
        writer_rhs = table_writer_class()
        writer_rhs.from_tabledata(
            TableData(
                "loader_mapping",
                ["Name", "Loader"],
                [
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
        rhs = writer_rhs.dumps()

        writer_lhs = table_writer_class()
        writer_lhs.from_writer(writer_rhs)
        lhs = writer_lhs.dumps()

        print_test_result(expected=lhs, actual=rhs)

        assert lhs == rhs


class Test_MarkdownTableWriter_from_tablib:
    def test_normal_multiple_write(self, capsys):
        try:
            import tablib
        except ImportError:
            pytest.skip("requires tablib")

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


class Test_MarkdownTableWriter_line_break_handling:
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
        writer = table_writer_class(headers=["no", "text"], value_matrix=[[1, "first\nsecond"]])
        writer.update_preprocessor(line_break_handling=value)

        out = writer.dumps()
        print_test_result(expected=expected, actual=out)

        assert out == expected


@pytest.mark.skipif(SKIP_DATAFRAME_TEST, reason="required package not found")
class Test_MarkdownTableWriter_from_dataframe:
    @pytest.mark.parametrize(
        ["add_index_column", "expected"],
        [
            [
                False,
                dedent(
                    """\
                    # add_index_column: False
                    | A | B |
                    |--:|--:|
                    |  1| 10|
                    |  2| 11|
                    """
                ),
            ],
            [
                True,
                dedent(
                    """\
                    # add_index_column: True
                    |   | A | B |
                    |---|--:|--:|
                    |a  |  1| 10|
                    |b  |  2| 11|
                    """
                ),
            ],
        ],
    )
    def test_normal(self, tmpdir, add_index_column, expected):
        writer = table_writer_class(table_name=f"add_index_column: {add_index_column}")
        df = pd.DataFrame({"A": [1, 2], "B": [10, 11]}, index=["a", "b"])

        writer.from_dataframe(df, add_index_column=add_index_column)
        out = writer.dumps()
        print_test_result(expected=expected, actual=out)
        assert out == expected

        # pickle test
        df_pkl_filepath = str(tmpdir.join("df.pkl"))
        df.to_pickle(df_pkl_filepath)

        writer.from_dataframe(df_pkl_filepath, add_index_column=add_index_column)
        out = writer.dumps()
        print_test_result(expected=expected, actual=out)
        assert out == expected


@pytest.mark.skipif(SKIP_DATAFRAME_TEST, reason="required package not found")
class Test_MarkdownTableWriter_from_series:
    @pytest.mark.parametrize(
        ["add_index_column", "expected"],
        [
            [
                False,
                dedent(
                    """\
                    # add_index_column: False
                    |value |
                    |-----:|
                    |100.00|
                    | 49.50|
                    | 29.01|
                    |  0.00|
                    | 24.75|
                    | 49.50|
                    | 74.25|
                    | 99.00|
                    """
                ),
            ],
            [
                True,
                dedent(
                    """\
                    # add_index_column: True
                    |     |value |
                    |-----|-----:|
                    |count|100.00|
                    |mean | 49.50|
                    |std  | 29.01|
                    |min  |  0.00|
                    |25%  | 24.75|
                    |50%  | 49.50|
                    |75%  | 74.25|
                    |max  | 99.00|
                    """
                ),
            ],
        ],
    )
    def test_normal(self, add_index_column, expected):
        writer = table_writer_class(table_name=f"add_index_column: {add_index_column}")

        writer.from_series(
            pd.Series(list(range(100))).describe(), add_index_column=add_index_column
        )
        out = writer.dumps()
        print_test_result(expected=expected, actual=out)
        assert out == expected
