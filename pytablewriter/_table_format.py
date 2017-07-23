# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import enum

from .writer import (
    CsvTableWriter,
    ElasticsearchWriter,
    ExcelXlsxTableWriter,
    ExcelXlsTableWriter,
    HtmlTableWriter,
    JavaScriptTableWriter,
    JsonTableWriter,
    LatexTableWriter,
    LatexMatrixWriter,
    LtsvTableWriter,
    MarkdownTableWriter,
    MediaWikiTableWriter,
    NullTableWriter,
    NumpyTableWriter,
    PandasDataFrameWriter,
    PythonCodeTableWriter,
    RstCsvTableWriter,
    RstGridTableWriter,
    RstSimpleTableWriter,
    SpaceAlignedTableWriter,
    SqliteTableWriter,
    TomlTableWriter,
    TsvTableWriter,
)


class FormatAttr(object):
    """
    Bitmaps to represent table attributes.
    """

    NONE = 1 << 1

    #: Can create a file with the format.
    FILE = 1 << 2

    #: Table format that can represent as a text.
    TEXT = 1 << 3

    #: Table format that can represent as a binary file.
    BIN = 1 << 4

    #: Can create a source code (variables definition)
    #: one of the programming language.
    SOURCECODE = 1 << 5

    #: Can call API for external service.
    API = 1 << 6

    SECONDARY_EXT = 1 << 10
    SECONDARY_NAME = 1 << 11


@enum.unique
class TableFormat(enum.Enum):
    """
    Enum to represent table format attributes.
    """

    CSV = (
        [CsvTableWriter().format_name], CsvTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT, ["csv"])
    ELASTICSEARCH = (
        [ElasticsearchWriter().format_name], ElasticsearchWriter,
        FormatAttr.API, [])
    EXCEL_XLS = (
        [ExcelXlsTableWriter().format_name], ExcelXlsTableWriter,
        FormatAttr.FILE | FormatAttr.BIN | FormatAttr.SECONDARY_NAME, ["xls"])
    EXCEL_XLSX = (
        [ExcelXlsxTableWriter().format_name], ExcelXlsxTableWriter,
        FormatAttr.FILE | FormatAttr.BIN, ["xlsx"])
    HTML = (
        [HtmlTableWriter().format_name, "htm"], HtmlTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT, ["html", "htm"])
    JAVASCRIPT = (
        [JavaScriptTableWriter().format_name, "js"], JavaScriptTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT | FormatAttr.SOURCECODE, ["js"])
    JSON = (
        [JsonTableWriter().format_name], JsonTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT, ["json"])
    LATEX_MATRIX = (
        [LatexMatrixWriter().format_name], LatexMatrixWriter,
        FormatAttr.FILE | FormatAttr.TEXT, ["tex"])
    LATEX_TABLE = (
        [LatexTableWriter().format_name], LatexTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT | FormatAttr.SECONDARY_EXT, ["tex"])
    LTSV = (
        [LtsvTableWriter().format_name], LtsvTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT, ["ltsv"])
    MARKDOWN = (
        [MarkdownTableWriter().format_name, "md"], MarkdownTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT, ["md"])
    MEDIAWIKI = (
        [MediaWikiTableWriter().format_name], MediaWikiTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT, [])
    NULL = (
        [NullTableWriter().format_name],
        NullTableWriter, FormatAttr.NONE, [])
    NUMPY = (
        [NumpyTableWriter().format_name], NumpyTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT | FormatAttr.SOURCECODE | FormatAttr.SECONDARY_EXT,
        ["py"])
    PANDAS = (
        [PandasDataFrameWriter().format_name], PandasDataFrameWriter,
        FormatAttr.FILE | FormatAttr.TEXT | FormatAttr.SOURCECODE | FormatAttr.SECONDARY_EXT,
        ["py"])
    PYTHON = (
        [PythonCodeTableWriter().format_name, "py"], PythonCodeTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT | FormatAttr.SOURCECODE, ["py"])
    RST_CSV_TABLE = (
        [RstCsvTableWriter().format_name], RstCsvTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT | FormatAttr.SECONDARY_EXT, ["rst"])
    RST_GRID_TABLE = (
        [RstGridTableWriter().format_name, "rst"], RstGridTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT, ["rst"])
    RST_SIMPLE_TABLE = (
        [RstSimpleTableWriter().format_name], RstSimpleTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT | FormatAttr.SECONDARY_EXT, ["rst"])
    SPACE_ALIGNED = (
        [SpaceAlignedTableWriter().format_name], SpaceAlignedTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT, [])
    SQLITE = (
        [SqliteTableWriter().format_name], SqliteTableWriter,
        FormatAttr.FILE | FormatAttr.BIN, ["sqlite", "sqlite3"])
    TOML = (
        [TomlTableWriter().format_name], TomlTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT, ["toml"])
    TSV = (
        [TsvTableWriter().format_name], TsvTableWriter,
        FormatAttr.FILE | FormatAttr.TEXT, ["tsv"])

    @property
    def name_list(self):
        """
        :return: Names associated with the table format.
        :rtype: list
        """

        return self.__name_list

    @property
    def writer_class(self):
        """
        :return: Table writer class associated with the table format.
        :rtype:
            :py:class:`~pytablewriter.writer._table_writer.TableWriterInterface`
        """

        return self.__writer_class

    @property
    def format_attribute(self):
        """
        :return: Table attributes bitmap.
        :rtype: :py:class:`pytablewriter.FormatAttr`
        """

        return self.__format_attribute

    @property
    def file_extension_list(self):
        """
        :return: File extensions associated with the table format.
        :rtype: list
        """

        return self.__file_extension_list

    def __init__(
            self, name_list, writer_class, format_attribute,
            file_extension_list):
        self.__name_list = name_list
        self.__writer_class = writer_class
        self.__format_attribute = format_attribute
        self.__file_extension_list = file_extension_list

    @classmethod
    def find_all_attr(cls, format_attribute):
        """
        Searching table formats which have specific attributes.

        :param FormatAttr format_attribute:
            Table format attributes to look for.
        :return: Table formats that matched the attribute.
        :rtype: list
        """

        return [
            table_format
            for table_format in TableFormat
            if table_format.format_attribute & format_attribute
        ]

    @classmethod
    def search_table_format(cls, format_attribute):
        import warnings

        warnings.warn(
            "search_table_format will be deleted in the future, "
            "use find_all_attr instead.",
            DeprecationWarning)

        return cls.find_all_attr(format_attribute)
