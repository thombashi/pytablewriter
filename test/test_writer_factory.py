"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import itertools
import sys

import pytest

import pytablewriter as ptw
from pytablewriter.typehint import Integer


class Test_WriterFactory_get_format_names:
    def test_normal(self):
        assert ptw.TableWriterFactory.get_format_names() == [
            "adoc",
            "asciidoc",
            "bold_unicode",
            "borderless",
            "css",
            "csv",
            "elasticsearch",
            "excel",
            "htm",
            "html",
            "javascript",
            "js",
            "json",
            "json_lines",
            "jsonl",
            "latex_matrix",
            "latex_table",
            "ldjson",
            "ltsv",
            "markdown",
            "md",
            "mediawiki",
            "ndjson",
            "null",
            "numpy",
            "pandas",
            "pandas_pickle",
            "py",
            "python",
            "rst",
            "rst_csv",
            "rst_csv_table",
            "rst_grid",
            "rst_grid_table",
            "rst_simple",
            "rst_simple_table",
            "space_aligned",
            "sqlite",
            "ssv",
            "toml",
            "tsv",
            "unicode",
            "yaml",
        ]


class Test_WriterFactory_get_extensions:
    def test_normal(self):
        assert ptw.TableWriterFactory.get_extensions() == [
            "adoc",
            "asc",
            "asciidoc",
            "css",
            "csv",
            "htm",
            "html",
            "js",
            "json",
            "jsonl",
            "ldjson",
            "ltsv",
            "md",
            "ndjson",
            "py",
            "rst",
            "sqlite",
            "sqlite3",
            "tex",
            "toml",
            "tsv",
            "xls",
            "xlsx",
            "yml",
        ]


class Test_WriterFactory_create_from_file_extension:
    @pytest.mark.parametrize(
        ["value", "expected"],
        list(
            itertools.product(
                ["valid_ext.adoc", "valid_ext.asciidoc", ".asc", "ADOC"], [ptw.AsciiDocTableWriter]
            )
        )
        + list(
            itertools.product(
                ["valid_ext.csv", "valid_ext.CSV", ".csv", "CSV"], [ptw.CsvTableWriter]
            )
        )
        + list(
            itertools.product(
                ["valid_ext.css", "valid_ext.CSS", ".css", "CSS"], [ptw.CssTableWriter]
            )
        )
        + list(
            itertools.product(
                ["valid_ext.html", "valid_ext.HTML", ".html", "HTML"], [ptw.HtmlTableWriter]
            )
        )
        + list(
            itertools.product(
                ["valid_ext.htm", "valid_ext.HTM", ".htm", "HTM"], [ptw.HtmlTableWriter]
            )
        )
        + list(
            itertools.product(
                ["valid_ext.js", "valid_ext.JS", ".js", "JS"], [ptw.JavaScriptTableWriter]
            )
        )
        + list(
            itertools.product(
                ["valid_ext.json", "valid_ext.JSON", ".json", "JSON"], [ptw.JsonTableWriter]
            )
        )
        + list(
            itertools.product(
                ["valid_ext.ltsv", "valid_ext.LTSV", ".ltsv", "LTSV"], [ptw.LtsvTableWriter]
            )
        )
        + list(
            itertools.product(
                ["valid_ext.md", "valid_ext.MD", ".md", "MD"], [ptw.MarkdownTableWriter]
            )
        )
        + list(
            itertools.product(
                ["valid_ext.py", "valid_ext.PY", ".py", "PY"], [ptw.PythonCodeTableWriter]
            )
        )
        + list(
            itertools.product(
                ["valid_ext.rst", "valid_ext.RST", ".rst", "RST"], [ptw.RstGridTableWriter]
            )
        )
        + list(
            itertools.product(
                ["valid_ext.sqlite", "valid_ext.sqlite3", ".sqlite", "SQLITE"],
                [ptw.SqliteTableWriter],
            )
        )
        + list(
            itertools.product(
                ["valid_ext.tex", "valid_ext.TEX", ".tex", "TEX"], [ptw.LatexMatrixWriter]
            )
        )
        + list(
            itertools.product(
                ["valid_ext.tsv", "valid_ext.TSV", ".tsv", "TSV"], [ptw.TsvTableWriter]
            )
        )
        + list(
            itertools.product(
                ["valid_ext.toml", "valid_ext.TOML", ".toml", "TOML"], [ptw.TomlTableWriter]
            )
        )
        + list(
            itertools.product(
                ["valid_ext.xls", "valid_ext.XLS", ".xls", "XLS"], [ptw.ExcelXlsTableWriter]
            )
        )
        + list(
            itertools.product(
                ["valid_ext.xlsx", "valid_ext.XLSX", ".xlsx"], [ptw.ExcelXlsxTableWriter]
            )
        )
        + list(
            itertools.product(["valid_ext.yml", "valid_ext.YML", ".yml"], [ptw.YamlTableWriter])
        ),
    )
    def test_normal(self, value, expected):
        table_name = "dummy"
        headers = ["a", "b"]
        value_matrix = [[1, 2]]
        type_hints = [Integer, Integer]
        is_formatting_float = False

        writer = ptw.TableWriterFactory.create_from_file_extension(
            value,
            table_name=table_name,
            headers=headers,
            value_matrix=value_matrix,
            type_hints=type_hints,
            is_formatting_float=is_formatting_float,
        )

        print(type(writer), file=sys.stderr)
        assert isinstance(writer, expected)
        assert writer.table_name == table_name
        assert writer.headers == headers
        assert writer.value_matrix == value_matrix
        assert writer.type_hints == type_hints
        assert writer.is_formatting_float == is_formatting_float

    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["hoge", ptw.WriterNotFoundError],
            ["hoge.txt", ptw.WriterNotFoundError],
            [".txt", ptw.WriterNotFoundError],
        ],
    )
    def test_exception(self, value, expected):
        with pytest.raises(expected):
            ptw.TableWriterFactory.create_from_file_extension(value)


class Test_FileLoaderFactory_create_from_format_name:
    @pytest.mark.parametrize(
        ["format_name", "expected"],
        [
            ["adoc", ptw.AsciiDocTableWriter],
            ["asciidoc", ptw.AsciiDocTableWriter],
            ["csv", ptw.CsvTableWriter],
            ["CSV", ptw.CsvTableWriter],
            ["excel", ptw.ExcelXlsxTableWriter],
            ["Excel", ptw.ExcelXlsxTableWriter],
            ["elasticsearch", ptw.ElasticsearchWriter],
            ["Elasticsearch", ptw.ElasticsearchWriter],
            ["html", ptw.HtmlTableWriter],
            ["HTML", ptw.HtmlTableWriter],
            ["htm", ptw.HtmlTableWriter],
            ["HTML", ptw.HtmlTableWriter],
            ["javascript", ptw.JavaScriptTableWriter],
            ["JAVASCRIPT", ptw.JavaScriptTableWriter],
            ["js", ptw.JavaScriptTableWriter],
            ["JS", ptw.JavaScriptTableWriter],
            ["json", ptw.JsonTableWriter],
            ["JSON", ptw.JsonTableWriter],
            ["latex_matrix", ptw.LatexMatrixWriter],
            ["latex_table", ptw.LatexTableWriter],
            ["ltsv", ptw.LtsvTableWriter],
            ["LTSV", ptw.LtsvTableWriter],
            ["markdown", ptw.MarkdownTableWriter],
            ["Markdown", ptw.MarkdownTableWriter],
            ["md", ptw.MarkdownTableWriter],
            ["MD", ptw.MarkdownTableWriter],
            ["mediawiki", ptw.MediaWikiTableWriter],
            ["MediaWiki", ptw.MediaWikiTableWriter],
            ["null", ptw.NullTableWriter],
            ["NULL", ptw.NullTableWriter],
            ["numpy", ptw.NumpyTableWriter],
            ["pandas", ptw.PandasDataFrameWriter],
            ["pandas_pickle", ptw.PandasDataFramePickleWriter],
            ["py", ptw.PythonCodeTableWriter],
            ["Python", ptw.PythonCodeTableWriter],
            ["rst", ptw.RstGridTableWriter],
            ["rst_grid_table", ptw.RstGridTableWriter],
            ["rst_simple_table", ptw.RstSimpleTableWriter],
            ["rst_csv_table", ptw.RstCsvTableWriter],
            ["space_aligned", ptw.SpaceAlignedTableWriter],
            ["SPACE_ALIGNED", ptw.SpaceAlignedTableWriter],
            ["ssv", ptw.SpaceAlignedTableWriter],
            ["sqlite", ptw.SqliteTableWriter],
            ["SQLite", ptw.SqliteTableWriter],
            ["tsv", ptw.TsvTableWriter],
            ["TSV", ptw.TsvTableWriter],
            ["toml", ptw.TomlTableWriter],
            ["TOML", ptw.TomlTableWriter],
            ["unicode", ptw.UnicodeTableWriter],
            ["Unicode", ptw.UnicodeTableWriter],
            ["yaml", ptw.YamlTableWriter],
            ["YAML", ptw.YamlTableWriter],
        ],
    )
    def test_normal(self, format_name, expected):
        table_name = "dummy"
        headers = ["a", "b"]
        value_matrix = [[1, 2]]
        type_hints = [Integer, Integer]
        is_formatting_float = False

        writer = ptw.TableWriterFactory.create_from_format_name(
            format_name,
            table_name=table_name,
            headers=headers,
            value_matrix=value_matrix,
            type_hints=type_hints,
            is_formatting_float=is_formatting_float,
        )

        print(format_name, type(writer), file=sys.stderr)
        assert isinstance(writer, expected)
        assert writer.table_name == table_name
        assert writer.headers == headers
        assert writer.value_matrix == value_matrix
        assert writer.type_hints == type_hints
        assert writer.is_formatting_float == is_formatting_float

    @pytest.mark.parametrize(
        ["format_name", "expected"],
        [
            ["not_exist_format", ptw.WriterNotFoundError],
            ["", ptw.WriterNotFoundError],
            [None, AttributeError],
        ],
    )
    def test_exception(self, format_name, expected):
        with pytest.raises(expected):
            ptw.TableWriterFactory.create_from_format_name(format_name)
