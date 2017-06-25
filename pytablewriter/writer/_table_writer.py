# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import abc
import re
import sys

from mbstrdecoder import MultiByteStrDecoder
from typepy import Typecode
import typepy

import pytablereader as ptr
from six.moves import zip

from .._error import (
    NotSupportedError,
    EmptyValueError,
    EmptyTableNameError,
    EmptyHeaderError,
    EmptyTableDataError
)
from .._logger import (
    logger,
    WriterLogger,
)
from ._interface import TableWriterInterface


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

    .. py:attribute:: type_hint_list

        A list of type hints for each columns of data.
        Acceptable values are as follows:

            - |None| (automatically detect column type from values in the column)
            - :py:class:`pytablewriter.Bool`
            - :py:class:`pytablewriter.DateTime`
            - :py:class:`pytablewriter.Dictionary`
            - :py:class:`pytablewriter.Infinity`
            - :py:class:`pytablewriter.Integer`
            - :py:class:`pytablewriter.List`
            - :py:class:`pytablewriter.Nan`
            - :py:class:`pytablewriter.NoneType`
            - :py:class:`pytablewriter.NullString`
            - :py:class:`pytablewriter.RealNumber`
            - :py:class:`pytablewriter.String`

        A writer will convert data for each column using type-hint
        information before writing tables when you call ``write_xxx`` methods.
        If a type-hint value is not |None|, the writer will try to
        convert data for each data in a column to type-hint class.
        If the type-hint value is |None| or failed to convert data,
        the writer will automatically detect column data type from
        the column data.

        If ``type_hint_list`` is |None|, the writer will detect
        column data types for  all of the columns automatically and write a
        table.
        Defaults to |None|.

        :Examples:

            :ref:`example-type-hint-js`

    .. py:attribute:: is_write_header

        Write headers of the table if the value is |True|.

    .. py:attribute:: is_padding

        Padding for each item in the table if the value is |True|.

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
        self.__set_value_matrix(value_matrix)
        self.__clear_preprocessed_data()

    @property
    def tabledata(self):
        return ptr.TableData(
            self.table_name, self.header_list, self.value_matrix)

    @property
    def type_hint_list(self):
        return self._dp_extractor.col_type_hint_list

    @type_hint_list.setter
    def type_hint_list(self, value):
        self.__set_type_hint_list(value)
        self.__clear_preprocessed_data()

    @property
    def _quote_flag_mapping(self):
        return self._dp_extractor.quote_flag_mapping

    @_quote_flag_mapping.setter
    def _quote_flag_mapping(self, value):
        self._dp_extractor.quote_flag_mapping = value
        self.__clear_preprocessed_data()

    @abc.abstractmethod
    def _write_table(self):
        pass

    def __init__(self):
        from dataproperty import (
            Align,
            DataPropertyExtractor,
        )

        self.stream = sys.stdout
        self.table_name = None
        self.header_list = None
        self.value_matrix = None

        self.is_write_header = True
        self.is_padding = True

        self.is_write_header_separator_row = True
        self.is_write_value_separator_row = False
        self.is_write_opening_row = False
        self.is_write_closing_row = False

        self.is_float_formatting = True

        self._value_matrix = []
        self._column_dp_list = []
        self._value_dp_matrix = []

        self._logger = WriterLogger(self)

        self._dp_extractor = DataPropertyExtractor()
        self._dp_extractor.min_column_width = 1
        self._dp_extractor.strip_str_header = '"'
        self._dp_extractor.strip_str_value = '"'
        self._dp_extractor.type_value_mapping[Typecode.NONE] = ""

        self.type_hint_list = None
        self._quote_flag_mapping = {
            Typecode.BOOL: False,
            Typecode.DATETIME: True,
            Typecode.DICTIONARY: False,
            Typecode.INFINITY: False,
            Typecode.INTEGER: False,
            Typecode.IP_ADDRESS: True,
            Typecode.LIST: False,
            Typecode.NAN: False,
            Typecode.NONE: False,
            Typecode.NULL_STRING: True,
            Typecode.REAL_NUMBER: False,
            Typecode.STRING: True,
        }

        self._is_required_table_name = False
        self._is_remove_line_break = False
        self._is_complete_table_property_preprocess = False

        self.iteration_length = -1
        self.write_callback = None
        self.__iter_count = None

        self.__align_char_mapping = {
            Align.AUTO: "<",
            Align.LEFT: "<",
            Align.RIGHT: ">",
            Align.CENTER: "^",
        }

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
        self.type_hint_list = [
            self.__get_typehint_from_dtype(dtype)
            for dtype in dataframe.dtypes
        ]

    def write_table(self):
        """
        |write_table|.
        """

        self._logger.logging_start_write()
        self._write_table()
        self._logger.logging_complete_write()

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
            raise NotSupportedError(
                "the class not supported the write_table_iter method")

        self._verify_table_name()
        self._verify_stream()

        if all([
            typepy.is_empty_sequence(self.header_list),
            typepy.is_empty_sequence(self.value_matrix),
        ]):
            raise EmptyTableDataError()

        self._verify_header()

        old_is_write_header = self.is_write_header
        old_is_write_opening_row = self.is_write_opening_row
        old_is_write_closing_row = self.is_write_closing_row

        self.is_write_closing_row = False
        self.__iter_count = 1

        self._logger.logging_start_write([
            "iteration-length={:d}".format(self.iteration_length)
        ])

        for work_matrix in self.value_matrix:
            is_final_iter = all([
                self.iteration_length > 0,
                self.__iter_count >= self.iteration_length
            ])

            if is_final_iter:
                self.is_write_closing_row = True

            self.__set_value_matrix(work_matrix)
            self.__clear_preprocessed_flag()

            self._write_table()

            if not is_final_iter:
                self._write_value_row_separator()

            self.is_write_opening_row = False
            self.is_write_header = False

            try:
                self.write_callback(self.__iter_count, self.iteration_length)
            except TypeError:
                pass

            # update typehint for the next iteration
            """
            if self.type_hint_list is None:
                self.__set_type_hint_list([
                    column_dp.type_class for column_dp in self._column_dp_list
                ])
            """

            if is_final_iter:
                break

            self.__iter_count += 1

        self.is_write_header = old_is_write_header
        self.is_write_opening_row = old_is_write_opening_row
        self.is_write_closing_row = old_is_write_closing_row
        self.__iter_count = None

        self._logger.logging_complete_write()

    def _get_padding_len(self, column_dp, value_dp=None):
        if not self.is_padding:
            return 0

        try:
            return value_dp.get_padding_len(column_dp.ascii_char_width)
        except AttributeError:
            return column_dp.ascii_char_width

    def _get_row_item(self, col_dp, value_dp):
        to_string_format_str = self.__get_to_string_format(
            col_dp, value_dp)

        if col_dp.typecode in [Typecode.BOOL, Typecode.DATETIME]:
            item = to_string_format_str.format(value_dp.data)
        else:
            try:
                value = col_dp.type_class(
                    value_dp.data, strict_level=typepy.StrictLevel.MIN
                ).convert()
            except typepy.TypeConversionError:
                value = value_dp.data

            try:
                item = to_string_format_str.format(value)
            except ValueError:
                item = MultiByteStrDecoder(value).unicode_str

        return self.__get_align_format(col_dp, value_dp).format(
            self.__remove_line_break(item))

    def __get_to_string_format(self, col_dp, value_dp):
        if any([
            all([
                col_dp.typecode == Typecode.REAL_NUMBER,
                value_dp.typecode in [Typecode.INTEGER, Typecode.REAL_NUMBER],
                not self.is_float_formatting
            ]),
            value_dp.typecode == Typecode.NONE,
        ]):
            return "{}"

        try:
            col_dp.format_str.format(value_dp.data)
        except (TypeError, ValueError):
            return "{}"

        return col_dp.format_str

    def _get_align_char(self, align):
        return self.__align_char_mapping[align]

    def __get_align_format(self, col_dp, value_dp):
        format_list = ["{:" + self._get_align_char(col_dp.align)]
        col_padding_len = self._get_padding_len(col_dp, value_dp)
        if col_padding_len > 0:
            format_list.append(str(col_padding_len))
        format_list.append("s}")

        return "".join(format_list)

    def __get_typehint_from_dtype(self, col_dtype):
        col_dtype = str(col_dtype)

        if re.search("^float", col_dtype):
            return typepy.type.RealNumber

        if re.search("^int", col_dtype):
            return typepy.type.Integer

        return None

    def _verify_property(self):
        self._verify_table_name()
        self._verify_stream()

        if all([
            typepy.is_empty_sequence(self.header_list),
            typepy.is_empty_sequence(self.value_matrix),
        ]):
            raise EmptyTableDataError()

        self._verify_header()
        try:
            self._verify_value_matrix()
        except EmptyValueError:
            pass

    def __set_value_matrix(self, value_matrix):
        self.__value_matrix_org = value_matrix

    def __set_type_hint_list(self, type_hint_list):
        self._dp_extractor.col_type_hint_list = type_hint_list

    def _verify_table_name(self):
        if all([
                self._is_required_table_name,
                typepy.is_null_string(self.table_name),
        ]):
            raise EmptyTableNameError(
                "table_name must be a string, with at least one or "
                "more character.")

    def _verify_stream(self):
        if self.stream is None:
            raise IOError("null output stream")

    def _verify_header(self):
        pass

    def _validate_empty_header(self):
        """
        :raises pytablewriter.EmptyHeaderError: If the |header_list| is empty.
        """

        if typepy.is_empty_sequence(self.header_list):
            raise EmptyHeaderError(
                "header_list expected to have one ore more header names")

    def _verify_value_matrix(self):
        if typepy.is_empty_sequence(self.value_matrix):
            raise EmptyValueError()

        if typepy.is_empty_sequence(self.header_list):
            return

    def _preprocess_table_property(self):
        if self._is_complete_table_property_preprocess:
            return

        self._value_matrix = []

        self._dp_extractor.header_list = self.header_list
        self._dp_extractor.data_matrix = self.__value_matrix_org

        self._column_dp_list = self._dp_extractor.to_col_dataproperty_list(
            self._column_dp_list)
        self._header_dp_list = self._dp_extractor.to_header_dataproperty_list()

        if self.__iter_count == 1:
            import math

            for column_dp in self._column_dp_list:
                column_dp.extend_width(int(
                    math.ceil(column_dp.ascii_char_width * 0.25)))

        try:
            self._value_dp_matrix = self._dp_extractor.to_dataproperty_matrix()
        except TypeError:
            self._value_dp_matrix = []

        self._is_complete_table_property_preprocess = True

    def _preprocess_value_matrix(self):
        if self._is_complete_value_matrix_preprocess:
            return

        self._value_matrix = [
            [
                self._get_row_item(col_dp, value_dp)
                for col_dp, value_dp in
                zip(self._column_dp_list, value_dp_list)
            ]
            for value_dp_list in self._value_dp_matrix
        ]

        self._is_complete_value_matrix_preprocess = True

    def _preprocess(self):
        self._preprocess_table_property()
        self._preprocess_value_matrix()

    def __clear_preprocessed_flag(self):
        logger.debug("__clear_preprocessed_flag")

        self._is_complete_table_property_preprocess = False
        self._is_complete_value_matrix_preprocess = False

    def __clear_preprocessed_data(self):
        logger.debug("__clear_preprocessed_data")

        self.__clear_preprocessed_flag()
        self._column_dp_list = []

    def __remove_line_break(self, text):
        if not self._is_remove_line_break:
            return text

        return self.__RE_LINE_BREAK.sub(" ", text)
