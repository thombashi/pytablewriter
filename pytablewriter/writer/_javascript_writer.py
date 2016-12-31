# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import six

from .._converter import lower_bool_converter
from .._function import str_datetime_converter
from ._text_writer import SourceCodeTableWriter


def js_datetime_converter(value):
    return 'new Date("{:s}")'.format(value.strftime("%Y-%m-%dT%H:%M:%S%z"))


class JavaScriptTableWriter(SourceCodeTableWriter):
    """
    A table writer for class JavaScript format.

    :Examples:

        :ref:`example-js-table-writer`
    """

    @property
    def support_split_write(self):
        return True

    def __init__(self):
        super(JavaScriptTableWriter, self).__init__()

        self._dp_extractor.none_value = "null"
        self._dp_extractor.inf_value = "Infinity"
        self._dp_extractor.nan_value = "NaN"
        self._dp_extractor.bool_converter = lower_bool_converter

    def write_table(self):
        """
        |write_table| with JavaScript nested list variable definition format.

        :raises pytablewriter.EmptyTableNameError:
            If the |table_name| is empty.
        :raises pytablewriter.EmptyTableDataError:
            If the |header_list| and the |value_matrix| is empty.

        .. note::

            - |None| values will be written as ``null``
            - |inf| values will be written as ``Infinity``
            - |nan| values will be written as ``NaN``
        """

        self._verify_property()

        if self.is_datetime_instance_formatting:
            self._dp_extractor.datetime_converter = js_datetime_converter
        else:
            self._dp_extractor.datetime_converter = str_datetime_converter

        self._preprocess()

        org_stream = self.stream
        self.stream = six.StringIO()

        self.inc_indent_level()
        super(JavaScriptTableWriter, self).write_table()
        self.dec_indent_level()
        data_frame_text = self.stream.getvalue().rstrip("\n")
        if self.is_write_closing_row:
            data_frame_line_list = data_frame_text.splitlines()
            data_frame_line_list[-2] = data_frame_line_list[-2].rstrip(",")
            data_frame_text = "\n".join(data_frame_line_list)

        self.stream.close()
        self.stream = org_stream

        self.dec_indent_level()
        self._write_line(data_frame_text)
        self.inc_indent_level()

    def _get_opening_row_item_list(self):
        return "var {:s} = [".format(self.variable_name)

    def _get_closing_row_item_list(self):
        return "];"
