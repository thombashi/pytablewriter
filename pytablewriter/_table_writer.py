# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import sys

import dataproperty
from dataproperty import Typecode
from six.moves import zip

from ._error import NotSupportedError
from ._error import EmptyValueError
from ._error import EmptyTableDataError
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

    .. py:attribute:: is_write_header

        Write a header of the table if the value is |True|.

    .. py:attribute:: is_padding

        Padding an item in the table if the value is |True|.

    .. py:attribute:: is_quote_header

        Add double quote to string in the header if the value is |True|.

    .. py:attribute:: is_quote_table

        Dictionary of { Typecode : bool } format.
        Add double quote to string in table elements,
        where a |Typecode| of table-value is |True| in the dictionary.

    .. py:attribute:: iteration_length

        The number of iterations to write a table.
        This value used in :py:meth:`.write_table_iter` method.
        (defaults to ``-1`` which means number of iterations is indefinite)

    .. py:attribute:: write_callback

        This is called when for each of the iteration of writing a table is
        completed. This method is used in :py:meth:`.write_table_iter` method.
        (defaults to |None|)
        Example of a call back function definition is as follows:

        .. code:: python

            def callback_example(iter_count, iter_length):
                print("{:d}/{:d}".format(iter_count, iter_length))

        Arguments that passed to the callback is:

        - first argument: current iteration number (start from 1)
        - second argument: total number of iteration
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

        self.is_write_header = True
        self.is_padding = True
        self.is_quote_header = True
        self.is_quote_table = {
            Typecode.NONE: False,
            Typecode.INTEGER: False,
            Typecode.FLOAT: False,
            Typecode.STRING: True,
            Typecode.DATETIME: True,
            Typecode.FLOAT: False,
            Typecode.NAN: False,
            Typecode.BOOL: False,
        }

        self.is_write_header_separator_row = True
        self.is_write_value_separator_row = False
        self.is_write_opening_row = False
        self.is_write_closing_row = False
        self.is_float_formatting = True

        self._value_matrix = []
        self._column_prop_list = []
        self._value_prop_matrix = []

        self._prop_extractor = dataproperty.PropertyExtractor()
        self._prop_extractor.min_padding_len = 1
        self._prop_extractor.none_value = ""
        self._prop_extractor.datetime_format_str = "%Y-%m-%d %H:%M:%S%z"
        self._prop_extractor.bool_converter = default_bool_converter

        self._preprocessed_property = False

        self.iteration_length = -1
        self.write_callback = None

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

    def set_table_data(self, tabledata):
        """
        Set table data to fllowing attributes from
        :py:class:`pytablereader.TableData`

        - :py:attr:`~.table_name`.
        - :py:attr:`~.header_list`.
        - :py:attr:`~.value_matrix`.

        :param pytablereader.TableData tabledata: Input data.
        """

        self.table_name = tabledata.table_name
        self.header_list = tabledata.header_list
        self.value_matrix = tabledata.record_list

    def write_table_iter(self):
        """
        Write a table with iteration.
        "Iteration" means that divide the table writing into multiple process.
        This method is useful especially for large data.
        The following is premise to execute this method:

        - set iterator to the |value_matrix|
        - set the number of iterations to the |iteration_length| attribute

        Call back function (Optional):
        Callback function is called when for each of the iteration of writing
        a table is completed. To set call back function,
        set a callback function to the |write_callback| attribute.

        :raises pytablewriter.NotSupportedError:
            If the class does not support this method.

        .. note::

            Following classes do not support this method:
            |HtmlTableWriter|, |RstGridTableWriter|, |RstSimpleTableWriter|.
            ``support_split_write`` attribute will return |True| if the class
            is supported this method.
        """

        if not self.support_split_write:
            raise NotSupportedError()

        self._verify_table_name()
        self._verify_stream()

        if all([
            dataproperty.is_empty_sequence(self.header_list),
            dataproperty.is_empty_sequence(self.value_matrix),
        ]):
            raise EmptyTableDataError()

        self._verify_header()

        old_is_write_header = self.is_write_header
        old_is_write_opening_row = self.is_write_opening_row
        old_is_write_closing_row = self.is_write_closing_row

        self.is_write_closing_row = False
        iter_count = 1

        for work_matrix in self.value_matrix:
            is_final_iter = all([
                self.iteration_length > 0,
                iter_count >= self.iteration_length
            ])

            if is_final_iter:
                self.is_write_closing_row = True

            self.value_matrix = work_matrix
            self.write_table()

            if not is_final_iter:
                self._write_value_row_separator()

            self.is_write_opening_row = False
            self.is_write_header = False

            try:
                self.write_callback(iter_count, self.iteration_length)
            except TypeError:
                pass

            if is_final_iter:
                break

            iter_count += 1

        self.is_write_header = old_is_write_header
        self.is_write_opening_row = old_is_write_opening_row
        self.is_write_closing_row = old_is_write_closing_row

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
        to_string_format_str = self.__get_to_string_format(
            col_prop, value_prop)

        if col_prop.typecode in [Typecode.BOOL, Typecode.DATETIME]:
            item = to_string_format_str.format(value_prop.data)
        else:
            try:
                value = col_prop.type_factory.value_converter_factory.create(
                    value_prop.data).convert()
            except dataproperty.TypeConversionError:
                value = value_prop.data

            try:
                item = to_string_format_str.format(value)
            except ValueError:
                item = "{}".format(value)

        item = self.__get_align_format(col_prop).format(item)

        if all([
            self.is_quote_table.get(col_prop.typecode, False),
            any([
                self.is_quote_table.get(value_prop.typecode, False),
                value_prop.typecode in [Typecode.INTEGER, Typecode.FLOAT],
            ])
        ]):
            return u'"{:s}"'.format(item)

        return item

    def __get_to_string_format(self, col_prop, value_prop):
        if any([
            all([
                col_prop.typecode == Typecode.FLOAT,
                value_prop.typecode in [Typecode.INTEGER, Typecode.FLOAT],
                not self.is_float_formatting
            ]),
            value_prop.typecode == Typecode.NONE,
        ]):
            format_str = u""
        else:
            format_str = col_prop.format_str

        try:
            format_str.format(value_prop.data)
        except ValueError:
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

        if all([
            dataproperty.is_empty_sequence(self.header_list),
            dataproperty.is_empty_sequence(self.value_matrix),
        ]):
            raise EmptyTableDataError()

        self._verify_header()
        try:
            self._verify_value_matrix()
        except EmptyValueError:
            pass

    def _verify_table_name(self):
        pass

    def _verify_stream(self):
        if self.stream is None:
            raise IOError("null output stream")

    def _verify_header(self):
        pass

    def _verify_value_matrix(self):
        if dataproperty.is_empty_sequence(self.value_matrix):
            raise EmptyValueError()

        if dataproperty.is_empty_sequence(self.header_list):
            return

        dict_invalid = {}
        for row, value_list in enumerate(self.value_matrix):
            if len(self.header_list) != len(value_list):
                erroror_key = "row={:d}".format(row)
                dict_invalid[erroror_key] = (
                    "expected-col-len={:d}, actual={:d}".format(
                        len(value_list), len(self.header_list))
                )

        if len(dict_invalid) > 0:
            import os

            message = [
                "invalid table value: mismatch length with header and value",
                "  header: col-len={:d} {:s}".format(
                    len(self.header_list), self.header_list),
                "  value:  {:s}".format(str(dict_invalid)),
            ]
            raise ValueError(os.linesep.join(message))

    def _preprocess_property(self):
        if self._preprocessed_property:
            return

        self._value_matrix = []
        self._column_prop_list = []
        self._value_prop_matrix = []

        self._prop_extractor.header_list = self.header_list
        self._prop_extractor.data_matrix = self.__value_matrix_org
        self._column_prop_list = self._prop_extractor.extract_column_property_list()
        try:
            self._value_prop_matrix = self._prop_extractor.extract_data_property_matrix()
        except TypeError:
            self._value_prop_matrix = []

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
