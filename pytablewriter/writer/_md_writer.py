# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import copy

from mbstrdecoder import MultiByteStrDecoder
import typepy

import dataproperty as dp

from .._const import FormatName
from ._text_writer import IndentationTextTableWriter


class MarkdownTableWriter(IndentationTextTableWriter):
    """
    Atable writer class for Markdown format.

    :Examples:

        :ref:`example-markdown-table-writer`
    """

    @property
    def format_name(self):
        return FormatName.MARKDOWN

    @property
    def support_split_write(self):
        return True

    def __init__(self):
        super(MarkdownTableWriter, self).__init__()

        self.indent_string = ""
        self.column_delimiter = "|"
        self.char_cross_point = "|"
        self.is_write_opening_row = True

        self._quote_flag_mapping = copy.deepcopy(dp.NULL_QUOTE_FLAG_MAPPING)
        self._is_remove_line_break = True

        self._dp_extractor.min_column_width = 3

    def write_table(self):
        """
        |write_table| with Markdown table format.

        :raises pytablewriter.EmptyHeaderError: If the |header_list| is empty.

        .. note::

            - |None| values will be written as an empty string.
        """

        super(MarkdownTableWriter, self).write_table()

    def _verify_header(self):
        self._validate_empty_header()

    def _get_header_format_string(self, col_dp, value_dp):
        if col_dp.column_index == 0:
            # if the first column header has five or more spaces at
            # the beginning, the table data not properly rendered at GitHub.

            return "{{:{:s}{:s}}}".format(
                self._get_align_char(dp.Align.LEFT),
                str(self._get_padding_len(col_dp, value_dp)))

        return super(MarkdownTableWriter, self)._get_header_format_string(
            col_dp, value_dp)

    def _get_opening_row_item_list(self):
        if typepy.is_null_string(self.table_name):
            return []

        return [
            "#" * (self._indent_level + 1) + " " +
            MultiByteStrDecoder(self.table_name).unicode_str
        ]

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
