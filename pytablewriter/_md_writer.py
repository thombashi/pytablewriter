# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import dataproperty

from ._text_writer import IndentationTextTableWriter


class MarkdownTableWriter(IndentationTextTableWriter):
    """
    Concrete class of a table writer for Markdown format.

    :Examples:

        :ref:`example-markdown-table-writer`
    """

    def __init__(self):
        super(MarkdownTableWriter, self).__init__()

        self.indent_string = u""
        self.column_delimiter = u"|"
        self.char_cross_point = u"|"
        self.is_quote_str = False

        self._prop_extractor.min_padding_len = 3

    def write_table(self):
        """
        |write_table| with Markdown table format.
        """

        if dataproperty.is_not_empty_string(self.table_name):
            self.__write_chapter(self.table_name)

        super(MarkdownTableWriter, self).write_table()

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

    def __write_chapter(self, text):
        if dataproperty.is_empty_string(text):
            return

        return self._write_raw_line(
            u"#" * (self._indent_level + 1) + u" " + text)
