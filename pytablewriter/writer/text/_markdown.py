# encoding: utf-8

from __future__ import absolute_import, unicode_literals

import copy

import dataproperty as dp
import typepy
from mbstrdecoder import MultiByteStrDecoder

from ...style import Align, MarkdownStyler
from ._text_writer import IndentationTextTableWriter


class MarkdownTableWriter(IndentationTextTableWriter):
    """
    A table writer class for Markdown format.

        :Example:
            :ref:`example-markdown-table-writer`
    """

    FORMAT_NAME = "markdown"

    @property
    def format_name(self):
        return self.FORMAT_NAME

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

    def _to_header_item(self, col_dp, value_dp):
        return self.__escape_vertical_bar_char(
            super(MarkdownTableWriter, self)._to_header_item(col_dp, value_dp)
        )

    def _to_row_item(self, col_dp, value_dp):
        return self.__escape_vertical_bar_char(
            super(MarkdownTableWriter, self)._to_row_item(col_dp, value_dp)
        )

    def _get_opening_row_item_list(self):
        return []

    def _get_header_row_separator_item_list(self):
        header_separator_list = []
        for col_dp in self._column_dp_list:
            padding_len = self._get_padding_len(col_dp) + self.margin * 2
            align = self._get_align(col_dp.column_index, col_dp.align)

            if align == Align.RIGHT:
                separator_item = "-" * (padding_len - 1) + ":"
            elif align == Align.CENTER:
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

        with self._logger:
            self._verify_property()
            self.__write_chapter()
            self._write_table()
            if self.is_write_null_line_after_table:
                self.write_null_line()

    def _write_table_iter(self):
        self.__write_chapter()
        super(MarkdownTableWriter, self)._write_table_iter()

    def __write_chapter(self):
        if typepy.is_null_string(self.table_name):
            return

        self._write_line(
            "{:s} {:s}".format(
                "#" * (self._indent_level + 1), MultiByteStrDecoder(self.table_name).unicode_str
            )
        )

    def _create_styler(self, style, writer):
        return MarkdownStyler(style, writer)

    @staticmethod
    def __escape_vertical_bar_char(value):
        return value.replace("|", r"\|")
