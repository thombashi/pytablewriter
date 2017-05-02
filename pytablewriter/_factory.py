# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import copy
import os

import typepy

from ._const import FormatName
from ._error import WriterNotFoundError
from .writer._csv_writer import CsvTableWriter
from .writer._excel_writer import (
    ExcelXlsxTableWriter,
    ExcelXlsTableWriter
)
from .writer._html_writer import HtmlTableWriter
from .writer._javascript_writer import JavaScriptTableWriter
from .writer._json_writer import JsonTableWriter
from .writer._ltsv_writer import LtsvTableWriter
from .writer._md_writer import MarkdownTableWriter
from .writer._mediawiki_writer import MediaWikiTableWriter
from .writer._null_writer import NullTableWriter
from .writer._pandas_writer import PandasDataFrameWriter
from .writer._python_code_writer import PythonCodeTableWriter
from .writer._rst_writer import (
    RstCsvTableWriter,
    RstGridTableWriter,
    RstSimpleTableWriter
)
from .writer._sqlite_writer import SqliteTableWriter
from .writer._toml_writer import TomlTableWriter
from .writer._tsv_writer import TsvTableWriter


class TableWriterFactory(object):
    """
    A factor class of table writer classes.
    """

    __COMMON_WRITER_TABLE = {
        FormatName.CSV: CsvTableWriter,
        FormatName.HTML: HtmlTableWriter,
        FormatName.JSON: JsonTableWriter,
        FormatName.JAVASCRIPT_ABBR: JavaScriptTableWriter,
        FormatName.LTSV: LtsvTableWriter,
        FormatName.PYTHON_ABBR: PythonCodeTableWriter,
        FormatName.RST: RstGridTableWriter,
        FormatName.SQLITE: SqliteTableWriter,
        FormatName.TSV: TsvTableWriter,
        FormatName.TOML: TomlTableWriter,
    }

    @classmethod
    def create_from_file_extension(cls, file_extension):
        """
        Create a writer class instance from a file extension.
        Supported file extensions are as follows:

            ==================  ===================================
            Format name         Writer                             
            ==================  ===================================
            ``".csv"``          :py:class:`~.CsvTableWriter`       
            ``".html"``         :py:class:`~.HtmlTableWriter`      
            ``".js"``           :py:class:`~.JavaScriptTableWriter`
            ``".json"``         :py:class:`~.JsonTableWriter`      
            ``".ltsv"``         :py:class:`~.LtsvTableWriter`       
            ``".md"``           :py:class:`~.MarkdownTableWriter`  
            ``".py"``           :py:class:`~.PythonCodeTableWriter`
            ``".rst"``          :py:class:`~.RstGridTableWriter`   
            ``".tsv"``          :py:class:`~.TsvTableWriter`       
            ``".xls"``          :py:class:`~.ExcelXlsTableWriter`  
            ``".xlsx"``         :py:class:`~.ExcelXlsxTableWriter` 
            ``".sqlite"``       :py:class:`~.SqliteTableWriter`    
            ``".sqlite3"``      :py:class:`~.SqliteTableWriter`    
            ``".tsv"``          :py:class:`~.TsvTableWriter`       
            ``".toml"``         :py:class:`~.TomlTableWriter`      
            ==================  ===================================

        :param str file_extension:
            File extension string (case insensitive).
        :return:
            Writer that coincide with the ``file_extension``.
        :raises pytablewriter.WriterNotFoundError:
            If appropriate writer not found.
        """

        ext = os.path.splitext(file_extension)[1]
        if typepy.is_null_string(ext):
            file_extension = file_extension
        else:
            file_extension = ext

        file_extension = file_extension.lstrip(".").lower()

        try:
            return cls.__create_writer(
                cls.__get_extension_writer_mapping(), file_extension)
        except WriterNotFoundError as e:
            raise WriterNotFoundError("\n".join([
                "{:s} (unknown file extension).".format(e.args[0]),
                "",
                "acceptable file extensions are: {}.".format(
                    ", ".join(cls.get_extension_list())),
            ]))

    @classmethod
    def create_from_format_name(cls, format_name):
        """
        Create a writer class instance from a format name.
        Supported file format names are as follows:

            ==============================  ===================================
            Format name                     Loader                             
            ==============================  ===================================
            ``"csv"``                       :py:class:`~.CsvTableWriter`       
            ``"excel"``                     :py:class:`~.ExcelXlsxTableWriter` 
            ``"html"``                      :py:class:`~.HtmlTableWriter`      
            ``"javascript"``/``"js"``       :py:class:`~.JavaScriptTableWriter`
            ``"json"``                      :py:class:`~.JsonTableWriter`      
            ``"ltsv"``                      :py:class:`~.LtsvTableWriter`       
            ``"markdown"``                  :py:class:`~.MarkdownTableWriter`  
            ``"mediawiki"``                 :py:class:`~.MediaWikiTableWriter` 
            ``"null"``                      :py:class:`~.NullTableWriter`      
            ``"pandas"``                    :py:class:`~.PandasDataFrameWriter`
            ``"py"``/``"python"``           :py:class:`~.PythonCodeTableWriter`
            ``"rst"``/``"rst_grid_table"``  :py:class:`~.RstGridTableWriter`   
            ``"rst_simple_table"``          :py:class:`~.RstSimpleTableWriter` 
            ``"rst_csv_table"``             :py:class:`~.RstCsvTableWriter`    
            ``"sqlite"``                    :py:class:`~.SqliteTableWriter`    
            ``"tsv"``                       :py:class:`~.TsvTableWriter`       
            ``"toml"``                      :py:class:`~.TomlTableWriter`      
            ==============================  ===================================

        :param str format_name: Format name string (case insensitive).
        :return: Writer that coincide with the ``format_name``:
        :raises pytablewriter.WriterNotFoundError:
            If appropriate writer not found.
        """

        format_name = format_name.lower()

        try:
            return cls.__create_writer(
                cls.__get_format_name_writer_mapping(), format_name)
        except WriterNotFoundError as e:
            raise WriterNotFoundError("\n".join([
                "{} (unknown format name).".format(e.args[0]),
                "acceptable format names are: {}.".format(
                    ", ".join(cls.get_format_name_list())),
            ]))

    @staticmethod
    def __create_writer(writer_mapping, format_name):
        try:
            return writer_mapping[format_name]()
        except KeyError:
            raise WriterNotFoundError(", ".join([
                "writer not found: format='{}'".format(format_name),
            ]))

    @classmethod
    def get_format_name_list(cls):
        """
        :return: Available format name List.
        :rtype: list

        :Examples:
            .. code:: python

                >>> import pytablewriter as ptw
                >>> for name in ptw.TableWriterFactory.get_format_name_list():
                ...     print(name)
                ...
                csv
                excel
                html
                javascript
                js
                json
                ltsv
                markdown
                mediawiki
                null
                pandas
                py
                python
                rst
                rst_csv_table
                rst_grid_table
                rst_simple_table
                sqlite
                toml
                tsv
        """

        return sorted(cls.__get_format_name_writer_mapping())

    @classmethod
    def get_extension_list(cls):
        """
        :return: Available file format extension list.
        :rtype: list

        :Examples:
            .. code:: python

                >>> import pytablewriter as ptw
                >>> for name in ptw.TableWriterFactory.get_extension_list():
                ...     print(name)
                ...
                csv
                htm
                html
                js
                json
                ltsv
                md
                py
                rst
                sqlite
                sqlite3
                toml
                tsv
                xls
                xlsx
        """

        return sorted(cls.__get_extension_writer_mapping())

    @classmethod
    def __get_format_name_writer_mapping(cls):
        """
        :return: Mappings of format-name and writer class.
        :rtype: dict
        """

        writer_mapping = copy.deepcopy(cls.__COMMON_WRITER_TABLE)
        writer_mapping.update({
            FormatName.EXCEL: ExcelXlsxTableWriter,
            FormatName.JAVASCRIPT: JavaScriptTableWriter,
            FormatName.MARKDOWN: MarkdownTableWriter,
            FormatName.MEDIAWIKI: MediaWikiTableWriter,
            FormatName.NULL: NullTableWriter,
            FormatName.PANDAS: PandasDataFrameWriter,
            FormatName.PYTHON: PythonCodeTableWriter,
            FormatName.RST_GRID_TABBLE: RstGridTableWriter,
            FormatName.RST_SIMPLE_TABBLE: RstSimpleTableWriter,
            FormatName.RST_CSV_TABBLE: RstCsvTableWriter,
        })

        return writer_mapping

    @classmethod
    def __get_extension_writer_mapping(cls):
        """
        :return: Mappings of format-extension and writer class.
        :rtype: dict
        """

        writer_mapping = copy.deepcopy(cls.__COMMON_WRITER_TABLE)
        writer_mapping .update({
            "htm": HtmlTableWriter,
            "md": MarkdownTableWriter,
            "sqlite3": SqliteTableWriter,
            "xls": ExcelXlsTableWriter,
            "xlsx": ExcelXlsxTableWriter,
        })

        return writer_mapping
