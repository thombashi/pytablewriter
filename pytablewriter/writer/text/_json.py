# encoding: utf-8

from __future__ import absolute_import, unicode_literals

import copy
from decimal import Decimal

import dataproperty
import typepy
from mbstrdecoder import MultiByteStrDecoder
from six.moves import zip

from ..._converter import strip_quote
from ._text_writer import IndentationTextTableWriter


try:
    import simplejson as json
except ImportError:
    import json


class JsonTableWriter(IndentationTextTableWriter):
    """
    A table writer class for JSON format.

        :Examples:
            :ref:`example-json-table-writer`

    .. py:method:: write_table

        |write_table| with JSON format.

        :raises pytablewriter.EmptyHeaderError: If the |header_list| is empty.
        :Examples:
            :ref:`example-json-table-writer`

        .. note::
            Specific values in the tabular data are converted when writing:

            - |None|: written as ``null``
            - |inf|: written as ``Infinity``
            - |nan|: written as ``NaN``
    """

    FORMAT_NAME = "json"

    @property
    def format_name(self):
        return self.FORMAT_NAME

    @property
    def support_split_write(self):
        return True

    def __init__(self):
        super(JsonTableWriter, self).__init__()

        self.is_formatting_float = False
        self.is_write_opening_row = True
        self.is_write_closing_row = True
        self.char_right_side_row = ","

        self._is_require_header = True
        self._dp_extractor.type_value_map = {
            typepy.Typecode.NONE: "null",
            typepy.Typecode.INFINITY: "Infinity",
            typepy.Typecode.NAN: "NaN",
        }
        self.value_map = {True: "true", False: "false"}
        self._quoting_flags = copy.deepcopy(dataproperty.NOT_QUOTING_FLAGS)

    def write_null_line(self):
        self._verify_stream()
        self.stream.write("\n")

    def _write_table(self):
        self._preprocess_value_matrix()

        with self._logger:
            self._write_opening_row()
            self.inc_indent_level()

            json_text_list = []
            for json_data in self._table_value_matrix:
                json_text = json.dumps(json_data, sort_keys=True, indent=4 * self._indent_level)
                json_text = strip_quote(
                    json_text, self._dp_extractor.type_value_map.get(typepy.Typecode.NONE)
                )
                json_text = strip_quote(json_text, "true")
                json_text = strip_quote(json_text, "false")
                json_text_list.append(json_text)

            joint_text = self.char_right_side_row + "\n"
            json_text = joint_text.join(json_text_list)
            if all([not self.is_write_closing_row, typepy.is_not_null_string(json_text)]):
                json_text += joint_text

            self.stream.write(json_text)

            self.dec_indent_level()
            self._write_closing_row()

    def _preprocess_value_matrix(self):
        if self._is_complete_value_matrix_preprocess:
            return

        try:
            dp_matrix = self._dp_extractor.to_dp_matrix(self.value_matrix)
        except TypeError:
            dp_matrix = []

        value_matrix = [[self.__get_data_helper(dp) for dp in dp_list] for dp_list in dp_matrix]

        self._table_value_matrix = [
            dict(zip(self.header_list, value_list)) for value_list in value_matrix
        ]

        self._is_complete_value_matrix_preprocess = True

    @staticmethod
    def __get_data_helper(dp):
        if dp.typecode == typepy.Typecode.REAL_NUMBER and isinstance(dp.data, Decimal):
            return float(dp.data)

        if dp.typecode == typepy.Typecode.DATETIME:
            return dp.to_str()

        return dp.data

    def _get_opening_row_item_list(self):
        if typepy.is_not_null_string(self.table_name):
            return ['{{ "{:s}" : ['.format(MultiByteStrDecoder(self.table_name).unicode_str)]

        return ["["]

    def _get_closing_row_item_list(self):
        if typepy.is_not_null_string(self.table_name):
            return ["]}"]

        return ["]"]
