# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals
import re
import sys

import dataproperty as dp
from dataproperty import Typecode
from mbstrdecoder import MultiByteStrDecoder
import pytablereader as ptr
from six.moves import zip

from .._error import (
    NotSupportedError,
    EmptyValueError,
    EmptyTableNameError,
    EmptyHeaderError,
    EmptyTableDataError
)
from ._interface import TableWriterInterface


def default_bool_converter(value):
    return str(value)


class AbstractTableWriter(TableWriterInterface):
    """
    Base abstract class of table writer classes.

    .. py:attribute:: stream

        Stream to write tables.
        You can use arbitrary stream which supported ``write`` method
        such as ``sys.stdout``, file stream, ``StringIO``, etc.
        Defaults to ``sys.stdout``.

    .. py:attribute:: table_name

        Name of the table.

    .. py:attribute:: header_list

        List of table header to write.

    .. py:attribute:: value_matrix

        Table data (nested list) to write.

    .. py:attribute:: is_write_header

        Write headers of the table if the value is |True|.

    .. py:attribute:: is_padding

        Padding for each item in the table if the value is |True|.

    .. py:attribute:: is_quote_header

        Add double quote to the headers if the value is |True|.

    .. py:attribute:: quote_flag_table

        Add double quote to strings in table elements,
        where |Typecode| of table-value is |True| in the ``quote_flag_table``
        mapping table. ``quote_flag_table`` should be a dictionary.
        And is ``{ Typecode : bool }``. Defaults to 

        .. code-block:: json
            :caption: quote_flag_table default value

            {
                Typecode.NONE: False,
                Typecode.INTEGER: False,
                Typecode.FLOAT: False,
                Typecode.STRING: True,
                Typecode.DATETIME: True,
                Typecode.FLOAT: False,
                Typecode.NAN: False,
                Typecode.BOOL: False,
            }

    .. py:attribute:: iteration_length

        The number of iterations to write a table.
        This value used in :py:meth:`.write_table_iter` method.
        (defaults to ``-1`` which means number of iterations is indefinite)

    .. py:attribute:: write_callback

        The value expected to a function.
        The function called when for each of the iteration of writing a table
        completed. (defaults to |None|)
        Example callback function definition is as follows:

        .. code:: python

            def callback_example(iter_count, iter_length):
                print("{:d}/{:d}".format(iter_count, iter_length))

        Arguments that passed to the callback is:

        - first argument: current iteration number (start from 1)
        - second argument: total number of iteration
    """

    __RE_LINE_BREAK = re.compile("[\s\0\t\r\n]+")

    @property
    def value_matrix(self):
        return self.__value_matrix_org

    @value_matrix.setter
    def value_matrix(self, value_matrix):
        self.__value_matrix_org = value_matrix
        self._preprocessed_property = False
        self._preprocessed_value_matrix = False

    @property
    def tabledata(self):
        return ptr.TableData(
            self.table_name, self.header_list, self.value_matrix)

    def __init__(self):
        self.stream = sys.stdout
        self.table_name = None
        self.header_list = None
        self.value_matrix = None

        self.is_write_header = True
        self.is_padding = True
        self.is_quote_header = True
        self.quote_flag_table = {
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

        self._prop_extractor = dp.PropertyExtractor()
        self._prop_extractor.min_padding_len = 1
        self._prop_extractor.none_value = ""
        self._prop_extractor.datetime_format_str = "%Y-%m-%d %H:%M:%S%z"
        self._prop_extractor.bool_converter = default_bool_converter

        self._is_required_table_name = False
        self._is_remove_line_break = False
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

    def from_tabledata(self, tabledata):
        """
        Set tabular attributes to the writer from
        :py:class:`pytablereader.TableData`. Following attributes will be set:

        - :py:attr:`~.table_name`.
        - :py:attr:`~.header_list`.
        - :py:attr:`~.value_matrix`.

        :py:class:`pytablereader.TableData` can be create from various data
        formats, for more detailed information can be found in
        http://pytablereader.readthedocs.io/en/latest/

        :param pytablereader.TableData tabledata: Input table data.
        """

        self.table_name = tabledata.table_name
        self.header_list = tabledata.header_list
        self.value_matrix = tabledata.value_matrix

    def from_csv(self, csv_source):
        """
        Set tabular attributes to the writer from
        from CSV data source. Following attributes will be set:

        - :py:attr:`~.header_list`.
        - :py:attr:`~.value_matrix`.

        :py:attr:`~.table_name` will be also setting if the CSV data source
        is a file. In that case, :py:attr:`~.table_name` is as same as
        the filename.

        :param str csv_source:
            Input CSV data source, either can be designated CSV text or
            CSV file path.

        :Examples:

            :ref:`example-from-csv`
        """

        loader = ptr.CsvTableTextLoader(csv_source)
        try:
            for tabledata in loader.load():
                self.from_tabledata(tabledata)
            return
        except ptr.error.InvalidDataError:
            pass

        loader = ptr.CsvTableFileLoader(csv_source)
        for tabledata in loader.load():
            self.from_tabledata(tabledata)

    def from_dataframe(self, dataframe):
        """
        Set tabular attributes to the writer from
        from :py:class:`pandas.DataFrame`. Following attributes will be set:

        - :py:attr:`~.header_list`.
        - :py:attr:`~.value_matrix`.

        :param pandas.DataFrame dataframe: Input dataframe.

        :Examples:

            :ref:`example-from-pandas-dataframe`
        """

        self.header_list = list(dataframe.columns.values)
        self.value_matrix = dataframe.values.tolist()

    def set_dataframe(self, dataframe):
        # This method will be deleted in the future. Use from_tabledata
        # instead.

        self.from_dataframe(dataframe)

    def set_table_data(self, tabledata):
        # This method will be deleted in the future. Use from_tabledata
        # instead.

        self.from_tabledata(tabledata)

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
            dp.is_empty_sequence(self.header_list),
            dp.is_empty_sequence(self.value_matrix),
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

    def _get_padding_len(self, column_property, value_prop=None):
        if self.is_padding:
            try:
                return value_prop.get_padding_len(column_property.ascii_char_width)
            except AttributeError:
                return column_property.ascii_char_width

        return 0

    def _get_left_align_formatformat(self):
        return "<"

    def _get_right_align_formatformat(self):
        return ">"

    def _get_center_align_formatformat(self):
        return "^"

    def _get_row_item(self, col_prop, value_prop):
        to_string_format_str = self.__get_to_string_format(
            col_prop, value_prop)

        if col_prop.typecode in [Typecode.BOOL, Typecode.DATETIME]:
            item = to_string_format_str.format(value_prop.data)
        else:
            try:
                value = col_prop.type_class(
                    value_prop.data, is_strict=False).convert()
            except dp.TypeConversionError:
                value = value_prop.data

            try:
                item = to_string_format_str.format(value)
            except ValueError:
                item = MultiByteStrDecoder(value).unicode_str

        item = self.__remove_line_break(item)
        item = self.__get_align_format(col_prop, value_prop).format(item)

        if all([
            self.quote_flag_table.get(col_prop.typecode, False),
            any([
                self.quote_flag_table.get(value_prop.typecode, False),
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
            format_str = ""
        else:
            format_str = col_prop.format_str

        try:
            format_str.format(value_prop.data)
        except ValueError:
            format_str = ""

        return "{:" + format_str + "}"

    def __get_align_format(self, col_prop, value_prop):
        align_func_table = {
            dp.Align.AUTO: self._get_left_align_formatformat,
            dp.Align.LEFT: self._get_left_align_formatformat,
            dp.Align.RIGHT: self._get_right_align_formatformat,
            dp.Align.CENTER: self._get_center_align_formatformat,
        }

        align = align_func_table[col_prop.align]()

        format_list = ["{:" + align]
        col_padding_len = self._get_padding_len(col_prop, value_prop)
        if col_padding_len > 0:
            format_list.append(str(col_padding_len))
        format_list.append("s}")

        return "".join(format_list)

    def _verify_property(self):
        self._verify_table_name()
        self._verify_stream()

        if all([
            dp.is_empty_sequence(self.header_list),
            dp.is_empty_sequence(self.value_matrix),
        ]):
            raise EmptyTableDataError()

        self._verify_header()
        try:
            self._verify_value_matrix()
        except EmptyValueError:
            pass

    def _verify_table_name(self):
        if all([
                self._is_required_table_name,
                dp.is_empty_string(self.table_name),
        ]):
            raise EmptyTableNameError(
                "table_name must be string, with at least one character or more length.")

    def _verify_stream(self):
        if self.stream is None:
            raise IOError("null output stream")

    def _verify_header(self):
        pass

    def _validate_empty_header(self):
        """
        :raises pytablewriter.EmptyHeaderError: If the |header_list| is empty.
        """

        if dp.is_empty_sequence(self.header_list):
            raise EmptyHeaderError(
                "header_list expected to have one ore more header names")

    def _verify_value_matrix(self):
        if dp.is_empty_sequence(self.value_matrix):
            raise EmptyValueError()

        if dp.is_empty_sequence(self.header_list):
            return

    def _preprocess_property(self):
        if self._preprocessed_property:
            return

        self._value_matrix = []
        self._column_prop_list = []
        self._value_prop_matrix = []

        self._prop_extractor.header_list = self.header_list
        self._prop_extractor.data_matrix = self.__value_matrix_org
        self._column_prop_list = self._prop_extractor.extract_col_property_list()
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

    def __remove_line_break(self, text):
        if not self._is_remove_line_break:
            return text

        return self.__RE_LINE_BREAK.sub(" ", text)
