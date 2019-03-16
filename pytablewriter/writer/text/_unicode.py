# encoding: utf-8

from __future__ import absolute_import, unicode_literals

import copy

import dataproperty as dp

from ._text_writer import IndentationTextTableWriter


class UnicodeTableWriter(IndentationTextTableWriter):
    """
    A table writer class using Unicode characters.

        :Example:
            :ref:`example-unicode-table-writer`
    """

    FORMAT_NAME = "unicode"

    @property
    def format_name(self):
        return self.FORMAT_NAME

    @property
    def support_split_write(self):
        return True

    def __init__(self):
        super(UnicodeTableWriter, self).__init__()

        self.table_name = ""

        self.column_delimiter = "│"
        self.char_left_side_row = "│"
        self.char_right_side_row = "│"

        self.char_cross_point = "┼"
        self.char_left_cross_point = "├"
        self.char_right_cross_point = "┤"
        self.char_top_left_cross_point = "┌"
        self.char_top_right_cross_point = "┐"
        self.char_bottom_left_cross_point = "└"
        self.char_bottom_right_cross_point = "┘"

        self.char_opening_row = "─"
        self.char_opening_row_cross_point = "┬"

        self.char_header_row_separator = "─"
        self.char_value_row_separator = "─"

        self.char_closing_row = "─"
        self.char_closing_row_cross_point = "┴"

        self.indent_string = "    "
        self.is_write_header_separator_row = True
        self.is_write_value_separator_row = True
        self.is_write_opening_row = True
        self.is_write_closing_row = True

        self._quoting_flags = copy.deepcopy(dp.NOT_QUOTING_FLAGS)

        self._init_cross_point_maps()
