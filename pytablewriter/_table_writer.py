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


def default_bool_converter(value):
    return str(value)


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
        self.is_float_formatting = True

        self._value_matrix = []
        self._column_prop_list = []
        self._value_prop_matrix = []

        self._prop_extractor = dataproperty.PropertyExtractor()
        self._prop_extractor.min_padding_len = 1
        self._prop_extractor.none_value = ""
        self._prop_extractor.datetime_format_str = "%Y-%m-%dT%H:%M:%S%z"
        self._prop_extractor.bool_converter = default_bool_converter

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
        return u"<"

    def _get_right_align_formatformat(self):
        return u">"

    def _get_center_align_formatformat(self):
        return u"^"

    def _get_row_item(self, col_prop, value_prop):
        from dataproperty import Typecode

        to_string_format_str = self.__get_to_string_format(
            col_prop, value_prop)

        if col_prop.typecode in [Typecode.BOOL, Typecode.DATETIME]:
            hoge = to_string_format_str.format(value_prop.data)
        else:
            try:
                value = col_prop.type_factory.value_converter_factory.create(
                    value_prop.data).convert()
            except dataproperty.TypeConversionError:
                value = value_prop.data

            try:
                hoge = to_string_format_str.format(value)
            except ValueError:
                hoge = "{}".format(value)

        item = self.__get_align_format(col_prop).format(hoge)

        if self.is_quote_str and any([
            all([
                col_prop.typecode == Typecode.STRING,
                value_prop.typecode not in [
                    Typecode.NONE, Typecode.BOOL, Typecode.INFINITY, Typecode.NAN]
            ]),
        ]):
            return u'"%s"' % (item)

        return item

    def __get_to_string_format(self, col_prop, value_prop):
        if any([
            not self.is_float_formatting,
            value_prop.typecode == dataproperty.Typecode.NONE,
        ]):
            format_str = u""
        else:
            format_str = col_prop.format_str

        try:
            format_str.format(value_prop.data)
        except dataproperty.TypeConversionError:
            format_str = u""

        return u"{:" + format_str + u"}"

    def __get_align_format(self, col_prop):
        align_func_table = {
            dataproperty.Align.AUTO: self._get_left_align_formatformat,
            dataproperty.Align.LEFT: self._get_left_align_formatformat,
            dataproperty.Align.RIGHT: self._get_right_align_formatformat,
            dataproperty.Align.CENTER: self._get_center_align_formatformat,
        }

        align = align_func_table[col_prop.align]()

        format_list = [u"{:" + align]
        if self._get_padding_len(col_prop) > 0:
            format_list.append(str(self._get_padding_len(col_prop)))
        format_list.append(u"s}")

        return u"".join(format_list)

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
                self._get_row_item(col_prop, value_prop)
                for col_prop, value_prop in
                zip(self._column_prop_list, value_prop_list)
            ]
            for value_prop_list in self._value_prop_matrix
        ]

        self._preprocessed_value_matrix = True

    def _preprocess(self):
        self._preprocess_property()
        self._preprocess_value_matrix()
