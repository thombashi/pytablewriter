# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
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
            ["valid_ext.md", "valid_ext.MD", ".md", "MD"],
            [ptw.MarkdownTableWriter])
        ) + list(itertools.product(
            ["valid_ext.py", "valid_ext.PY", ".py", "PY"],
            [ptw.PythonCodeTableWriter])
        ) + list(itertools.product(
            ["valid_ext.rst", "valid_ext.RST", ".rst", "RST"],
            [ptw.RstGridTableWriter])
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

    @pytest.mark.parametrize(["file_path", "format_name", "expected"], [
        ["valid_ext.html", "csv", ptw.CsvTableWriter],
        ["invalid_ext.txt", "CSV", ptw.CsvTableWriter],
        ["valid_ext.html", "excel", ptw.ExcelXlsxTableWriter],
        ["invalid_ext.txt", "Excel", ptw.ExcelXlsxTableWriter],
        ["valid_ext.json", "html", ptw.HtmlTableWriter],
        ["invalid_ext.txt", "HTML", ptw.HtmlTableWriter],
        ["valid_ext.html", "json", ptw.JsonTableWriter],
        ["invalid_ext.txt", "JSON", ptw.JsonTableWriter],
        ["valid_ext.html", "markdown", ptw.MarkdownTableWriter],
        ["invalid_ext.txt", "Markdown", ptw.MarkdownTableWriter],
        ["valid_ext.html", "mediawiki", ptw.MediaWikiTableWriter],
        ["invalid_ext.txt", "MediaWiki", ptw.MediaWikiTableWriter],
    ])
    def test_normal(self, file_path, format_name, expected):
        writer = ptw.TableWriterFactory.create_from_format_name(format_name)

        assert isinstance(writer, expected)

    @pytest.mark.parametrize(["file_path", "format_name", "expected"], [
        ["valid_ext.csv", "not_exist_format", ptw.WriterNotFoundError],
        ["valid_ext.csv", "", ptw.WriterNotFoundError],
        ["valid_ext.csv", None, AttributeError],
    ])
    def test_exception(self, file_path, format_name, expected):
        with pytest.raises(expected):
            ptw.TableWriterFactory.create_from_format_name(format_name)
