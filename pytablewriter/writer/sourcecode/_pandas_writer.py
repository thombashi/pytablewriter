# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

from mbstrdecoder import MultiByteStrDecoder
import typepy

from ..._const import TableFormat
from ..._error import EmptyTableNameError
from ..._function import (
    quote_datetime_formatter,
    dateutil_datetime_formatter
)
from ._sourcecode_writer import SourceCodeTableWriter


class PandasDataFrameWriter(SourceCodeTableWriter):
    """
    A writer class for Pandas DataFrame format.

    :Examples:

        :ref:`example-pandas-dataframe-writer`

    .. py:method:: write_table

        |write_table| with Pandas DataFrame format.
        The tabular data will be written as ``pandas.DataFrame`` class
        variable definition.

        :raises pytablewriter.EmptyTableNameError:
            If the |table_name| is empty.
        :raises pytablewriter.EmptyHeaderError: If the |header_list| is empty.

        .. note::

            Values in the tabular data which described below will be converted
            when writing:

            - |None|: written as ``None``
            - |inf|: written as ``numpy.inf``
            - |nan|: written as ``numpy.nan``
            - |datetime| instances determined by |is_datetime_instance_formatting| attribute:
                - |True|: written as `dateutil.parser <https://dateutil.readthedocs.io/en/stable/parser.html>`__
                - |False|: written as |str|

            .. seealso::

                :ref:`example-type-hint-python`
    """

    @property
    def format_name(self):
        return TableFormat.PANDAS

    @property
    def support_split_write(self):
        return True

    def __init__(self):
        super(PandasDataFrameWriter, self).__init__()

        self.table_name = u""

        self.is_write_header = False
        self._dp_extractor.type_value_mapping = {
            typepy.Typecode.NONE: None,
            typepy.Typecode.INFINITY: 'numpy.inf',
            typepy.Typecode.NAN: 'numpy.nan',
        }

    def get_variable_name(self, value):
        import pathvalidate

        return pathvalidate.sanitize_python_var_name(
            self.table_name, "_").lower()

    def _write_table(self):
        self._verify_property()

        if self.is_datetime_instance_formatting:
            self._dp_extractor.datetime_formatter = dateutil_datetime_formatter
        else:
            self._dp_extractor.datetime_formatter = quote_datetime_formatter

        self.inc_indent_level()
        super(PandasDataFrameWriter, self)._write_table()
        self.dec_indent_level()

    def _get_opening_row_item_list(self):
        return ["{} = pandas.DataFrame([".format(self.variable_name)]

    def _get_closing_row_item_list(self):
        return "], columns=[{}])".format(", ".join([
            '"{}"'.format(MultiByteStrDecoder(header).unicode_str)
            for header in self.header_list
        ]))

    def _verify_property(self):
        super(PandasDataFrameWriter, self)._verify_property()

        if typepy.is_null_string(self.table_name):
            raise EmptyTableNameError(
                "table_name must be a string of one or more characters")

    def _verify_header(self):
        self._validate_empty_header()
