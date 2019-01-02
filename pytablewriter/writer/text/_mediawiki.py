# encoding: utf-8

from __future__ import absolute_import, unicode_literals

import copy
import re

import dataproperty as dp
import typepy
from mbstrdecoder import MultiByteStrDecoder
from six.moves import zip

from ...style import Align
from .._table_writer import LineBreakHandling
from ._text_writer import TextTableWriter


class MediaWikiTableWriter(TextTableWriter):
    """
    A table writer class for MediaWiki format.

        :Example:
            :ref:`example-mediawiki-table-writer`
    """

    FORMAT_NAME = "mediawiki"
    __RE_TABLE_SEQUENCE = re.compile(r"^[\s]+[*|#]+")

    @property
    def format_name(self):
        return self.FORMAT_NAME

    @property
    def support_split_write(self):
        return True

    def __init__(self):
        super(MediaWikiTableWriter, self).__init__()

        self.column_delimiter = "\n"

        self.is_padding = False
        self.is_write_header_separator_row = True
        self.is_write_value_separator_row = True
        self.is_write_opening_row = True
        self.is_write_closing_row = True

        self.line_break_handling = LineBreakHandling.NOP

        self._quoting_flags = copy.deepcopy(dp.NOT_QUOTING_FLAGS)

    def _write_header(self):
        if not self.is_write_header:
            return

        if typepy.is_not_null_string(self.table_name):
            self._write_line("|+" + MultiByteStrDecoder(self.table_name).unicode_str)

        super(MediaWikiTableWriter, self)._write_header()

    def _write_value_row(self, value_list, value_dp_list):
        self._write_row(
            [
                self.__modify_table_element(value, value_dp)
                for value, value_dp, in zip(value_list, value_dp_list)
            ]
        )

    def _get_opening_row_item_list(self):
        return ['{| class="wikitable"']

    def _get_header_row_separator_item_list(self):
        return ["|-"]

    def _get_value_row_separator_item_list(self):
        return self._get_header_row_separator_item_list()

    def _get_closing_row_item_list(self):
        return ["|}"]

    def _get_header_format_string(self, col_dp, value_dp):
        return "! {{:{:s}{:s}}}".format(
            self._get_align_char(Align.CENTER), str(self._get_padding_len(col_dp, value_dp))
        )

    def __modify_table_element(self, value, value_dp):
        if value_dp.align is Align.LEFT:
            forma_stirng = "| {1:s}"
        else:
            forma_stirng = '| style="text-align:{0:s}"| {1:s}'

        if self.__RE_TABLE_SEQUENCE.search(value) is not None:
            value = "\n" + value.lstrip()

        return forma_stirng.format(value_dp.align.align_string, value)
