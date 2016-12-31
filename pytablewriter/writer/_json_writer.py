# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals
import json

import dataproperty as dp
from mbstrdecoder import MultiByteStrDecoder
from six.moves import zip

from .._converter import (
    lower_bool_converter,
    strip_quote
)
from .._function import _get_data_helper
from ._text_writer import IndentationTextTableWriter


class JsonTableWriter(IndentationTextTableWriter):
    """
    A table writer class for JSON format.

    :Examples:

        :ref:`example-json-table-writer`
    """

    @property
    def support_split_write(self):
        return True

    def __init__(self):
        super(JsonTableWriter, self).__init__()

        self.is_write_opening_row = True
        self.is_write_closing_row = True
        self.char_right_side_row = ","

        self._dp_extractor.none_value = "null"
        self._dp_extractor.inf_value = "Infinity"
        self._dp_extractor.nan_value = "NaN"
        self._dp_extractor.bool_converter = lower_bool_converter

    def write_null_line(self):
        self._verify_stream()
        self.stream.write("\n")

    def write_table(self):
        """
        |write_table| with JSON format.

        :raises pytablewriter.EmptyHeaderError: If the |header_list| is empty.

        .. note::

            - |None| values will be written as ``null``
            - |inf| values will be written as ``"Infinity"``
            - |nan| values will be written as ``"NaN"``
        """

        self._verify_property()
        self._preprocess_value_matrix()

        self._write_opening_row()
        self.inc_indent_level()

        json_text_list = []
        for json_data in self._value_matrix:
            json_text = json.dumps(
                json_data, sort_keys=True, indent=4 * self._indent_level)
            json_text = strip_quote(json_text, self._dp_extractor.none_value)
            json_text = strip_quote(json_text, "true")
            json_text = strip_quote(json_text, "false")
            json_text_list.append(json_text)

        joint_text = self.char_right_side_row + "\n"
        json_text = joint_text.join(json_text_list)
        if all([
            not self.is_write_closing_row,
            dp.is_not_empty_string(json_text),
        ]):
            json_text += joint_text

        self.stream.write(json_text)

        self.dec_indent_level()
        self._write_closing_row()

    def _verify_header(self):
        self._validate_empty_header()

    def _preprocess_value_matrix(self):
        if self._preprocessed_value_matrix:
            return

        self._dp_extractor.data_matrix = self.value_matrix

        try:
            dp_matrix = self._dp_extractor.to_dataproperty_matrix()
        except TypeError:
            dp_matrix = []

        value_matrix = [
            [_get_data_helper(dp) for dp in dp_list]
            for dp_list in dp_matrix
        ]

        self._value_matrix = [
            dict(zip(self.header_list, value_list))
            for value_list in value_matrix
        ]

        self._preprocessed_value_matrix = True

    def _get_opening_row_item_list(self):
        if dp.is_not_empty_string(self.table_name):
            return '{{ "{:s}" : ['.format(
                MultiByteStrDecoder(self.table_name).unicode_str)

        return "["

    def _get_closing_row_item_list(self):
        if dp.is_not_empty_string(self.table_name):
            return "]}"

        return "]"
