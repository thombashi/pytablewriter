# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import typepy

from ..._function import (
    quote_datetime_formatter,
    dateutil_datetime_formatter
)
from ._sourcecode import SourceCodeTableWriter


class PythonCodeTableWriter(SourceCodeTableWriter):
    """
    A table writer class for Python source code format.

    .. py:method:: write_table

        |write_table| with Python format.
        The tabular data are written as a nested list variable definition
        for Python format.

        :raises pytablewriter.EmptyTableNameError:
            If the |table_name| is empty.
        :raises pytablewriter.EmptyTableDataError:
            If the |header_list| and the |value_matrix| is empty.
        :Example:
            :ref:`example-python-code-table-writer`

        .. note::
            Specific values in the tabular data are converted when writing:

            - |None|: written as ``None``
            - |inf|: written as ``float("inf")``
            - |nan|: written as ``float("nan")``
            - |datetime| instances determined by |is_datetime_instance_formatting| attribute:
                - |True|: written as `dateutil.parser <https://dateutil.readthedocs.io/en/stable/parser.html>`__
                - |False|: written as |str|

            .. seealso::
                :ref:`example-type-hint-python`
    """

    @property
    def format_name(self):
        return "python"

    @property
    def support_split_write(self):
        return True

    def __init__(self):
        super(PythonCodeTableWriter, self).__init__()

        self.table_name = ""
        self._dp_extractor.type_value_mapping = {
            typepy.Typecode.NONE: None,
            typepy.Typecode.INFINITY: 'float("inf")',
            typepy.Typecode.NAN: 'float("nan")',
        }

    def get_variable_name(self, value):
        import pathvalidate

        return pathvalidate.sanitize_python_var_name(
            self.table_name, "_").lower()

    def _write_table(self):
        if self.is_datetime_instance_formatting:
            self._dp_extractor.datetime_formatter = dateutil_datetime_formatter
        else:
            self._dp_extractor.datetime_formatter = quote_datetime_formatter

        self.inc_indent_level()
        super(PythonCodeTableWriter, self)._write_table()
        self.dec_indent_level()

    def _get_opening_row_item_list(self):
        if typepy.is_not_null_string(self.table_name):
            return [self.variable_name + " = ["]

        return ["["]

    def _get_closing_row_item_list(self):
        return ["]"]
