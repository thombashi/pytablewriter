# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
try:
    import json
except ImportError:
    import simplejson as json

import dataproperty

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

    def write_null_line(self):
        self._verify_stream()
        self.stream.write(u"\n")

    def write_table(self):
        """
        |write_table| with JSON format.
        """

        self._verify_property()
        self._preprocess_value_matrix()

        self.stream.write(
            json.dumps(self._value_matrix, sort_keys=True, indent=4) + u"\n")

    def _preprocess_value_matrix(self):
        if self._preprocessed_value_matrix:
            return

        value_matrix = [
            [dataproperty.convert_value(value) for value in value_list]
            for value_list in self.value_matrix
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
