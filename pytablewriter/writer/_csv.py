# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import typepy

from ._text_writer import TextTableWriter


class CsvTableWriter(TextTableWriter):
    """
    A table writer class for character separated values format.
    The default separated character is a comma (``","``).

    :Example:
        :ref:`example-csv-table-writer`
    """

    @property
    def format_name(self):
        return "csv"

    @property
    def support_split_write(self):
        return True

    def __init__(self):
        super(CsvTableWriter, self).__init__()

        self.indent_string = ""
        self.column_delimiter = ","
        self.is_padding = False
        self.is_formatting_float = False
        self.is_write_header_separator_row = False
        self.is_write_null_line_after_table = False

        self._quoting_flags[typepy.Typecode.NULL_STRING] = False

    def _write_header(self):
        if typepy.is_empty_sequence(self.header_list):
            return

        super(CsvTableWriter, self)._write_header()

    def _get_opening_row_item_list(self):
        return []

    def _get_value_row_separator_item_list(self):
        return []

    def _get_closing_row_item_list(self):
        return []
