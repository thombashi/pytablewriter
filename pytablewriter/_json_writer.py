# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
try:
    import json
except ImportError:   # pragma: no cover
    import simplejson as json
import re

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

        self.__none_value = "null"
        self.__re_replace_null = re.compile('["]null["]', re.MULTILINE)

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
        json_text = self.__re_replace_null.sub(
            self.__none_value, json_text)

        self.stream.write(json_text)

    def _preprocess_value_matrix(self):
        if self._preprocessed_value_matrix:
            return

        value_matrix = [
            [
                dataproperty.convert_value(value, self.__none_value)
                for value in value_list
            ]
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
