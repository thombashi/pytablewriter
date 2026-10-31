import io

import pytest

from pytablewriter import LatexTableWriter, TableWriterFactory
from pytablewriter.style import Align, Style

from .test_latex_table_writer import normal_test_data_list


@pytest.mark.parametrize("data", normal_test_data_list)
def test_explicit_array_compatibility(data):
    kwargs = {"headers": data.header, "value_matrix": data.value}
    assert LatexTableWriter(**kwargs).dumps() == data.expected
    assert LatexTableWriter(table_environment="array", **kwargs).dumps() == data.expected


@pytest.mark.parametrize("value", ["", "TABULAR", "table", None, 1, [], {}])
def test_invalid_environment(value):
    with pytest.raises(ValueError, match="table_environment"):
        LatexTableWriter(table_environment=value)
    writer = LatexTableWriter()
    with pytest.raises(ValueError, match="table_environment"):
        writer.table_environment = value
    assert writer.table_environment == "array"


def test_text_math_and_structure(capsys):
    writer = LatexTableWriter(
        table_environment="tabular",
        table_name="ignored table name",
        headers=["multi word", "value"],
        value_matrix=[
            ["a & b%$#_{}~^|\\path\nnext", float("inf")],
            ["ordinary text", r"\alpha"],
            [None, 12.5],
        ],
        column_styles=[Style(align=Align.LEFT), Style(align=Align.RIGHT)],
    )
    out = writer.dumps()
    assert out.startswith(r"\begin{tabular}{l | r} \hline")
    assert out.endswith("\\end{tabular}\n")
    assert (
        r"a \& b\%\$\#\_\{\}\textasciitilde{}\textasciicircum{}\textbar{}\textbackslash{}path next"
        in out
    )
    assert r"\ensuremath{\infty}" in out
    assert r"\ensuremath{\alpha}" in out
    assert "ordinary text" in out
    assert out.count(" & ") == 4
    assert out.count(r"\\ \hline") == 4
    assert "ignored table name" not in out
    writer.write_table()
    assert capsys.readouterr().out == out
    writer.table_environment = "array"
    assert writer.dumps().startswith(r"\begin{array}")
    writer.table_environment = "tabular"
    assert writer.dumps() == out


@pytest.mark.parametrize("headers,values", [(None, [[1, None]]), (["only header"], []), ([], [])])
def test_optional_headers_and_empty(headers, values):
    writer = LatexTableWriter(table_environment="tabular", headers=headers, value_matrix=values)
    out = writer.dumps()
    if not headers and not values:
        assert out == ""
    else:
        assert out.count(r"\begin{tabular}") == out.count(r"\end{tabular}") == 1
        assert out.count("only header") == bool(headers)


def test_styles_and_literal_math():
    writer = LatexTableWriter(
        table_environment="tabular",
        enable_ansi_escape=False,
        headers=["bold & header"],
        value_matrix=[["a_b"], ["$x^2$"], [r"x_{1}"]],
        column_styles=[Style(font_weight="bold", font_style="italic", decoration_line="underline")],
    )
    out = writer.dumps()
    assert r"\it{\bf{a\_b}}" in out
    assert r"\underline{" in out
    assert r"\$x\textasciicircum{}2\$" in out
    assert r"x\_\{1\}" in out
    assert r"bold \& header" in out


def test_factory_and_split_write():
    stream = io.StringIO()
    writer = TableWriterFactory.create_from_format_name(
        "latex_table",
        table_environment="tabular",
        headers=["word header", "number"],
        value_matrix=iter([[["first row", 1]], [["second row", 2]]]),
        iteration_length=2,
    )
    writer.stream = stream
    writer.write_table_iter()
    out = stream.getvalue()
    assert out.count(r"\begin{tabular}") == out.count(r"\end{tabular}") == 1
    assert out.count("word header") == 1
    assert out.count("first row") == out.count("second row") == 1
    assert out.count(r"\\ \hline") == 3


def test_formatted_numbers_and_literal_header():
    writer = LatexTableWriter(
        table_environment="tabular",
        headers=[r"\alpha"],
        value_matrix=[[12345]],
        column_styles=[Style(thousand_separator="underscore")],
    )
    out = writer.dumps()
    assert r"\textbackslash{}alpha" in out
    assert r"12\_345" in out
    assert r"\ensuremath" not in out
