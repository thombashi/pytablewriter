# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import dataproperty as dp
from mbstrdecoder import MultiByteStrDecoder

from .._error import EmptyTableNameError
from .._function import (
    str_datetime_converter,
    dateutil_datetime_converter
)
from ._text_writer import SourceCodeTableWriter


class PandasDataFrameWriter(SourceCodeTableWriter):
    """
    A writer class for Pandas DataFrame format.

    :Examples:

        :ref:`example-pandas-dataframe-writer`
    """

    @property
    def support_split_write(self):
        return True

    def __init__(self):
        super(PandasDataFrameWriter, self).__init__()

        self.table_name = u""

        self.is_write_header = False
        self._dp_extractor.inf_value = 'numpy.inf'
        self._dp_extractor.nan_value = 'numpy.nan'

    def write_table(self):
        """
        |write_table| with Pandas DataFrame format.
        The tabular data will be written as ``pandas.DataFrame`` class
        variable definition.

        :raises pytablewriter.EmptyTableNameError:
            If the |table_name| is empty.
        :raises pytablewriter.EmptyHeaderError: If the |header_list| is empty.

        .. note::

            - |None| values will be written as ``None``
            - |inf| values will be written as ``numpy.inf``
            - |nan| values will be written as ``numpy.nan``
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
        super(PandasDataFrameWriter, self).write_table()
        self.dec_indent_level()

        if any([
            dp.is_empty_sequence(self.value_matrix),
            not self.is_write_closing_row,
        ]):
            return

        self._write_line("{}.columns = [".format(self.variable_name))
        self.inc_indent_level()
        for header in self.header_list:
            self._write_line(
                '"{}",'.format(MultiByteStrDecoder(header).unicode_str))
        self.dec_indent_level()
        self._write_line("]")

    def _get_opening_row_item_list(self):
        return [self.variable_name + " = pandas.DataFrame(["]

    def _get_closing_row_item_list(self):
        return "])"

    def _verify_property(self):
        super(PandasDataFrameWriter, self)._verify_property()

        if dp.is_empty_string(self.table_name):
            raise EmptyTableNameError()

    def _verify_header(self):
        self._validate_empty_header()
