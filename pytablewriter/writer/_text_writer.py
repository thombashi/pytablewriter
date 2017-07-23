# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import dataproperty
import typepy

from six.moves import zip

from .._error import EmptyHeaderError
from ._interface import (
    IndentationInterface,
    TextWriterInterface
)
from ._table_writer import AbstractTableWriter


class TextTableWriter(AbstractTableWriter, TextWriterInterface):
    """
    A base class for table writer with text formats.

    .. py:attribute:: column_delimiter

        A column delimiter of a table.

    .. py:attribute:: char_left_side_row

        A character of a left side of a row.

    .. py:attribute:: char_right_side_row

        A character of a right side of a row.

    .. py:attribute:: char_cross_point

        A character of the crossing point of column delimiter and row
        delimiter.

    .. py:attribute:: char_opening_row

        A character of the first line of a table.

    .. py:attribute:: char_header_row_separator

        A character of a separator line of the header and
        the body of the table.

    .. py:attribute:: char_value_row_separator

        A character of a row separator line of the table.

    .. py:attribute:: char_closing_row

        A character of the last line of a table.

    .. py:attribute:: is_write_header_separator_row

        Write a header separator line of the table if the value is |True|.

    .. py:attribute:: is_write_value_separator_row

        Write row separator line(s) of the table if the value is |True|.

    .. py:attribute:: is_write_opening_row

        Write an opening line of the table if the value is |True|.

    .. py:attribute:: is_write_closing_row

        Write a closing line of the table if the value is |True|.

    .. py:attribute:: is_write_null_line_after_table

        Write a blank line of after writing a table if the value is |True|.

    .. figure:: ss/table_char.png
       :scale: 60%
       :alt: table_char

       Character attributes that compose a table
    """

    def __init__(self):
        super(TextTableWriter, self).__init__()

        self.column_delimiter = "|"
        self.char_left_side_row = ""
        self.char_right_side_row = ""
        self.char_cross_point = ""

        self.char_opening_row = "-"
        self.char_header_row_separator = "-"
        self.char_value_row_separator = "-"
        self.char_closing_row = "-"

        self._is_remove_line_break = True
        self.is_write_null_line_after_table = True

    def write_null_line(self):
        """
        Write a null line to the |stream|.
        """

        self._write_line()

    def write_table(self):
        """
        |write_table|.

        .. note::
            - |None| values are written as an empty string.
        """

        super(TextTableWriter, self).write_table()
        if self.is_write_null_line_after_table:
            self.write_null_line()

    def _write_table_iter(self):
        super(TextTableWriter, self)._write_table_iter()
        if self.is_write_null_line_after_table:
            self.write_null_line()

    def _write_table(self):
        self._preprocess()
        self._write_opening_row()

        try:
            self._write_header()
            self.__write_header_row_separator()
        except EmptyHeaderError:
            pass

        is_first_value_row = True
        for value_list, value_dp_list in zip(
                self._value_matrix, self._value_dp_matrix):
            try:
                if is_first_value_row:
                    is_first_value_row = False
                else:
                    if self.is_write_value_separator_row:
                        self._write_value_row_separator()

                self._write_value_row(value_list, value_dp_list)
            except TypeError:
                continue

        self._write_closing_row()

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

    def _get_header_format_string(self, col_dp, value_dp):
        return "{{:{:s}{:s}}}".format(
            self._get_align_char(dataproperty.Align.CENTER),
            str(self._get_padding_len(col_dp, value_dp)))

    def _write_raw_string(self, unicode_text):
        self._verify_stream()

        self.stream.write(unicode_text)

    def _write_raw_line(self, unicode_text=""):
        self._write_raw_string(unicode_text + "\n")

    def _write(self, text):
        self._write_raw_string(text)

    def _write_line(self, text=""):
        self._write_raw_line(text)

    def _write_row(self, value_list):
        if typepy.is_empty_sequence(value_list):
            return

        self._write_line(
            self.char_left_side_row +
            self.column_delimiter.join(value_list) +
            self.char_right_side_row)

    def _write_header(self):
        if not self.is_write_header:
            return

        if typepy.is_empty_sequence(self._header_list):
            raise EmptyHeaderError("header is empty")

        self._write_row(self._header_list)

    def _write_value_row(self, value_list, value_dp_list):
        self._write_row(value_list)

    def __get_row_separator_item_list(self, separator_char):
        return [
            separator_char * self._get_padding_len(col_dp)
            for col_dp in self._column_dp_list
        ]

    def __write_separator_row(self, value_list):
        if typepy.is_empty_sequence(value_list):
            return

        left_cross_point = self.char_cross_point
        right_cross_point = self.char_cross_point
        if typepy.is_null_string(self.char_left_side_row):
            left_cross_point = ""
        if typepy.is_null_string(self.char_right_side_row):
            right_cross_point = ""

        self._write_line(
            left_cross_point +
            self.char_cross_point.join(value_list) +
            right_cross_point)

    def _write_opening_row(self):
        if not self.is_write_opening_row:
            return

        self.__write_separator_row(self._get_opening_row_item_list())

    def __write_header_row_separator(self):
        if any([
                not self.is_write_header,
                not self.is_write_header_separator_row,
        ]):
            return

        self.__write_separator_row(self._get_header_row_separator_item_list())

    def _write_value_row_separator(self):
        """
        Write row separator of the table which matched to the table type
        regardless of the value of the
        :py:attr:`.is_write_value_separator_row`.
        """

        self.__write_separator_row(self._get_value_row_separator_item_list())

    def _write_closing_row(self):
        if not self.is_write_closing_row:
            return

        self.__write_separator_row(self._get_closing_row_item_list())


class IndentationTextTableWriter(TextTableWriter, IndentationInterface):
    """
    A base class for table writer with indentation text formats.

    .. py:attribute:: indent_string

        Indentation string for each level.
    """

    def __init__(self):
        super(IndentationTextTableWriter, self).__init__()

        self.set_indent_level(0)
        self.indent_string = ""

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

    def _write_line(self, text=""):
        if typepy.is_not_null_string(text):
            self._write_raw_line(self._get_indent_string() + text)
        else:
            self._write_raw_line("")
