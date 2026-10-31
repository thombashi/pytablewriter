import io
import itertools
import re

import pytest

import pytablewriter as ptw
from pytablewriter.style import Align, Style


def parse_table_boundaries(text):
    """Scan physical rows and unescaped delimiters, independently of the writer.

    This checks table structure, not Confluence's inline markup renderer.
    Double backslashes are line-break tokens; a single backslash escapes a character.
    """
    rows = []
    for line in text.splitlines():
        tokens = re.findall(r"\\\\|\\.|\|\||\||[^\\|]+", line)
        assert "".join(tokens) == line
        delimiter = tokens[0]
        assert delimiter in ("|", "||")
        assert tokens[-1] == delimiter
        cells = []
        cell = ""
        for token in tokens[1:]:
            if token in ("|", "||"):
                assert token == delimiter
                assert cell  # Empty cells must not become double-pipe header boundaries.
                cells.append(cell)
                cell = ""
            else:
                cell += token
        assert not cell
        rows.append((delimiter, cells))
    return rows


def test_official_table_example(capsys):
    writer = ptw.ConfluenceWikiTableWriter(
        headers=["heading 1", "heading 2", "heading 3"],
        value_matrix=[["cell A1", "cell A2", "cell A3"], ["cell B1", "cell B2", "cell B3"]],
    )
    expected = (
        "||heading 1||heading 2||heading 3||\n"
        "|cell A1|cell A2|cell A3|\n"
        "|cell B1|cell B2|cell B3|\n"
    )
    assert writer.dumps() == expected
    writer.write_table()
    assert capsys.readouterr().out == expected
    assert writer.format_name == "confluence"


@pytest.mark.parametrize(
    "headers, values, expected",
    [
        ([], [], ""),
        (["a", "b"], [], "||a||b||\n"),
        ([], [[1, 2]], "|1|2|\n"),
        (["", None], [["", None]], "|| ||None||\n| | |\n"),
        (
            ["文字", "bool", "number"],
            [["日本語", True, 12.5]],
            "||文字||bool||number||\n|日本語|True|12.5|\n",
        ),
    ],
)
def test_empty_and_typed_cells(headers, values, expected):
    output = ptw.ConfluenceWikiTableWriter(headers=headers, value_matrix=values).dumps()
    assert output == expected
    for _, cells in parse_table_boundaries(output):
        assert len(cells) == (len(headers) if headers else len(values[0]))


@pytest.mark.parametrize(
    "cell",
    [
        "|",
        "||",
        "\\",
        "\\\\",
        "\\|",
        "\n",
        "\r\n",
        "\r",
        "a\n\nb",
        "a\r\nb",
        "|\n||",
        "x\\",
        "\\\n|",
        "雪|\\\r\n",
    ],
)
def test_structural_escaping(cell):
    output = ptw.ConfluenceWikiTableWriter(
        headers=[cell, "", cell],
        value_matrix=[[cell, None, cell], ["", cell, ""]],
    ).dumps()
    rows = parse_table_boundaries(output)
    assert [kind for kind, _ in rows] == ["||", "|", "|"]
    assert [len(cells) for _, cells in rows] == [3, 3, 3]
    assert rows[0][1][0] == rows[1][1][0] == rows[2][1][1]
    assert "\r" not in output


def test_escape_contract():
    writer = ptw.ConfluenceWikiTableWriter(
        headers=["a|b", "a\\b", "a\r\nb"],
        value_matrix=[["a|b", "a\\b", "a\nb"]],
    )
    assert writer.dumps() == ("||a\\|b||a&#92;b||a\\\\ b||\n|a\\|b|a&#92;b|a\\\\ b|\n")


def test_exhaustive_short_structural_cells():
    # A grammar-based check over all short combinations catches adjacency failures.
    alphabet = ["|", "\\", "\n", "\r", "x", ""]
    values = [["".join(parts), "", "end"] for parts in itertools.product(alphabet, repeat=3)]
    output = ptw.ConfluenceWikiTableWriter(headers=["a", "b", "c"], value_matrix=values).dumps()
    rows = parse_table_boundaries(output)
    assert len(rows) == len(values) + 1
    assert all(len(cells) == 3 for _, cells in rows)
    assert all(kind == "|" for kind, _ in rows[1:])


def test_formatting_options():
    writer = ptw.ConfluenceWikiTableWriter(
        headers=["name", "value"],
        value_matrix=[["a|b", 1.2345]],
        margin=1,
        max_precision=2,
        column_styles=[Style(align=Align.LEFT), Style(align=Align.RIGHT)],
    )
    assert writer.dumps() == "|| name || value ||\n| a\\|b | 1.23 |\n"
    writer.is_write_header = False
    assert writer.dumps() == "| a\\|b | 1.23 |\n"


@pytest.mark.parametrize(
    "options, expected",
    [
        ({"is_padding": True}, "|| a  ||  b  ||\n|   1| 1.23|\n|long|20.00|\n"),
        ({"is_formatting_float": False}, "||a||b||\n|1|1.23|\n|long|20|\n"),
        ({"type_hints": [ptw.String, ptw.String]}, "||a||b||\n|001|1.23|\n|long|20.0|\n"),
    ],
)
def test_text_formatting_options(options, expected):
    writer = ptw.ConfluenceWikiTableWriter(
        headers=["a", "b"],
        value_matrix=[["001", 1.23], ["long", 20.0]],
        **options,
    )
    assert writer.dumps() == expected


def test_structure_checker_rejects_broken_tables():
    for text in ["|a||b|\n", "|a|b\n", "|a||\n", "|a\nb|\n"]:
        with pytest.raises(AssertionError):
            parse_table_boundaries(text)


@pytest.mark.parametrize("headers", [[], ["a", "b"]])
@pytest.mark.parametrize("iteration_length", [-1, 3])
@pytest.mark.parametrize("trailing_blank", [False, True])
def test_split_write(headers, iteration_length, trailing_blank):
    chunks = [[["a|b", 1]], [["雪", 2]], [["x\ny", 3]]]
    expected = ptw.ConfluenceWikiTableWriter(
        headers=headers,
        value_matrix=list(itertools.chain.from_iterable(chunks)),
        is_write_null_line_after_table=trailing_blank,
    ).dumps()
    calls = []
    writer = ptw.ConfluenceWikiTableWriter(
        headers=headers,
        value_matrix=iter(chunks),
        iteration_length=iteration_length,
        is_write_null_line_after_table=trailing_blank,
        write_callback=lambda count, length: calls.append((count, length)),
    )
    assert writer.support_split_write
    writer.stream = io.StringIO()
    writer.write_table_iter()
    assert writer.stream.getvalue() == expected
    assert calls == [(i, iteration_length) for i in range(1, 4)]
    assert writer.is_write_header
    assert sum(kind == "||" for kind, _ in parse_table_boundaries(expected.rstrip("\n"))) == bool(
        headers
    )


@pytest.mark.parametrize("name", ["confluence", "confluence_wiki", "CONFLUENCE", "Confluence_Wiki"])
def test_public_factory(name):
    from pytablewriter.writer import ConfluenceWikiTableWriter
    from pytablewriter.writer.text import ConfluenceWikiTableWriter as TextWriter

    writer = ptw.TableWriterFactory.create_from_format_name(name, headers=["a"], value_matrix=[[1]])
    assert type(writer) is ptw.ConfluenceWikiTableWriter is ConfluenceWikiTableWriter is TextWriter
    assert writer.dumps() == "||a||\n|1|\n"
    assert ptw.TableFormat.from_name(name) is ptw.TableFormat.CONFLUENCE
    assert "wiki" not in ptw.TableWriterFactory.get_extensions()


def test_dump_stream_and_file(tmp_path):
    writer = ptw.ConfluenceWikiTableWriter(headers=["a"], value_matrix=[["雪|x"]])
    stream = io.StringIO()
    writer.dump(stream, close_after_write=False)
    assert stream.getvalue() == writer.dumps()
    path = tmp_path / "table.txt"
    writer.dump(str(path))
    assert path.read_text(encoding="utf-8") == writer.dumps()
