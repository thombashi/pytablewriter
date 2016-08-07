# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import dataproperty

from ._error import EmptyHeaderError
from ._text_writer import IndentationTextTableWriter


class MarkdownTableWriter(IndentationTextTableWriter):
    """
    Concrete class of a table writer for Markdown format.

    :Examples:

        :ref:`example-markdown-table-writer`
    """

    @property
    def support_split_write(self):
        return True

    def __init__(self):
        super(MarkdownTableWriter, self).__init__()

        self.indent_string = u""
        self.column_delimiter = u"|"
        self.char_cross_point = u"|"
        self.is_write_opening_row = True
        self.is_quote_header = False
        self.is_quote_table[dataproperty.Typecode.STRING] = False
        self.is_quote_table[dataproperty.Typecode.DATETIME] = False

        self._prop_extractor.min_padding_len = 3

    def write_table(self):
        """
        |write_table| with Markdown table format.

        :raises pytablewriter.EmptyHeaderError: If the |header_list| is empty.

        .. note::

            - |None| is not written
        """

        super(MarkdownTableWriter, self).write_table()

    def _verify_header(self):
        if dataproperty.is_empty_sequence(self.header_list):
            raise EmptyHeaderError()

    def _get_opening_row_item_list(self):
        if dataproperty.is_empty_string(self.table_name):
            return []

        return [u"#" * (self._indent_level + 1) + u" " + self.table_name]

    def _get_header_row_separator_item_list(self):
        header_separator_list = []
        for col_prop in self._column_prop_list:
            padding_len = self._get_padding_len(col_prop)

            if col_prop.align == dataproperty.Align.RIGHT:
                separator_item = u"-" * (padding_len - 1) + u":"
            elif col_prop.align == dataproperty.Align.CENTER:
                separator_item = u":" + u"-" * (padding_len - 2) + u":"
            else:
                separator_item = u"-" * padding_len

            header_separator_list.append(separator_item)

        return header_separator_list

    def _get_value_row_separator_item_list(self):
        return []

    def _get_closing_row_item_list(self):
        return []
