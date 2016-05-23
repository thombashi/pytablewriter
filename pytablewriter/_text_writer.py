# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import dataproperty
from ._error import EmptyHeaderError
from ._table_writer import TableWriter
from ._interface import IndentationInterface
from ._interface import TextWriterInterface


class TextTableWriter(TableWriter, TextWriterInterface):
    """
    Base class of table writer that text format.

    .. py:attribute:: column_delimiter

        A column delimiter of a table.

    .. py:attribute:: char_left_side_row

        A character of a left sides of a row.

    .. py:attribute:: char_right_side_row

        A character of a right sides of a row.

    .. py:attribute:: char_cross_point

        A character of crossing point of column delimiter and row delimiter.

    .. py:attribute:: char_opening_row

        A character of the first line of a table.

    .. py:attribute:: char_header_row_separator

        A character of a separator line of the header and
        the body of the table.

    .. py:attribute:: char_value_row_separator

        A character of a row separator line of the table.

    .. py:attribute:: char_closing_row

        A character of the last line of a table.

    .. py:attribute:: is_write_header

        Write a header of the table if the value is |True|.

    .. py:attribute:: is_write_header_separator_row

        Write a header separator line of the table if the value is |True|.

    .. py:attribute:: is_write_value_separator_row

        Write row separator line(s) of the table if the value is |True|.

    .. py:attribute:: is_write_opening_row

        Write opening line of the table if the value is |True|.

    .. py:attribute:: is_write_closing_row

        Write closing line of the table if the value is |True|.

    .. figure:: ss/table_char.png
       :scale: 60%
       :alt: table_char

       Character attributes that compose a table
    """

    def __init__(self):
        super(TextTableWriter, self).__init__()

        self.column_delimiter = u"|"
        self.char_left_side_row = u""
        self.char_right_side_row = u""
        self.char_cross_point = u"+"

        self.char_opening_row = u"-"
        self.char_header_row_separator = u"-"
        self.char_value_row_separator = u"-"
        self.char_closing_row = u"-"

        self.is_write_header = True
        self.is_write_header_separator_row = True
        self.is_write_value_separator_row = False
        self.is_write_opening_row = False
        self.is_write_closing_row = False

    def write_null_line(self):
        """
        Write a null line to the |stream|.
        """

        self._write_line()

    def write_table(self):
        """
        |write_table|.
        """

        self._verify_property()
        self._preprocess()

        self.__write_opening_row()

        try:
            self._write_header()
            self.__write_header_row_separator()
        except EmptyHeaderError:
            pass

        is_first_value_row = True
        for value_list in self._value_matrix:
            try:
                if is_first_value_row:
                    is_first_value_row = False
                else:
                    self.__write_value_row_separator()

                self.__write_value_row(value_list)
            except TypeError:
                continue

        self.__write_closing_row()

    def _get_opening_row_item_list(self):
        return self.__get_row_separator_item_list(self.char_opening_row)

    def _get_header_row_separator_item_list(self):
        return self.__get_row_separator_item_list(
            self.char_header_row_separator)

    def _get_value_row_separator_item_list(self):
        return self.__get_row_separator_item_list(
            self.char_value_row_separator)

    def _get_closing_row_item_list(self):
        return self.__get_row_separator_item_list(self.char_closing_row)

    def _get_left_align_formatformat(self):
        return u"%%-%d%s"

    def _get_right_align_formatformat(self):
        return u"%%%d%s"

    def _get_center_align_formatformat(self):
        return self._get_left_align_formatformat()

    def _write_raw_string(self, unicode_text):
        self._verify_stream()

        self.stream.write(unicode_text)

    def _write_raw_line(self, unicode_text=u""):
        self._write_raw_string(unicode_text + u"\n")

    def _write(self, text):
        self._write_raw_string(text)

    def _write_line(self, text=u""):
        self._write_raw_line(text)

    def _write_header(self):
        if not self.is_write_header:
            return

        self.__write_value_row([
            self._get_row_item(
                col_prop, dataproperty.DataProperty(header), is_header=True)
            for col_prop, header in
            zip(self._column_prop_list, self.header_list)
        ])

    def __get_row_separator_item_list(self, separator_char):
        return [
            separator_char * self._get_padding_len(col_prop)
            for col_prop in self._column_prop_list
        ]

    def __write_separator_row(self, value_list):
        if dataproperty.is_empty_list_or_tuple(value_list):
            return

        left_cross_point = self.char_cross_point
        right_cross_point = self.char_cross_point
        if dataproperty.is_empty_string(self.char_left_side_row):
            left_cross_point = u""
        if dataproperty.is_empty_string(self.char_right_side_row):
            right_cross_point = u""

        self._write_line(
            left_cross_point +
            self.char_cross_point.join(value_list) +
            right_cross_point)

    def __write_value_row(self, value_list):
        if dataproperty.is_empty_list_or_tuple(value_list):
            return

        self._write_line(
            self.char_left_side_row +
            self.column_delimiter.join(value_list) +
            self.char_right_side_row)

    def __write_opening_row(self):
        if not self.is_write_opening_row:
            return

        self.__write_separator_row(self._get_opening_row_item_list())

    def __write_header_row_separator(self):
        if not self.is_write_header_separator_row:
            return

        self.__write_separator_row(self._get_header_row_separator_item_list())

    def __write_value_row_separator(self):
        if not self.is_write_value_separator_row:
            return

        self.__write_separator_row(self._get_value_row_separator_item_list())

    def __write_closing_row(self):
        if not self.is_write_closing_row:
            return

        self.__write_separator_row(self._get_closing_row_item_list())


class IndentationTextTableWriter(TextTableWriter, IndentationInterface):

    def __init__(self):
        super(IndentationTextTableWriter, self).__init__()

        self.set_indent_level(0)
        self.indent_string = u""

    def set_indent_level(self, indent_level):
        """
        Set the current indent level.

        :param int indent_level: New indent level.
        """

        self._indent_level = indent_level

    def inc_indent_level(self):
        """
        Increment the current indent level.
        """

        self._indent_level += 1

    def dec_indent_level(self):
        """
        Decrement the current indent level.
        """

        self._indent_level -= 1

    def _get_indent_string(self):
        return self.indent_string * self._indent_level

    def _write(self, text):
        self._write_raw_string(self._get_indent_string() + text)

    def _write_line(self, text=u""):
        self._write_raw_line(self._get_indent_string() + text)


class SourceCodeTableWriter(IndentationTextTableWriter):

    def __init__(self):
        super(SourceCodeTableWriter, self).__init__()

        self.indent_string = u"    "
        self.column_delimiter = u", "
        self.char_left_side_row = u"["
        self.char_right_side_row = u"],"
        self.is_padding = False
        self.is_write_header_separator_row = False
