# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import abc

import typepy

from .._text_writer import IndentationTextTableWriter


class SourceCodeTableWriter(IndentationTextTableWriter):
    """
    Base class of table writer with a source code (variable definition) format.

    .. py:attribute:: is_datetime_instance_formatting

        Write |datetime| values in the table as definition of |datetime| class
        instances coincide with specific language if this value is |True|.
        Write as |str| if this value is |False|.
    """

    @abc.abstractmethod
    def get_variable_name(self, value):  # pragma: no cover
        pass

    @property
    def variable_name(self):
        """
        Return a valid variable name that converted from the |table_name|.

        :return: A variable name.
        :rtype: str
        """

        return self.get_variable_name(self.table_name)

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

        self.is_formatting_float = False
        self.is_datetime_instance_formatting = True

        self._quoting_flags[typepy.Typecode.DATETIME] = False
        self._is_require_table_name = True
        self._is_remove_line_break = True

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
