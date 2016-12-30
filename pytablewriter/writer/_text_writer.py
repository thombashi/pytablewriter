# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import dataproperty as dp
from six.moves import zip

from .._error import EmptyHeaderError
from ._table_writer import AbstractTableWriter
from ._interface import (
    IndentationInterface,
    TextWriterInterface
)


class TextTableWriter(AbstractTableWriter, TextWriterInterface):
    """
    Base class of table writer with text format.

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

        self.column_delimiter = "|"
        self.char_left_side_row = ""
        self.char_right_side_row = ""
        self.char_cross_point = ""

        self.char_opening_row = "-"
        self.char_header_row_separator = "-"
        self.char_value_row_separator = "-"
        self.char_closing_row = "-"

    def write_null_line(self):
        """
        Write a null line to the |stream|.
        """

        self._write_line()

    def write_table(self):
        """
        |write_table|.

        .. note::

            - |None| values will be written as an empty string.
        """

        self._verify_property()
        self._preprocess()

        self._write_opening_row()

        try:
            self._write_header()
            self.__write_header_row_separator()
        except EmptyHeaderError:
            pass

        is_first_value_row = True
        for value_list, value_prop_list in zip(self._value_matrix, self._value_prop_matrix):
            try:
                if is_first_value_row:
                    is_first_value_row = False
                else:
                    if self.is_write_value_separator_row:
                        self._write_value_row_separator()

                self._write_value_row(value_list, value_prop_list)
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

    def _get_header_item(self, col_prop, value_prop):
        from dataproperty import StringType

        format_string = self._get_header_format_string(col_prop, value_prop)
        item = format_string.format(StringType(value_prop.data).convert())

        if self.is_quote_header:
            return u'"{:s}"'.format(item)

        return item

    def _get_header_format_string(self, col_prop, value_prop):
        return "{{:{:s}{:s}}}".format(
            self._get_center_align_formatformat(),
            str(self._get_padding_len(col_prop, value_prop)))

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
        if dp.is_empty_sequence(value_list):
            return

        self._write_line(
            self.char_left_side_row +
            self.column_delimiter.join(value_list) +
            self.char_right_side_row)

    def _write_header(self):
        if not self.is_write_header:
            return

        if dp.is_empty_sequence(self.header_list):
            raise EmptyHeaderError()

        if dp.is_empty_sequence(self._column_prop_list):
            self._write_row(self.header_list)
            return

        self._write_row([
            self._get_header_item(
                col_prop,
                dp.DataProperty(
                    header, strict_type_mapping=dp.STRICT_TYPE_MAPPING)
            )
            for col_prop, header in
            zip(self._column_prop_list, self.header_list)
        ])

    def _write_value_row(self, value_list, value_prop_list):
        self._write_row(value_list)

    def __get_row_separator_item_list(self, separator_char):
        return [
            separator_char * self._get_padding_len(col_prop)
            for col_prop in self._column_prop_list
        ]

    def __write_separator_row(self, value_list):
        if dp.is_empty_sequence(value_list):
            return

        left_cross_point = self.char_cross_point
        right_cross_point = self.char_cross_point
        if dp.is_empty_string(self.char_left_side_row):
            left_cross_point = ""
        if dp.is_empty_string(self.char_right_side_row):
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
        regardless of the value of the :py:attr:`.is_write_value_separator_row`.
        """

        self.__write_separator_row(self._get_value_row_separator_item_list())

    def _write_closing_row(self):
        if not self.is_write_closing_row:
            return

        self.__write_separator_row(self._get_closing_row_item_list())


class IndentationTextTableWriter(TextTableWriter, IndentationInterface):
    """
    Base class of table writer with indentation text format.

    .. py:attribute:: indent_string

        String of an indent for each level.
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
        self._write_raw_line(self._get_indent_string() + text)


class SourceCodeTableWriter(IndentationTextTableWriter):
    """
    Base class of table writer with source code (variable definition) format.

    .. py:attribute:: is_datetime_instance_formatting

        Write |datetime| values in the table as definition of date time class
        instances coincide with specific language if this value is |True|.
        Write as |str| if this value is |False|.
    """

    @property
    def variable_name(self):
        """
        :return: |table_name| that converted to a variable name.
        :rtype: str
        """

        import pathvalidate

        return pathvalidate.sanitize_python_var_name(
            self.table_name, "_").lower()

    def __init__(self):
        super(SourceCodeTableWriter, self).__init__()

        self.indent_string = "    "
        self.column_delimiter = ", "
        self.char_left_side_row = "["
        self.char_right_side_row = "],"
        self.char_cross_point = ""
        self.is_padding = False
        self.is_write_header_separator_row = False
        self.is_write_opening_row = True
        self.is_write_closing_row = True

        self.is_datetime_instance_formatting = True
        self.quote_flag_table[dp.Typecode.DATETIME] = False
        self._prop_extractor.datetime_format_str = "s"

        self._is_required_table_name = True
        self._is_remove_line_break = True

        self._prop_extractor.none_value = None
        self._prop_extractor.strict_type_mapping[
            dp.Typecode.DATETIME] = False

    def _get_value_row_separator_item_list(self):
        return []

    def _write_opening_row(self):
        self.dec_indent_level()
        super(SourceCodeTableWriter, self)._write_opening_row()
        self.inc_indent_level()

    def _write_closing_row(self):
        self.dec_indent_level()
        super(SourceCodeTableWriter, self)._write_closing_row()
        self.inc_indent_level()
