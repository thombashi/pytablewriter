"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from textwrap import dedent

import pytest

import pytablewriter as ptw
from pytablewriter.style import Style

from ..._common import print_test_result
from ...data import null_test_data_list, vut_style_tabledata, vut_styles


table_writer_class = ptw.CssTableWriter


class Test_CssTableWriter_table_format:
    def test_normal(self):
        assert table_writer_class().table_format is ptw.TableFormat.CSS


class Test_CssTableWriter_write_new_line:
    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_CssTableWriter_write_table:
    def test_normal_styles(self, capsys):
        writer = table_writer_class()
        writer.from_tabledata(vut_style_tabledata)
        writer.column_styles = vut_styles
        writer.write_table()

        expected = dedent(
            """\
.style-test thead th:nth-child(1) {
    text-align: left;
}
.style-test thead th:nth-child(2) {
    text-align: left;
}
.style-test thead th:nth-child(3) {
    text-align: left;
}
.style-test thead th:nth-child(4) {
    text-align: left;
}
.style-test thead th:nth-child(5) {
    text-align: left;
}
.style-test thead th:nth-child(6) {
    text-align: left;
}
.style-test thead th:nth-child(7) {
    font-weight:bold;
    text-align: left;
}
.style-test thead th:nth-child(8) {
    font-weight:bold;
    text-align: left;
}
.style-test thead th:nth-child(9) {
    font-style:italic;
    text-align: left;
}
.style-test thead th:nth-child(10) {
    font-weight:bold;
    font-style:italic;
    text-align: left;
}
.style-test tbody tr:nth-child(1) td:nth-child(1) {
    text-align: right;
}
.style-test tbody tr:nth-child(1) td:nth-child(2) {
    text-align: right;
}
.style-test tbody tr:nth-child(1) td:nth-child(3) {
    text-align: right;
}
.style-test tbody tr:nth-child(1) td:nth-child(4) {
    text-align: right;
}
.style-test tbody tr:nth-child(1) td:nth-child(5) {
    text-align: right;
}
.style-test tbody tr:nth-child(1) td:nth-child(6) {
    text-align: right;
}
.style-test tbody tr:nth-child(1) td:nth-child(7) {
    font-weight:bold;
    text-align: left;
}
.style-test tbody tr:nth-child(1) td:nth-child(8) {
    font-weight:bold;
    text-align: right;
}
.style-test tbody tr:nth-child(1) td:nth-child(9) {
    font-style:italic;
    text-align: right;
}
.style-test tbody tr:nth-child(1) td:nth-child(10) {
    font-weight:bold;
    font-style:italic;
    text-align: right;
}
.style-test tbody tr:nth-child(2) td:nth-child(1) {
    text-align: right;
}
.style-test tbody tr:nth-child(2) td:nth-child(2) {
    text-align: right;
}
.style-test tbody tr:nth-child(2) td:nth-child(3) {
    text-align: right;
}
.style-test tbody tr:nth-child(2) td:nth-child(4) {
    text-align: right;
}
.style-test tbody tr:nth-child(2) td:nth-child(5) {
    text-align: right;
}
.style-test tbody tr:nth-child(2) td:nth-child(6) {
    text-align: right;
}
.style-test tbody tr:nth-child(2) td:nth-child(7) {
    font-weight:bold;
    text-align: left;
}
.style-test tbody tr:nth-child(2) td:nth-child(8) {
    font-weight:bold;
    text-align: right;
}
.style-test tbody tr:nth-child(2) td:nth-child(9) {
    font-style:italic;
    text-align: right;
}
.style-test tbody tr:nth-child(2) td:nth-child(10) {
    font-weight:bold;
    font-style:italic;
    text-align: right;
}
"""
        )

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)
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
.vertical-align thead th:nth-child(1) {
    text-align: left;
}
.vertical-align thead th:nth-child(2) {
    text-align: left;
    vertical-align: top;
}
.vertical-align thead th:nth-child(3) {
    text-align: left;
    vertical-align: middle;
}
.vertical-align thead th:nth-child(4) {
    text-align: left;
    vertical-align: bottom;
}
.vertical-align thead th:nth-child(5) {
    text-align: right;
    vertical-align: top;
}
.vertical-align thead th:nth-child(6) {
    text-align: right;
    vertical-align: middle;
}
.vertical-align thead th:nth-child(7) {
    text-align: right;
    vertical-align: bottom;
}
.vertical-align tbody tr:nth-child(1) td:nth-child(1) {
    text-align: left;
}
.vertical-align tbody tr:nth-child(1) td:nth-child(2) {
    text-align: left;
    vertical-align: top;
}
.vertical-align tbody tr:nth-child(1) td:nth-child(3) {
    text-align: left;
    vertical-align: middle;
}
.vertical-align tbody tr:nth-child(1) td:nth-child(4) {
    text-align: left;
    vertical-align: bottom;
}
.vertical-align tbody tr:nth-child(1) td:nth-child(5) {
    text-align: right;
    vertical-align: top;
}
.vertical-align tbody tr:nth-child(1) td:nth-child(6) {
    text-align: right;
    vertical-align: middle;
}
.vertical-align tbody tr:nth-child(1) td:nth-child(7) {
    text-align: right;
    vertical-align: bottom;
}
"""
        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)
        assert out == expected

    def test_normal_write_style_tag(self, capsys):
        writer = table_writer_class(
            table_name="none value", headers=["none"], value_matrix=[[None]]
        )
        writer.write_table(write_style_tag=True)
        expected = """\
<style type="text/css">
    .none-value thead th:nth-child(1) {
        text-align: left;
    }
    .none-value tbody tr:nth-child(1) td:nth-child(1) {
        text-align: left;
    }
</style>
"""
        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)
        assert out == expected

    def test_normal_flavor(self):
        writer = table_writer_class()
        writer.table_name = "decoration line"
        writer.column_styles = [
            Style(decoration_line="underline"),
            Style(decoration_line="strike"),
            Style(decoration_line="line-through"),
        ]
        writer.headers = ["w/o style", "w/ strike", "w/ line through"]
        writer.value_matrix = [["u", "s", "lt"]]

        expected = """\
.decoration-line thead th:nth-child(1) {
    text-align: left;
    text-decoration-line: underline;
}
.decoration-line thead th:nth-child(2) {
    text-align: left;
    text-decoration-line: line-through;
}
.decoration-line thead th:nth-child(3) {
    text-align: left;
    text-decoration-line: line-through;
}
.decoration-line tbody tr:nth-child(1) td:nth-child(1) {
    text-align: left;
    text-decoration-line: underline;
}
.decoration-line tbody tr:nth-child(1) td:nth-child(2) {
    text-align: left;
    text-decoration-line: line-through;
}
.decoration-line tbody tr:nth-child(1) td:nth-child(3) {
    text-align: left;
    text-decoration-line: line-through;
}
"""

        output = writer.dumps()
        print_test_result(expected=expected, actual=output)

        assert output == expected

    def test_normal_dumps(self):
        writer = table_writer_class()
        writer.table_name = "none value"
        writer.headers = ["none"]
        writer.value_matrix = [[None]]
        expected = """\
<style type="text/css">
    .none-value thead th:nth-child(1) {
        text-align: left;
    }
    .none-value tbody tr:nth-child(1) td:nth-child(1) {
        text-align: left;
    }
</style>
"""
        out = writer.dumps(write_style_tag=True)
        print_test_result(expected=expected, actual=out)
        assert out == expected

    @pytest.mark.parametrize(
        ["table", "indent", "header", "value", "expected"],
        [
            [data.table, data.indent, data.header, data.value, data.expected]
            for data in null_test_data_list
        ],
    )
    def test_normal_empty(self, table, indent, header, value, expected):
        writer = table_writer_class(
            table_name=table, indent_string=indent, headers=header, value_matrix=value
        )

        assert writer.dumps() == ""
        assert str(writer) == ""


class Test_CssTableWriter_write_table_iter:
    def test_exception(self):
        writer = table_writer_class()

        with pytest.raises(ptw.NotSupportedError):
            writer.write_table_iter()
