# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import copy

from mbstrdecoder import MultiByteStrDecoder
import typepy

import dataproperty as dp

from ._text_writer import IndentationTextTableWriter


class MarkdownTableWriter(IndentationTextTableWriter):
    """
    A table writer class for Markdown format.
    """

    @property
    def format_name(self):
        return "markdown"

    @property
    def support_split_write(self):
        return True

    def __init__(self):
        super(MarkdownTableWriter, self).__init__()

        self.indent_string = ""
        self.column_delimiter = "|"
        self.char_left_side_row = "|"
        self.char_right_side_row = "|"
        self.char_cross_point = "|"
        self.is_write_opening_row = True
        self._use_default_header = True

        self._is_require_header = True
        self._quoting_flags = copy.deepcopy(dp.NOT_QUOTING_FLAGS)
        self._dp_extractor.min_column_width = 3

    def _get_header_item(self, col_dp, value_dp):
        return self.__escape_vertical_bar_char(
            super(MarkdownTableWriter, self)._get_header_item(
                col_dp, value_dp))

    def _get_row_item(self, col_dp, value_dp):
        return self.__escape_vertical_bar_char(
            super(MarkdownTableWriter, self)._get_row_item(col_dp, value_dp))

    def _get_opening_row_item_list(self):
        return []

    def _get_header_row_separator_item_list(self):
        header_separator_list = []
        for col_dp in self._column_dp_list:
            padding_len = self._get_padding_len(col_dp)

            if col_dp.align == dp.Align.RIGHT:
                separator_item = "-" * (padding_len - 1) + ":"
            elif col_dp.align == dp.Align.CENTER:
                separator_item = ":" + "-" * (padding_len - 2) + ":"
            else:
                separator_item = "-" * padding_len

            header_separator_list.append(separator_item)

        return header_separator_list

    def _get_value_row_separator_item_list(self):
        return []

    def _get_closing_row_item_list(self):
        return []

    def write_table(self):
        """
        |write_table| with Markdown table format.

        :raises pytablewriter.EmptyHeaderError: If the |header_list| is empty.
        :Example:
            :ref:`example-markdown-table-writer`

        .. note::
            - |None| values are written as an empty string
            - Vertical bar characters (``'|'``) in table items are escaped
        """

        self._logger.logging_start_write()
        self._verify_property()
        self.__write_chapter()
        self._write_table()
        if self.is_write_null_line_after_table:
            self.write_null_line()
        self._logger.logging_complete_write()

    def _write_table_iter(self):
        self.__write_chapter()
        super(MarkdownTableWriter, self)._write_table_iter()

    def __write_chapter(self):
        if typepy.is_null_string(self.table_name):
            return

        self._write_line("{:s} {:s}".format(
            "#" * (self._indent_level + 1),
            MultiByteStrDecoder(self.table_name).unicode_str))

    @staticmethod
    def __escape_vertical_bar_char(value):
        return value.replace("|", "\|")
