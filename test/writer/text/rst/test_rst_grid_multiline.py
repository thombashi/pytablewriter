import copy
import io
from textwrap import dedent

import pytest
from bs4 import BeautifulSoup
from dataproperty import calc_ascii_char_width
from docutils import nodes
from docutils.core import publish_doctree, publish_parts
from docutils.writers.html5_polyglot import Writer

from pytablewriter import (
    MarkdownTableWriter,
    RstCsvTableWriter,
    RstGridTableWriter,
    RstSimpleTableWriter,
    SpaceAlignedTableWriter,
    String,
)
from pytablewriter.style import Style


RAW_HTML = '.. raw:: html\n\n   <span title="Tooltip">Hello</span>'
BLOCKS = "* parent\n\n  * child\n\nExample::\n\n    first\n      nested\n\n    last"


class Wrapper:
    def __init__(self, child):
        self.child = child

    def __str__(self):
        return self.child


def parse_table(rst):
    warnings = io.StringIO()
    settings = {
        "raw_enabled": True,
        "file_insertion_enabled": False,
        "warning_stream": warnings,
        "halt_level": 2,
    }
    tree = publish_doctree(rst, settings_overrides=settings)
    html = publish_parts(rst, writer=Writer(), settings_overrides=settings)["fragment"]
    assert not warnings.getvalue()
    assert not list(tree.findall(nodes.system_message))
    tables = list(tree.findall(nodes.table))
    assert len(tables) == 1
    return tables[0], BeautifulSoup(html, "html.parser")


@pytest.mark.parametrize("wrap", [str, Wrapper])
@pytest.mark.parametrize("type_hints", [None, [String, String]])
@pytest.mark.parametrize("newline", ["\n", "\r\n", "\r"])
def test_issue_raw_html(wrap, type_hints, newline):
    writer = RstGridTableWriter(
        headers=["Header", "Header"],
        value_matrix=[[wrap(RAW_HTML.replace("\n", newline)), "N/A"]],
    )
    if type_hints is not None:
        writer.type_hints = type_hints
    rst = writer.dumps()
    table, html = parse_table(rst)
    rows = list(table.findall(nodes.row))
    assert len(rows) == 2
    assert len(rows[1].children) == 2
    assert list(rows[1][0].findall(nodes.raw))[0].astext() == '<span title="Tooltip">Hello</span>'
    assert rows[1][1].astext() == "N/A"
    cells = html.select("tbody tr td")
    assert cells[0].find("span", title="Tooltip").text == "Hello"
    assert cells[1].get_text(strip=True) == "N/A"
    assert "\r" not in rst
    assert (
        rst
        == RstGridTableWriter(
            headers=["Header", "Header"], value_matrix=[[RAW_HTML, "N/A"]]
        ).dumps()
    )


@pytest.mark.parametrize("align", ["left", "center", "right"])
@pytest.mark.parametrize("margin", [0, 1, 2])
@pytest.mark.parametrize("with_headers", [False, True])
def test_block_alignment_preserves_nested_structure(align, margin, with_headers):
    writer = RstGridTableWriter(
        table_name="Nested blocks",
        headers=["A much wider column heading", "Other"] if with_headers else [],
        value_matrix=[[BLOCKS, RAW_HTML], ["a much wider body value", "second row"]],
        margin=margin,
        indent_level=1,
        column_styles=[Style(align=align), Style(align=align)],
    )
    table, html = parse_table(writer.dumps())
    assert table[0].astext() == "Nested blocks"
    rows = list(table.findall(nodes.row))
    assert len(rows) == 2 + int(with_headers)
    first = rows[int(with_headers)]
    assert len(first.children) == 2
    lists = list(first[0].findall(nodes.bullet_list))
    assert len(lists) == 2
    assert list(lists[0].findall(nodes.bullet_list))[-1] is lists[1]
    literal = list(first[0].findall(nodes.literal_block))
    assert len(literal) == 1
    assert literal[0].astext() == "first\n  nested\n\nlast"
    assert not list(first[0].findall(nodes.block_quote))
    assert len(list(first[1].findall(nodes.raw))) == 1
    assert html.select("tbody tr td")[1].span["title"] == "Tooltip"
    assert writer._indent_level == 1


@pytest.mark.parametrize("with_headers", [False, True])
@pytest.mark.parametrize("is_write_header", [False, True])
def test_different_cell_heights_and_empty_values(with_headers, is_write_header):
    values = [["first\n\nlast\n", "", "end\ntwo"], [None, "middle", "tail\nline\nthree"]]
    original = copy.deepcopy(values)
    writer = RstGridTableWriter(
        headers=["left\nheading", "middle", "right\n\nheading"] if with_headers else [],
        value_matrix=values,
        is_write_header=is_write_header,
    )
    rst = writer.dumps()
    assert writer.value_matrix == original
    assert values == original
    table, _ = parse_table(rst)
    rows = list(table.findall(nodes.row))
    assert len(rows) == 2 + int(with_headers and is_write_header)
    assert all(len(row.children) == 3 for row in rows)
    first, second = rows[-2:]
    assert first[0].astext() == "first\n\nlast"
    assert first[1].astext() == ""
    assert first[2].astext() == "end\ntwo"
    assert second[0].astext() == ""
    assert second[1].astext() == "middle"
    assert second[2].astext() == "tail\nline\nthree"
    # A fourth, empty physical line belongs to the first logical body row.
    body_lines = rst.splitlines()[3 + (4 if with_headers and is_write_header else 0) :]
    assert body_lines[3].strip().replace("|", "").strip() == ""
    assert body_lines[4].strip().startswith("+")


def test_multiline_header_raw_and_literal_content():
    writer = RstGridTableWriter(headers=[RAW_HTML, "Example::\n\n    code"], value_matrix=[[1, 2]])
    table, html = parse_table(writer.dumps())
    headers = list(table.findall(nodes.thead))[0][0]
    assert len(list(headers[0].findall(nodes.raw))) == 1
    assert list(headers[1].findall(nodes.literal_block))[0].astext() == "code"
    assert html.select("thead tr th")[0].span.text == "Hello"


def test_logical_types_and_filter_indices():
    seen = []
    values = [["text\nlines", 1234, 1.2], ["tail", 20, 10.25]]
    writer = RstGridTableWriter(headers=["label", "integer", "real"], value_matrix=values)

    def style_filter(cell, **kwargs):
        seen.append((cell.row, cell.col, cell.value))
        return Style(align="right")

    writer.add_style_filter(style_filter)
    table, _ = parse_table(writer.dumps())
    body = list(table.findall(nodes.tbody))[0]
    assert [[entry.astext() for entry in row] for row in body] == [
        ["text\nlines", "1234", "1.20"],
        ["tail", "20", "10.25"],
    ]
    data_calls = [call for call in seen if call[0] >= 0]
    assert len(data_calls) == 6
    assert [call[:2] for call in data_calls] == [(r, c) for r in range(2) for c in range(3)]
    assert data_calls[0][2] == "text\nlines"
    assert writer.value_matrix == values
    # Cached rendering must not invoke cell filters or accumulate widths again.
    before = list(seen)
    writer.dumps()
    assert seen == before


@pytest.mark.parametrize("with_headers", [False, True])
def test_explicit_string_and_inline_styles(with_headers):
    writer = RstGridTableWriter(
        headers=["label", "number"] if with_headers else [],
        value_matrix=[["first\n\nlast", "0012"], ["other", "1.20"]],
        type_hints=[String, String],
        column_styles=[Style(font_weight="bold", align="center"), Style(font_style="italic")],
        enable_ansi_escape=False,
    )
    table, _ = parse_table(writer.dumps())
    body = list(table.findall(nodes.tbody))[0]
    assert [n.astext() for n in body[0][0].findall(nodes.strong)] == ["first", "last"]
    assert list(body[0][1].findall(nodes.emphasis))[0].astext() == "0012"
    assert list(body[1][1].findall(nodes.emphasis))[0].astext() == "1.20"


@pytest.mark.parametrize("with_headers", [False, True])
def test_font_filter_sizes_each_logical_cell(with_headers):
    writer = RstGridTableWriter(
        headers=["a", "b"] if with_headers else [],
        value_matrix=[["first\nlast", "x"], ["tail", "end"]],
        enable_ansi_escape=False,
    )
    calls = []

    def font_filter(cell, **kwargs):
        calls.append((cell.row, cell.col))
        return Style(font_weight="bold" if cell.row == 0 else "normal", align="center")

    writer.add_style_filter(font_filter)
    table, _ = parse_table(writer.dumps())
    body = list(table.findall(nodes.tbody))[0]
    assert [n.astext() for n in body[0][0].findall(nodes.strong)] == ["first", "last"]
    assert list(body[0][1].findall(nodes.strong))[0].astext() == "x"
    assert body[1][1].astext() == "end"
    assert [call for call in calls if call[0] >= 0] == [(0, 0), (0, 1), (1, 0), (1, 1)]
    assert writer.dumps() == writer.dumps()


def test_blank_lines_and_relative_indentation_are_not_stripped():
    writer = RstGridTableWriter(value_matrix=[["\n::\n\n    first\n    \n      nested\n\n", "x"]])
    rst = writer.dumps()
    table, _ = parse_table(rst)
    assert list(table.findall(nodes.literal_block))[0].astext() == "first\n\n  nested"
    lines = rst.splitlines()
    assert lines[3] == "    |            |x|"
    assert lines[7] == "    |            | |"
    assert lines[-2] == "    |            | |"


def test_multibyte_widths():
    writer = RstGridTableWriter(headers=["見出し\n一", "value"], value_matrix=[["日本\n語", "α"]])
    rst = writer.dumps()
    physical = [line.strip() for line in rst.splitlines() if line.strip().startswith(("+", "|"))]
    assert len({calc_ascii_char_width(line) for line in physical}) == 1
    table, _ = parse_table(rst)
    rows = list(table.findall(nodes.row))
    assert rows[0][0].astext() == "見出し\n一"
    assert rows[1][0].astext() == "日本\n語"
    assert rows[1][1].astext() == "α"


def test_cache_invalidation_and_repeated_writes():
    writer = RstGridTableWriter(headers=["a", "b"], value_matrix=[["one\ntwo", "x"]])
    first = writer.dumps()
    assert writer.dumps() == first
    stream = io.StringIO()
    writer.stream = stream
    writer.write_table()
    writer.write_table()
    assert stream.getvalue() == first * 2
    writer.margin = 2
    wider = writer.dumps()
    assert wider != first
    parse_table(wider)
    writer.headers = ["new\nheader", "b"]
    writer.value_matrix = [["new\nvalue\nmore", None]]
    changed = writer.dumps()
    assert "one" not in changed
    assert writer.dumps() == changed
    table, _ = parse_table(changed)
    assert list(table.findall(nodes.row))[-1][0].astext() == "new\nvalue\nmore"
    writer.value_matrix = [["z", 2]]
    writer.headers = ["a", "b"]
    assert (
        writer.dumps()
        == RstGridTableWriter(headers=["a", "b"], value_matrix=[["z", 2]], margin=2).dumps()
    )


def test_indent_restored_after_stream_failure():
    class BrokenStream(io.StringIO):
        def write(self, text):
            if "|" in text:
                raise OSError("stream failed")
            return super().write(text)

    writer = RstGridTableWriter(value_matrix=[[RAW_HTML]], indent_level=2)
    writer.stream = BrokenStream()
    with pytest.raises(OSError, match="stream failed"):
        writer.write_table()
    assert writer._indent_level == 2
    table, _ = parse_table(writer.dumps())
    assert len(list(table.findall(nodes.raw))) == 1


def test_indent_restored_after_filter_failure():
    writer = RstGridTableWriter(value_matrix=[[RAW_HTML]], indent_level=1)

    def broken_filter(cell, **kwargs):
        raise RuntimeError("filter failed")

    writer.add_style_filter(broken_filter)
    with pytest.raises(RuntimeError, match="filter failed"):
        writer.dumps()
    assert writer._indent_level == 1
    writer.clear_theme()
    table, _ = parse_table(writer.dumps())
    assert len(list(table.findall(nodes.raw))) == 1


@pytest.mark.parametrize(
    "writer_class",
    [RstSimpleTableWriter, RstCsvTableWriter, MarkdownTableWriter, SpaceAlignedTableWriter],
)
def test_other_text_writers_keep_existing_newline_policy(writer_class):
    writer = writer_class(headers=["a", "b"], value_matrix=[["first\nsecond", 1]])
    assert "first second" in writer.dumps()


def test_preprocessor_invalidation_and_empty_row():
    writer = RstGridTableWriter(
        headers=["a", "b"], value_matrix=[["first\nsecond", "x"], [None, ""]]
    )
    table, _ = parse_table(writer.dumps())
    assert len(list(table.findall(nodes.tbody))[0].children) == 2
    writer.update_preprocessor(line_break_handling="replace")
    assert "first second" in writer.dumps()
    writer.update_preprocessor(line_break_handling="nop")
    table, _ = parse_table(writer.dumps())
    assert list(table.findall(nodes.tbody))[0][0][0].astext() == "first\nsecond"


def test_single_line_output_is_unchanged():
    assert RstGridTableWriter(headers=["a", "b"], value_matrix=[[1, "x"]]).dumps() == dedent(
        """\
        .. table::

            +-+-+
            |a|b|
            +=+=+
            |1|x|
            +-+-+
        """
    )
