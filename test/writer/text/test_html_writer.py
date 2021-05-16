"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from textwrap import dedent

import pytest

import pytablewriter
from pytablewriter.style import Style

from ..._common import print_test_result
from ...data import (
    Data,
    headers,
    mix_header_list,
    mix_value_matrix,
    null_test_data_list,
    value_matrix,
    value_matrix_with_none,
    vut_style_tabledata,
    vut_styles,
)


normal_test_data_list = [
    Data(
        table="",
        indent="  ",
        header=headers,
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
""",
    ),
    Data(
        table=None,
        indent="  ",
        header=None,
        value=value_matrix,
        expected="""<table>
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
""",
    ),
    Data(
        table="tablename",
        indent="    ",
        header=headers,
        value=[],
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
    <tbody></tbody>
</table>
""",
    ),
    Data(
        table=None,
        indent="    ",
        header=headers,
        value=None,
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
    <tbody></tbody>
</table>
""",
    ),
    Data(
        table="",
        indent="  ",
        header=headers,
        value=value_matrix_with_none,
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
      <td align="right"></td>
      <td align="left">a</td>
      <td align="right">1.0</td>
      <td align="left"></td>
    </tr>
    <tr>
      <td align="right"></td>
      <td align="right">2.2</td>
      <td align="left"></td>
      <td align="right">2.2</td>
      <td align="right">2.2</td>
    </tr>
    <tr>
      <td align="right">3</td>
      <td align="right">3.3</td>
      <td align="left">ccc</td>
      <td align="right"></td>
      <td align="left">cccc</td>
    </tr>
    <tr>
      <td align="right"></td>
      <td align="right"></td>
      <td align="left"></td>
      <td align="right"></td>
      <td align="left"></td>
    </tr>
  </tbody>
</table>
""",
    ),
    Data(
        table="tablename",
        indent="    ",
        header=mix_header_list,
        value=mix_value_matrix,
        expected="""<table id="tablename">
    <caption>tablename</caption>
    <thead>
        <tr>
            <th>i</th>
            <th>f</th>
            <th>c</th>
            <th>if</th>
            <th>ifc</th>
            <th>bool</th>
            <th>inf</th>
            <th>nan</th>
            <th>mix_num</th>
            <th>time</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="right">1</td>
            <td align="right">1.10</td>
            <td align="left">aa</td>
            <td align="right">1.0</td>
            <td align="right">1</td>
            <td align="left">True</td>
            <td align="left">Infinity</td>
            <td align="left">NaN</td>
            <td align="right">1</td>
            <td align="left">2017-01-01T00:00:00</td>
        </tr>
        <tr>
            <td align="right">2</td>
            <td align="right">2.20</td>
            <td align="left">bbb</td>
            <td align="right">2.2</td>
            <td align="right">2.2</td>
            <td align="left">False</td>
            <td align="left">Infinity</td>
            <td align="left">NaN</td>
            <td align="right">Infinity</td>
            <td align="left">2017-01-02 03:04:05+09:00</td>
        </tr>
        <tr>
            <td align="right">3</td>
            <td align="right">3.33</td>
            <td align="left">cccc</td>
            <td align="right">-3.0</td>
            <td align="left">ccc</td>
            <td align="left">True</td>
            <td align="left">Infinity</td>
            <td align="left">NaN</td>
            <td align="right">NaN</td>
            <td align="left">2017-01-01T00:00:00</td>
        </tr>
    </tbody>
</table>
""",
    ),
]

table_writer_class = pytablewriter.HtmlTableWriter


class Test_HtmlTableWriter_write_new_line:
    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_HtmlTableWriter_write_table:
    @pytest.mark.parametrize(
        ["table", "indent", "header", "value", "expected"],
        [
            [data.table, data.indent, data.header, data.value, data.expected]
            for data in normal_test_data_list
        ],
    )
    def test_normal(self, capsys, table, indent, header, value, expected):
        writer = table_writer_class(
            table_name=table, indent_string=indent, headers=header, value_matrix=value
        )
        writer.write_table()

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected
        assert writer.dumps() == expected
        assert str(writer) == expected

    def test_normal_styles(self, capsys):
        writer = table_writer_class(column_styles=vut_styles)
        writer.from_tabledata(vut_style_tabledata)
        writer.write_table()

        expected = dedent(
            """\
            <table id="styletest">
                <caption>style test</caption>
                <thead>
                    <tr>
                        <th>none</th>
                        <th>empty</th>
                        <th>tiny</th>
                        <th>small</th>
                        <th>medium</th>
                        <th>large</th>
                        <th>null w/ bold</th>
                        <th>L bold</th>
                        <th>S italic</th>
                        <th>L bold italic</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td align="right">111</td>
                        <td align="right">111</td>
                        <td align="right" style="font-size:x-small">111</td>
                        <td align="right" style="font-size:small">111</td>
                        <td align="right" style="font-size:medium">111</td>
                        <td align="right" style="font-size:large">111</td>
                        <td align="left" style="font-weight:bold"></td>
                        <td align="right" style="font-size:large; font-weight:bold">111</td>
                        <td align="right" style="font-size:small; font-style:italic">111</td>
                        <td align="right" style="font-size:large; font-weight:bold; font-style:italic">111</td>
                    </tr>
                    <tr>
                        <td align="right">1234</td>
                        <td align="right">1234</td>
                        <td align="right" style="font-size:x-small">1234</td>
                        <td align="right" style="font-size:small">1234</td>
                        <td align="right" style="font-size:medium">1,234</td>
                        <td align="right" style="font-size:large">1 234</td>
                        <td align="left" style="font-weight:bold"></td>
                        <td align="right" style="font-size:large; font-weight:bold">1234</td>
                        <td align="right" style="font-size:small; font-style:italic">1234</td>
                        <td align="right" style="font-size:large; font-weight:bold; font-style:italic">1234</td>
                    </tr>
                </tbody>
            </table>
            """
        )

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)
        assert out == expected

        print("----- _repr_html_ -----")
        out = writer._repr_html_()
        print_test_result(expected=expected, actual=out)
        assert out == expected

    def test_normal_valign(self, capsys):
        writer = table_writer_class(
            table_name="vertical-align",
            headers=[
                "",
                "top",
                "middle",
                "bottom",
                "top-right",
                "middle-right",
                "bottom-right",
            ],
            value_matrix=[
                ["te\nst", "x", "x", "x", "x", "x", "x"],
            ],
            column_styles=[
                Style(vertical_align="baseline"),
                Style(vertical_align="top"),
                Style(vertical_align="middle"),
                Style(vertical_align="bottom"),
                Style(align="right", vertical_align="top"),
                Style(align="right", vertical_align="middle"),
                Style(align="right", vertical_align="bottom"),
            ],
        )

        writer.write_table()

        expected = """\
<table id="verticalalign">
    <caption>vertical-align</caption>
    <thead>
        <tr>
            <th></th>
            <th>top</th>
            <th>middle</th>
            <th>bottom</th>
            <th>top-right</th>
            <th>middle-right</th>
            <th>bottom-right</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="left">te<br>st</td>
            <td align="left" valign="top">x</td>
            <td align="left" valign="middle">x</td>
            <td align="left" valign="bottom">x</td>
            <td align="right" valign="top">x</td>
            <td align="right" valign="middle">x</td>
            <td align="right" valign="bottom">x</td>
        </tr>
    </tbody>
</table>
"""
        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)
        assert out == expected

    def test_normal_line_breaks(self, capsys):
        writer = table_writer_class(
            table_name="line breaks",
            headers=["a\nb", "\nc\n\nd\n", "e\r\nf"],
            value_matrix=[["v1\nv1", "v2\n\nv2", "v3\r\nv3"]],
        )
        writer.write_table()

        expected = """\
<table id="linebreaks">
    <caption>line breaks</caption>
    <thead>
        <tr>
            <th>a<br>b</th>
            <th><br>c<br><br>d<br></th>
            <th>e<br>f</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="left">v1<br>v1</td>
            <td align="left">v2<br><br>v2</td>
            <td align="left">v3<br>v3</td>
        </tr>
    </tbody>
</table>
"""
        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)
        assert out == expected

    def test_normal_none_values(self, capsys):
        writer = table_writer_class()
        writer.table_name = "none value"
        writer.headers = ["none"]
        writer.value_matrix = [[None]]
        writer.write_table()

        expected = """\
<table id="nonevalue">
    <caption>none value</caption>
    <thead>
        <tr>
            <th>none</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="left"></td>
        </tr>
    </tbody>
</table>
"""
        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)
        assert out == expected

    def test_normal_write_css(self, capsys):
        writer = table_writer_class()
        writer.table_name = "Write HTML with CSS"
        writer.headers = ["int"]
        writer.value_matrix = [[1]]
        writer.write_table(write_css=True)

        expected = """\
<style type="text/css">
    .Write-HTML-with-CSS-css thead th:nth-child(1) {
        text-align: left;
    }
    .Write-HTML-with-CSS-css tbody tr:nth-child(1) td:nth-child(1) {
        text-align: right;
    }
</style>
<table class="Write-HTML-with-CSS-css" id="WriteHTMLwithCSS">
    <caption>Write HTML with CSS</caption>
    <thead>
        <tr>
            <th>int</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
        </tr>
    </tbody>
</table>
"""
        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)
        assert out == expected

    @pytest.mark.parametrize(
        ["table", "indent", "header", "value", "expected"],
        [
            [data.table, data.indent, data.header, data.value, data.expected]
            for data in null_test_data_list
        ],
    )
    def test_normal_empty(self, table, indent, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.indent_string = indent
        writer.headers = header
        writer.value_matrix = value

        assert writer.dumps() == ""


class Test_HtmlTableWriter_write_table_iter:
    def test_exception(self):
        writer = table_writer_class()

        with pytest.raises(pytablewriter.NotSupportedError):
            writer.write_table_iter()
