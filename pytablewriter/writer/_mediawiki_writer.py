# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import re

import dataproperty as dp
from mbstrdecoder import MultiByteStrDecoder
from six.moves import zip

from ._text_writer import TextTableWriter


class MediaWikiTableWriter(TextTableWriter):
    """
    Concrete class of a table writer for MediaWiki format.

    :Examples:

        :ref:`example-mediawiki-table-writer`
    """

    __RE_TABLE_SEQUENCE = re.compile(u"^[\s]+[*|#]+")

    @property
    def support_split_write(self):
        return True

    def __init__(self):
        super(MediaWikiTableWriter, self).__init__()

        self.column_delimiter = u"\n"

        self.is_padding = False
        self.is_write_header_separator_row = True
        self.is_write_value_separator_row = True
        self.is_write_opening_row = True
        self.is_write_closing_row = True
        self.is_quote_header = False
        self.is_quote_table = {}

    def _write_header(self):
        if not self.is_write_header:
            return

        if dp.is_not_empty_string(self.table_name):
            self._write_line(
                u"|+" + MultiByteStrDecoder(self.table_name).unicode_str)

        super(MediaWikiTableWriter, self)._write_header()

    def _write_value_row(self, value_list, value_prop_list):
        self._write_row([
            self.__modify_table_element(value, value_prop)
            for value, value_prop, in zip(value_list, value_prop_list)
        ])

    def _get_opening_row_item_list(self):
        return u'{| class="wikitable"'

    def _get_header_row_separator_item_list(self):
        return [u"|-"]

    def _get_value_row_separator_item_list(self):
        return self._get_header_row_separator_item_list()

    def _get_closing_row_item_list(self):
        return u"|}"

    def _get_header_format_string(self, col_prop, value_prop):
        return u"! {{:{:s}{:s}}}".format(
            self._get_center_align_formatformat(),
            str(self._get_padding_len(col_prop, value_prop)))

    def __modify_table_element(self, value, value_prop):
        if value_prop.align is dp.Align.LEFT:
            forma_stirng = u'| {1:s}'
        else:
            forma_stirng = u'| style="text-align:{0:s}"| {1:s}'

        if self.__RE_TABLE_SEQUENCE.search(value) is not None:
            value = u"\n" + value.lstrip()

        return forma_stirng.format(
            value_prop.align.align_string, value)
