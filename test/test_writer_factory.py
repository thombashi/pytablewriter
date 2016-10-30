# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import pytest

import pytablewriter as ptw


class Test_WriterFactory_create_from_file_extension:

    @pytest.mark.parametrize(["value", "expected"], [
        ["valid_ext.csv", ptw.CsvTableWriter],
        ["valid_ext.CSV", ptw.CsvTableWriter],
        ["valid_ext.html", ptw.HtmlTableWriter],
        ["valid_ext.HTML", ptw.HtmlTableWriter],
        ["valid_ext.htm", ptw.HtmlTableWriter],
        ["valid_ext.HTM", ptw.HtmlTableWriter],
        ["valid_ext.json", ptw.JsonTableWriter],
        ["valid_ext.JSON", ptw.JsonTableWriter],
        ["valid_ext.md", ptw.MarkdownTableWriter],
        ["valid_ext.MD", ptw.MarkdownTableWriter],
        ["valid_ext.xls", ptw.ExcelXlsTableWriter],
        ["valid_ext.XLS", ptw.ExcelXlsTableWriter],
        ["valid_ext.xlsx", ptw.ExcelXlsxTableWriter],
        ["valid_ext.XLSX", ptw.ExcelXlsxTableWriter],
    ])
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
