# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import simplesqlite

import pytablereader as ptr

from .._const import TableFormat
from ._interface import BinaryWriterInterface
from ._table_writer import AbstractTableWriter


class SqliteTableWriter(AbstractTableWriter, BinaryWriterInterface):
    """
    A table writer class for SQLite database.

    .. py:method:: write_table()

        Write a table to a SQLite database.

        :raises pytablewriter.EmptyTableNameError:
            If the |table_name| is empty.
        :raises pytablewriter.EmptyHeaderError:
            If the |header_list| is empty.
        :raises pytablewriter.EmptyValueError:
            If the |value_matrix| is empty.

    :Examples:

        :ref:`example-sqlite-table-writer`
    """

    @property
    def format_name(self):
        return TableFormat.SQLITE

    @property
    def support_split_write(self):
        return True

    def __init__(self):
        super(SqliteTableWriter, self).__init__()

        self.stream = None
        self.is_padding = False
        self.is_float_formatting = False
        self._is_required_table_name = True

    def __del__(self):
        self.close()

    def open(self, database_path):
        self.close()

        self.stream = simplesqlite.SimpleSQLite(database_path, "w")

    def _verify_header(self):
        self._validate_empty_header()

    def _write_table(self):
        self._verify_property()
        self._verify_value_matrix()
        self._preprocess()

        self.stream.create_table_from_tabledata(ptr.TableData(
            self.table_name, self.header_list,
            [
                [value_dp.data for value_dp in value_dp_list]
                for value_dp_list in self._value_dp_matrix
            ]
        ))

    def _write_value_row_separator(self):
        pass
