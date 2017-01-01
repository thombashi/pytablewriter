# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals
import abc

import dataproperty as dp
from dataproperty import IntegerType
from six.moves import range
import xlwt

from .._converter import str_datetime_converter
from ._excel_workbook import (
    ExcelWorkbookXls,
    ExcelWorkbookXlsx
)
from ._interface import TextWriterInterface
from ._table_writer import AbstractTableWriter


class ExcelTableWriter(AbstractTableWriter, TextWriterInterface):
    """
    Abstract class of a table writer for Excel file format.
    """

    @property
    def support_split_write(self):
        return True

    @property
    def workbook(self):
        return self._workbook

    @property
    def first_header_row(self):
        """
        :return: Index of the first row of the header.
        :rtype: int

        .. note:: |excel_attr|
        """

        return self._first_header_row

    @property
    def last_header_row(self):
        """
        :return: Index of the last row of the header.
        :rtype: int

        .. note:: |excel_attr|
        """

        return self._last_header_row

    @property
    def first_data_row(self):
        """
        :return: Index of the first row of the data (table body).
        :rtype: int

        .. note:: |excel_attr|
        """

        return self._first_data_row

    @property
    def last_data_row(self):
        """
        :return: Index of the last row of the data (table body).
        :rtype: int

        .. note:: |excel_attr|
        """

        return self._last_data_row

    @property
    def first_data_col(self):
        """
        :return: Index of the first column of the table.
        :rtype: int

        .. note:: |excel_attr|
        """

        return self._first_data_col

    @property
    def last_data_col(self):
        """
        :return: Index of the last column of the table.
        :rtype: int

        .. note:: |excel_attr|
        """

        return self._last_data_col

    def __init__(self):
        super(ExcelTableWriter, self).__init__()

        self.stream = None
        self._workbook = None

        self._dp_extractor.inf_value = "Inf"
        self._dp_extractor.nan_value = "NaN"
        self._dp_extractor.datetime_converter = str_datetime_converter
        self._dp_extractor.datetime_format_str = "s"

        self._first_header_row = 0
        self._last_header_row = self.first_header_row
        self._first_data_row = self.last_header_row + 1
        self._first_data_col = 0
        self._last_data_row = None
        self._last_data_col = None

        self._current_data_row = self._first_data_row

    @abc.abstractproperty
    def open_workbook(self, workbook_path):
        """
        Open workbook.

        :param str workbook_path: File path to open.
        """

    def close(self):
        """
        Close the current workbook.
        """

        if self.workbook is not None:
            self.workbook.close()
            self._workbook = None

    def from_tabledata(self, tabledata):
        """
        Set following attributes from :py:class:`pytablereader.TableData`

        - :py:attr:`~.table_name`.
        - :py:attr:`~.header_list`.
        - :py:attr:`~.value_matrix`.

        And create worksheet named from :py:attr:`~.table_name` ABC
        if not existed yet.

        :param pytablereader.TableData tabledata: Input table data.
        """

        super(ExcelTableWriter, self).from_tabledata(tabledata)

        self.make_worksheet(self.table_name)

    def set_table_data(self, tabledata):
        # This method will be deleted in the future. Use from_tabledata
        # instead.

        self.from_tabledata(tabledata)

    def make_worksheet(self, sheet_name):
        """
        Make a worksheet to the current workbook.

        :param str sheet_name:
            Name of the worksheet to create. Name of the work sheet will
            automatically decided (like ``"Sheet1"``)
            if the ``sheet_name`` is empty.
        """

        if sheet_name is None:
            sheet_name = ""
        self.stream = self.workbook.add_worksheet(sheet_name)
        self._current_data_row = self._first_data_row

    def write_null_line(self):
        pass

    def write_table(self):
        """
        Write a table to the current worksheet.

        :raises IOError: If failed to write data to the worksheet.

        .. note::

            - |None| values will be written as an empty string.
            - |inf| values will be written as `Inf`
            - |nan| values will be written as ``NaN``
        """

        self._verify_property()
        self._preprocess_property()

        self._write_header()
        self._write_value_matrix()

        self._postprocess()

    def _write_value_row_separator(self):
        pass

    def _write_value_matrix(self):
        for value_dp_list in self._value_dp_matrix:
            for col_idx, value_dp in enumerate(value_dp_list):
                self._write_cell(self._current_data_row, col_idx, value_dp)

            self._current_data_row += 1

    def _get_last_column(self):
        if dp.is_not_empty_sequence(self.header_list):
            return len(self.header_list) - 1

        if dp.is_not_empty_sequence(self.value_matrix):
            return len(self.value_matrix[0]) - 1

        raise ValueError()

    def _postprocess(self):
        self._last_data_row = self._current_data_row
        self._last_data_col = self._get_last_column()


class ExcelXlsTableWriter(ExcelTableWriter):
    """
    A table writer class for Excel file format: ``.xls``
    (older or equal to Office 2003).
    """

    def __init__(self):
        super(ExcelXlsTableWriter, self).__init__()

        self.__col_style_table = {}

    def open_workbook(self, workbook_path):
        self._workbook = ExcelWorkbookXls(workbook_path)

    def _write_header(self):
        if any([
            not self.is_write_header,
            dp.is_empty_sequence(self.header_list),
        ]):
            return

        for col, value in enumerate(self.header_list):
            self.stream.write(self.first_header_row, col, value)

    def _write_cell(self, row, col, value_dp):
        if value_dp.typecode in [dp.Typecode.FLOAT]:
            try:
                cell_style = self.__get_cell_style(col)
            except ValueError:
                pass
            else:
                self.stream.write(
                    row, col, value_dp.data, cell_style)
                return

        self.stream.write(row, col, value_dp.data)

    def _postprocess(self):
        super(ExcelXlsTableWriter, self)._postprocess()

        self.__col_style_table = {}

    def __get_cell_style(self, col):
        if col in self.__col_style_table:
            return self.__col_style_table.get(col)

        try:
            col_dp = self._column_dp_list[col]
        except KeyError:
            return {}

        if col_dp.typecode not in [dp.Typecode.FLOAT]:
            raise ValueError()

        if not IntegerType(col_dp.minmax_decimal_places.max_value).is_type():
            raise ValueError()

        float_digit = col_dp.minmax_decimal_places.max_value
        if float_digit <= 0:
            raise ValueError()

        num_format_str = "#,{:s}0.{:s}".format(
            "#" * int(float_digit), "0" * int(float_digit))
        cell_style = xlwt.easyxf(num_format_str=num_format_str)
        self.__col_style_table[col] = cell_style

        return cell_style


class ExcelXlsxTableWriter(ExcelTableWriter):
    """
    A table writer class for Excel file format: ``.xlsx``
    (newer or equal to Office 2007).

    :Examples:

        :ref:`example-excel-table-writer`
    """

    MAX_CELL_WIDTH = 60

    class FormatName(object):
        HEADER = "header"
        CELL = "cell"
        NAN = "nan"

    class Default(object):
        FONT_NAME = "MS Gothic"
        FONT_SIZE = 9

        CELL_FORMAT = {
            "font_name": FONT_NAME,
            "font_size": FONT_SIZE,
            "align": "top",
            "text_wrap": True,
            "top": 1,
            "left": 1,
            "bottom": 1,
            "right": 1,
        }
        HEADER_FORMAT = {
            "font_name": FONT_NAME,
            "font_size": FONT_SIZE,
            "bg_color": "#DFDFFF",
            "bold": True,
            "left": 1,
            "right": 1,
        }
        NAN_FORMAT = {
            "font_name": FONT_NAME,
            "font_size": FONT_SIZE,
            "font_color": "silver",
            "top": 1,
            "left": 1,
            "bottom": 1,
            "right": 1,
        }

    @property
    def __nan_format_property(self):
        return self.format_table.get(self.FormatName.NAN, self.default_format)

    @property
    def __cell_format_property(self):
        return self.format_table.get(self.FormatName.CELL, self.default_format)

    def __init__(self):
        super(ExcelXlsxTableWriter, self).__init__()

        self.default_format = self.Default.CELL_FORMAT
        self.format_table = {
            self.FormatName.CELL: self.Default.CELL_FORMAT,
            self.FormatName.HEADER: self.Default.HEADER_FORMAT,
            self.FormatName.NAN: self.Default.NAN_FORMAT,
        }

        self.__col_cell_format_cache = {}
        self.__col_numprops_table = {}

    def open_workbook(self, workbook_path):
        self._workbook = ExcelWorkbookXlsx(workbook_path)

    def _write_header(self):
        if any([
            not self.is_write_header,
            dp.is_empty_sequence(self.header_list),
        ]):
            return

        header_format_props = self.format_table.get(
            self.FormatName.HEADER, self.default_format)
        header_format = self.__add_format(header_format_props)

        self.stream.write_row(
            row=self.first_header_row, col=0,
            data=self.header_list, cell_format=header_format)
        for row in range(self.first_header_row, self.last_header_row):
            self.stream.write_row(
                row=row, col=0, data=[""] * len(self.header_list),
                cell_format=header_format)

    def _write_cell(self, row, col, value_dp):
        base_props = dict(self.__cell_format_property)
        format_key = "{:d}_{:d}".format(col, value_dp.typecode)

        if value_dp.typecode in [dp.Typecode.INTEGER, dp.Typecode.FLOAT]:
            num_props = self.__get_number_property(col)
            base_props.update(num_props)
            cell_format = self.__get_cell_format(format_key, base_props)

            try:
                self.stream.write_number(
                    row, col, float(value_dp.data), cell_format)
                return
            except TypeError:
                pass

        if value_dp.typecode is dp.Typecode.NAN:
            base_props = dict(self.__nan_format_property)

        cell_format = self.__get_cell_format(format_key, base_props)
        self.stream.write(
            row, col, value_dp.data, cell_format)

    def __get_number_property(self, col):
        if col in self.__col_numprops_table:
            return self.__col_numprops_table.get(col)

        try:
            col_dp = self._column_dp_list[col]
        except KeyError:
            return {}

        if col_dp.typecode not in [dp.Typecode.INTEGER, dp.Typecode.FLOAT]:
            return {}

        num_props = {}
        if IntegerType(col_dp.minmax_decimal_places.max_value).is_type():
            float_digit = col_dp.minmax_decimal_places.max_value
            if float_digit > 0:
                num_props = {
                    "num_format": "0.{:s}".format("0" * int(float_digit))}

        self.__col_numprops_table[col] = num_props

        return num_props

    def __get_cell_format(self, format_key, cell_props):
        cell_format = self.__col_cell_format_cache.get(format_key)
        if cell_format is not None:
            return cell_format

        # cache miss
        cell_format = self.__add_format(cell_props)
        self.__col_cell_format_cache[format_key] = cell_format

        return cell_format

    def __add_format(self, dict_property):
        return self.workbook.workbook.add_format(dict_property)

    def __set_cell_width(self):
        font_size = self.__cell_format_property.get("font_size")

        if not IntegerType(font_size).is_type():
            return

        for col_idx, col_dp in enumerate(self._column_dp_list):
            width = (
                min(col_dp.ascii_char_width, self.MAX_CELL_WIDTH) *
                (font_size / 10.0) + 2
            )
            self.stream.set_column(col_idx, col_idx, width=width)

    def _preprocess_property(self):
        super(ExcelXlsxTableWriter, self)._preprocess_property()

        self.__set_cell_width()

    def _postprocess(self):
        super(ExcelXlsxTableWriter, self)._postprocess()

        self.stream.autofilter(
            self.last_header_row, self.first_data_col,
            self.last_data_row, self.last_data_col)
        self.stream.freeze_panes(self.first_data_row, self.first_data_col)

        self.__col_cell_format_cache = {}
        self.__col_numprops_table = {}
