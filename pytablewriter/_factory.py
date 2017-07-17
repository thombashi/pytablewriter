# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import os

import typepy

from ._error import WriterNotFoundError
from ._table_format import (
    FormatAttr,
    TableFormat,
)


class TableWriterFactory(object):
    """
    A factor class of table writer classes.
    """

    @classmethod
    def create_from_file_extension(cls, file_extension):
        """
        Create a table writer class instance from a file extension.
        Supported file extensions are as follows:

            ==================  ===================================
            Extension           Writer Class
            ==================  ===================================
            ``".csv"``          :py:class:`~.CsvTableWriter`
            ``".htm"``          :py:class:`~.HtmlTableWriter`
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
            Writer instance that coincides with the ``file_extension``.
        :rtype:
            :py:class:`~pytablewriter.writer._table_writer.TableWriterInterface`
        :raises pytablewriter.WriterNotFoundError:
            |WriterNotFoundError_desc| the file extension.
        """

        ext = os.path.splitext(file_extension)[1]
        if typepy.is_null_string(ext):
            file_extension = file_extension
        else:
            file_extension = ext

        file_extension = file_extension.lstrip(".").lower()

        for table_format in TableFormat:
            if file_extension not in table_format.file_extension_list:
                continue

            if table_format.format_attribute & FormatAttr.SECONDARY_EXT:
                continue

            return table_format.writer_class()

        raise WriterNotFoundError("\n".join([
            "{:s} (unknown file extension).".format(file_extension),
            "",
            "acceptable file extensions are: {}.".format(
                ", ".join(cls.get_extension_list())),
        ]))

    @classmethod
    def create_from_format_name(cls, format_name):
        """
        Create a table writer class instance from a format name.
        Supported file format names are as follows:

            ==============================  ===================================
            Format name                     Writer Class
            ==============================  ===================================
            ``"csv"``                       :py:class:`~.CsvTableWriter`
            ``"elasticsearch"``             :py:class:`~.ElasticsearchWriter`
            ``"excel"``                     :py:class:`~.ExcelXlsxTableWriter`
            ``"html"``/``"htm"``            :py:class:`~.HtmlTableWriter`
            ``"javascript"``/``"js"``       :py:class:`~.JavaScriptTableWriter`
            ``"json"``                      :py:class:`~.JsonTableWriter`
            ``"latex_matrix"``              :py:class:`~.LatexMatrixWriter`
            ``"latex_table"``               :py:class:`~.LatexTableWriter`
            ``"ltsv"``                      :py:class:`~.LtsvTableWriter`
            ``"markdown"``/``"md"``         :py:class:`~.MarkdownTableWriter`
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
        :return: Writer instance that coincides with the ``format_name``:
        :rtype:
            :py:class:`~pytablewriter.writer._table_writer.TableWriterInterface`
        :raises pytablewriter.WriterNotFoundError:
            |WriterNotFoundError_desc| for the format.
        """

        format_name = format_name.lower()

        for table_format in TableFormat:
            if any([
                    format_name not in table_format.name_list,
                    table_format.format_attribute & FormatAttr.SECONDARY_NAME,
            ]):
                continue

            return table_format.writer_class()

        raise WriterNotFoundError("\n".join([
            "{} (unknown format name).".format(format_name),
            "acceptable format names are: {}.".format(
                ", ".join(cls.get_format_name_list())),
        ]))

    @classmethod
    def get_format_name_list(cls):
        """
        :return: Available format names.
        :rtype: list

        :Example:
            .. code:: python

                >>> import pytablewriter as ptw
                >>> for name in ptw.TableWriterFactory.get_format_name_list():
                ...     print(name)
                ...
                csv
                elasticsearch
                excel
                htm
                html
                javascript
                js
                json
                latex_matrix
                latex_table
                ltsv
                markdown
                md
                mediawiki
                null
                numpy
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

        format_name_set = set()
        for table_format in TableFormat:
            for format_name in table_format.name_list:
                format_name_set.add(format_name)

        return sorted(list(format_name_set))

    @classmethod
    def get_extension_list(cls):
        """
        :return: Available file extensions.
        :rtype: list

        :Example:
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
                tex
                toml
                tsv
                xls
                xlsx
        """

        file_extension_set = set()
        for table_format in TableFormat:
            for file_extension in table_format.file_extension_list:
                file_extension_set.add(file_extension)

        return sorted(list(file_extension_set))
