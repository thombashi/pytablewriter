# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import itertools

import pytest
import pytablewriter as ptw


class Test_WriterFactory_create_from_file_extension:

    @pytest.mark.parametrize(
        ["value", "expected"],
        list(itertools.product(
            ["valid_ext.csv", "valid_ext.CSV", ".csv", "CSV"],
            [ptw.CsvTableWriter])
        ) + list(itertools.product(
            ["valid_ext.html", "valid_ext.HTML", ".html", "HTML"],
            [ptw.HtmlTableWriter])
        ) + list(itertools.product(
            ["valid_ext.htm", "valid_ext.HTM", ".htm", "HTM"],
            [ptw.HtmlTableWriter])
        ) + list(itertools.product(
            ["valid_ext.js", "valid_ext.JS", ".js", "JS"],
            [ptw.JavaScriptTableWriter])
        ) + list(itertools.product(
            ["valid_ext.json", "valid_ext.JSON", ".json", "JSON"],
            [ptw.JsonTableWriter])
        ) + list(itertools.product(
            ["valid_ext.ltsv", "valid_ext.LTSV", ".ltsv", "LTSV"],
            [ptw.LtsvTableWriter])
        ) + list(itertools.product(
            ["valid_ext.md", "valid_ext.MD", ".md", "MD"],
            [ptw.MarkdownTableWriter])
        ) + list(itertools.product(
            ["valid_ext.py", "valid_ext.PY", ".py", "PY"],
            [ptw.PythonCodeTableWriter])
        ) + list(itertools.product(
            ["valid_ext.rst", "valid_ext.RST", ".rst", "RST"],
            [ptw.RstGridTableWriter])
        ) + list(itertools.product(
            ["valid_ext.tsv", "valid_ext.TSV", ".tsv", "TSV"],
            [ptw.TsvTableWriter])
        ) + list(itertools.product(
            ["valid_ext.toml", "valid_ext.TOML", ".toml", "TOML"],
            [ptw.TomlTableWriter])
        ) + list(itertools.product(
            ["valid_ext.xls", "valid_ext.XLS", ".xls", "XLS"],
            [ptw.ExcelXlsTableWriter])
        ) + list(itertools.product(
            ["valid_ext.xlsx", "valid_ext.XLSX", ".xlsx"],
            [ptw.ExcelXlsxTableWriter])
        )
    )
    def test_normal(self, value, expected):
        writer = ptw.TableWriterFactory.create_from_file_extension(value)

        assert isinstance(writer, expected)

    @pytest.mark.parametrize(["value", "expected"], [
        ["hoge", ptw.WriterNotFoundError],
        ["hoge.txt", ptw.WriterNotFoundError],
        [".txt", ptw.WriterNotFoundError],
    ])
    def test_exception(self, value, expected):
        with pytest.raises(expected):
            ptw.TableWriterFactory.create_from_file_extension(value)


class Test_FileLoaderFactory_create_from_format_name:

    @pytest.mark.parametrize(["format_name", "expected"], [
        ["csv", ptw.CsvTableWriter],
        ["CSV", ptw.CsvTableWriter],
        ["excel", ptw.ExcelXlsxTableWriter],
        ["Excel", ptw.ExcelXlsxTableWriter],
        ["html", ptw.HtmlTableWriter],
        ["HTML", ptw.HtmlTableWriter],
        ["javascript", ptw.JavaScriptTableWriter],
        ["JAVASCRIPT", ptw.JavaScriptTableWriter],
        ["js", ptw.JavaScriptTableWriter],
        ["JS", ptw.JavaScriptTableWriter],
        ["json", ptw.JsonTableWriter],
        ["JSON", ptw.JsonTableWriter],
        ["ltsv", ptw.LtsvTableWriter],
        ["LTSV", ptw.LtsvTableWriter],
        ["markdown", ptw.MarkdownTableWriter],
        ["Markdown", ptw.MarkdownTableWriter],
        ["mediawiki", ptw.MediaWikiTableWriter],
        ["MediaWiki", ptw.MediaWikiTableWriter],
        ["null", ptw.NullTableWriter],
        ["NULL", ptw.NullTableWriter],
        ["pandas", ptw.PandasDataFrameWriter],
        ["py", ptw.PythonCodeTableWriter],
        ["Python", ptw.PythonCodeTableWriter],
        ["rst", ptw.RstGridTableWriter],
        ["rst_grid_table", ptw.RstGridTableWriter],
        ["rst_simple_table", ptw.RstSimpleTableWriter],
        ["rst_csv_table", ptw.RstCsvTableWriter],
        ["tsv", ptw.TsvTableWriter],
        ["TSV", ptw.TsvTableWriter],
        ["toml", ptw.TomlTableWriter],
        ["TOML", ptw.TomlTableWriter],
    ])
    def test_normal(self, format_name, expected):
        writer = ptw.TableWriterFactory.create_from_format_name(format_name)

        assert isinstance(writer, expected)

    @pytest.mark.parametrize(["format_name", "expected"], [
        ["not_exist_format", ptw.WriterNotFoundError],
        ["", ptw.WriterNotFoundError],
        [None, AttributeError],
    ])
    def test_exception(self, format_name, expected):
        with pytest.raises(expected):
            ptw.TableWriterFactory.create_from_format_name(format_name)
