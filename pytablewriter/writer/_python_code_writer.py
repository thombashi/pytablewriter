# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import dataproperty as dp

from .._function import (
    str_datetime_converter,
    dateutil_datetime_converter
)
from ._text_writer import SourceCodeTableWriter


class PythonCodeTableWriter(SourceCodeTableWriter):
    """
    A table writer class for Python source code format.

    :Examples:

        :ref:`example-python-code-table-writer`
    """

    @property
    def support_split_write(self):
        return True

    def __init__(self):
        super(PythonCodeTableWriter, self).__init__()

        self.table_name = ""
        self._dp_extractor.inf_value = 'float("inf")'
        self._dp_extractor.nan_value = 'float("nan")'

    def write_table(self):
        """
        |write_table| with Python format.
        The tabular data will be written as nested list variable definition
        for Python format.

        :raises pytablewriter.EmptyTableNameError:
            If the |table_name| is empty.
        :raises pytablewriter.EmptyTableDataError:
            If the |header_list| and the |value_matrix| is empty.

        .. note::

            - |None| values will be written as ``None``
            - |inf| values will be written as ``float("inf")'``
            - |nan| values will be written as ``float("nan")'``
            - |datetime| instance is determined by |is_datetime_instance_formatting| attribute:
                - |True|: written by using `dateutil.parser <https://dateutil.readthedocs.io/en/stable/parser.html>`__
                - |False|: written as |str|
        """

        self._verify_property()

        if self.is_datetime_instance_formatting:
            self._dp_extractor.datetime_converter = dateutil_datetime_converter
        else:
            self._dp_extractor.datetime_converter = str_datetime_converter

        self.inc_indent_level()
        super(PythonCodeTableWriter, self).write_table()
        self.dec_indent_level()

    def _get_opening_row_item_list(self):
        if dp.is_not_empty_string(self.table_name):
            return [self.variable_name + " = ["]

        return "["

    def _get_closing_row_item_list(self):
        return "]"
