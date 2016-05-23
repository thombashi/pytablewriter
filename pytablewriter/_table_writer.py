# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import sys

import dataproperty

from ._error import EmptyHeaderError
from ._error import EmptyValueError
from ._interface import TableWriterInterface


class TableWriter(TableWriterInterface):
    """
    Abstract class of table writer.

    .. py:attribute:: stream

        Stream to write the table.

    .. py:attribute:: table_name

        Table name of the table.

    .. py:attribute:: header_list

        List of header data to write.

    .. py:attribute:: value_matrix

        Nested list of data to write.

    .. py:attribute:: is_padding

        Padding an item in the table if the value is |True|.

    .. py:attribute:: is_quote_str

        Add double quote to string in the table if the value is |True|.
    """

    @property
    def value_matrix(self):
        return self.__value_matrix_org

    @value_matrix.setter
    def value_matrix(self, value_matrix):
        self.__value_matrix_org = value_matrix
        self._preprocessed_property = False
        self._preprocessed_value_matrix = False

    def __init__(self):
        self.stream = sys.stdout
        self.table_name = None
        self.header_list = None
        self.value_matrix = None

        self.is_padding = True
        self.is_quote_str = True

        self._value_matrix = []
        self._column_prop_list = []
        self._value_prop_matrix = []

        self._prop_extractor = dataproperty.PropertyExtractor()
        self._prop_extractor.min_padding_len = 1

        self._preprocessed_property = False

    def close(self):
        """
        Close the current |stream|.
        """

        try:
            if self.stream.name in ["<stdin>", "<stdout>", "<stderr>"]:
                return
        except AttributeError:
            pass

        try:
            self.stream.close()
        except AttributeError:
            pass
        finally:
            self.stream = None

    def _get_padding_len(self, column_property):
        if self.is_padding:
            return column_property.padding_len

        return 0

    def _get_left_align_formatformat(self):
        return u"%s"

    def _get_right_align_formatformat(self):
        return u"%s"

    def _get_center_align_formatformat(self):
        return u"%s"

    def _get_row_item(self, col_prop, value_prop, is_header):
        item = self.__get_format(
            col_prop, value_prop, is_header) % (value_prop.data)

        if self.is_quote_str and any([
            col_prop.typecode == dataproperty.Typecode.STRING,
            is_header
        ]):
            return u'"%s"' % (item.strip())

        return item

    def __get_format(self, col_prop, value_prop, is_header=False):
        align_func_table = {
            dataproperty.Align.AUTO: self._get_left_align_formatformat,
            dataproperty.Align.LEFT: self._get_left_align_formatformat,
            dataproperty.Align.RIGHT: self._get_right_align_formatformat,
            dataproperty.Align.CENTER: self._get_center_align_formatformat,
        }

        padding_space_len = 0
        if self.is_padding:
            if any([is_header, col_prop.align == dataproperty.Align.CENTER]):
                padding_space_len = int(
                    (col_prop.padding_len - value_prop.str_len) / 2)

        if any([is_header, value_prop.typecode == dataproperty.Typecode.NONE]):
            format_str = u"s"
        else:
            format_str = col_prop.format_str

        if is_header:
            formatformat = align_func_table[dataproperty.Align.CENTER]()
        else:
            formatformat = align_func_table[col_prop.align]()

        return (
            u" " * padding_space_len +
            formatformat % (
                self._get_padding_len(col_prop) - padding_space_len,
                format_str)
        )

    def _verify_property(self):
        self._verify_table_name()
        self._verify_stream()
        self._verify_header()
        self._verify_value_matrix()

    def _verify_table_name(self):
        pass

    def _verify_stream(self):
        if self.stream is None:
            raise IOError("null output stream")

    def _verify_header(self):
        if dataproperty.is_empty_list_or_tuple(self.header_list):
            raise EmptyHeaderError()

    def _verify_value_matrix(self):
        if dataproperty.is_empty_list_or_tuple(self.value_matrix):
            raise EmptyValueError()

        if dataproperty.is_empty_list_or_tuple(self.header_list):
            return

        for row, value_list in enumerate(self.value_matrix):
            dict_invalid = {}

            if len(self.header_list) != len(value_list):
                erroror_key = "row=%d" % (row)
                dict_invalid[erroror_key] = (
                    "expected-col-size=%d, actual= %s" % (
                        len(value_list), len(self.header_list))
                )

        if len(dict_invalid) > 0:
            import os

            message = [
                "_verify_value_matrix: miss match length with header and value",
                "  header: col-size=%d %s" % (
                    len(self.header_list), self.header_list),
                "  value:  %s" % (str(dict_invalid)),
            ]
            raise ValueError(os.linesep.join(message))

    def _preprocess_property(self):
        if self._preprocessed_property:
            return

        self._value_matrix = []
        self._column_prop_list = []
        self._value_prop_matrix = []

        if dataproperty.is_empty_list_or_tuple(self.value_matrix):
            return

        self._prop_extractor.header_list = self.header_list
        self._prop_extractor.data_matrix = self.__value_matrix_org
        self._column_prop_list = self._prop_extractor.extract_column_property_list()
        self._value_prop_matrix = self._prop_extractor.extract_data_property_matrix()

        self._preprocessed_property = True

    def _preprocess_value_matrix(self):
        if self._preprocessed_value_matrix:
            return

        self._value_matrix = [
            [
                self._get_row_item(col_prop, value_prop, is_header=False)
                for col_prop, value_prop in
                zip(self._column_prop_list, value_prop_list)
            ]
            for value_prop_list in self._value_prop_matrix
        ]

        self._preprocessed_value_matrix = True

    def _preprocess(self):
        self._preprocess_property()
        self._preprocess_value_matrix()
