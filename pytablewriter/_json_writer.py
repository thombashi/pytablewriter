# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
try:
    import json
except ImportError:   # pragma: no cover
    import simplejson as json

import dataproperty

from ._converter import lower_bool_converter
from ._converter import strip_quote
from ._interface import TextWriterInterface
from ._table_writer import TableWriter


class JsonTableWriter(TableWriter, TextWriterInterface):
    """
    Concrete class of a table writer for JSON format.

    :Examples:

        :ref:`example-json-table-writer`
    """

    def __init__(self):
        super(JsonTableWriter, self).__init__()

        self._prop_extractor.none_value = "null"
        self._prop_extractor.inf_value = "Infinity"
        self._prop_extractor.nan_value = "NaN"
        self._prop_extractor.bool_converter = lower_bool_converter

    def write_null_line(self):
        self._verify_stream()
        self.stream.write(u"\n")

    def write_table(self):
        """
        |write_table| with JSON format.
        """

        self._verify_property()
        self._preprocess_value_matrix()

        json_text = json.dumps(
            self._value_matrix, sort_keys=True, indent=4) + u"\n"
        json_text = strip_quote(json_text, self._prop_extractor.none_value)
        json_text = strip_quote(json_text, "true")
        json_text = strip_quote(json_text, "false")

        self.stream.write(json_text)

    def _preprocess_value_matrix(self):
        from ._function import _get_data_helper

        if self._preprocessed_value_matrix:
            return

        self._prop_extractor.data_matrix = self.value_matrix
        value_matrix = [
            [_get_data_helper(data_prop) for data_prop in prop_list]
            for prop_list
            in self._prop_extractor.extract_data_property_matrix()
        ]

        table_data = [
            dict(zip(self.header_list, value_list))
            for value_list in value_matrix
        ]

        if dataproperty.is_empty_string(self.table_name):
            self._value_matrix = table_data
        else:
            self._value_matrix = {self.table_name: table_data}

        self._preprocessed_value_matrix = True
