# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import dataproperty
from six.moves import range
import xlsxwriter

from ._interface import TextWriterInterface
from ._table_writer import TableWriter


class ExcelWorkbook(object):

    @property
    def workbook(self):
        return self.__workbook

    @property
    def file_path(self):
        return self.__file_path

    def __init__(self, file_path):
        self.open(file_path)

    def __del__(self):
        self.close()

    def open(self, file_path):
        self.__file_path = file_path
        self.__workbook = xlsxwriter.Workbook(file_path)

    def close(self):
        if self.workbook is None:
            return

        self.__workbook.close()
        self.__clear()

    def __clear(self):
        self.__workbook = None
        self.__file_path = None


class ExcelTableWriter(TableWriter, TextWriterInterface):
    """
    Concrete class of a table writer for Excel format.

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
            "font_name" 	: FONT_NAME,
            "font_size" 	: FONT_SIZE,
            "align"			: "top",
            "text_wrap"		: True,
            "top"			: 1,
            "left"			: 1,
            "bottom"		: 1,
            "right"			: 1,
        }
        HEADER_FORMAT = {
            "font_name" 	: FONT_NAME,
            "font_size" 	: FONT_SIZE,
            "bg_color"		: "#DFDFFF",
            "bold"			: True,
            "left"			: 1,
            "right"			: 1,
        }
        NAN_FORMAT = {
            "font_name"		: FONT_NAME,
            "font_size"		: FONT_SIZE,
            "font_color"	: "silver",
            "top"			: 1,
            "left"			: 1,
            "bottom"		: 1,
            "right"			: 1,
        }

    @property
    def workbook(self):
        return self.__workbook

    @property
    def first_header_row(self):
        """
        :return: Index of the first row of the header.
        :rtype: int

        .. note:: |excel_attr|
        """

        return self.__first_header_row

    @property
    def last_header_row(self):
        """
        :return: Index of the last row of the header.
        :rtype: int

        .. note:: |excel_attr|
        """

        return self.__last_header_row

    @property
    def first_data_row(self):
        """
        :return: Index of the first row of the data (table body).
        :rtype: int

        .. note:: |excel_attr|
        """

        return self.__first_data_row

    @property
    def last_data_row(self):
        """
        :return: Index of the last row of the data (table body).
        :rtype: int

        .. note:: |excel_attr|
        """

        return self.__last_data_row

    @property
    def first_data_col(self):
        """
        :return: Index of the first column of the table.
        :rtype: int

        .. note:: |excel_attr|
        """

        return self.__first_data_col

    @property
    def last_data_col(self):
        """
        :return: Index of the last column of the table.
        :rtype: int

        .. note:: |excel_attr|
        """

        return self.__last_data_col

    @property
    def __nan_format_property(self):
        return self.format_table.get(self.FormatName.NAN, self.default_format)

    @property
    def __cell_format_property(self):
        return self.format_table.get(self.FormatName.CELL, self.default_format)

    def __init__(self):
        super(ExcelTableWriter, self).__init__()

        self.stream = None

        self.default_format = self.Default.CELL_FORMAT
        self.format_table = {
            self.FormatName.CELL	: self.Default.CELL_FORMAT,
            self.FormatName.HEADER	: self.Default.HEADER_FORMAT,
            self.FormatName.NAN		: self.Default.NAN_FORMAT,
        }

        self.__workbook = None
        self.__sheet_table = {}
        self.__col_cell_format_cache = {}

        self.__first_header_row = 0
        self.__last_header_row = self.first_header_row
        self.__first_data_row = self.last_header_row + 1
        self.__first_data_col = 0
        self.__last_data_row = None
        self.__last_data_col = None

    def open_workbook(self, workbook_path):
        """
        Open workbook.

        :param str workbook_path: File path to open.
        """

        self.__workbook = ExcelWorkbook(workbook_path)

    def close(self):
        """
        Close the current workbook.
        """

        if self.workbook is not None:
            self.workbook.close()
            self.__workbook = None

    def make_worksheet(self, sheet_name):
        """
        Make a worksheet to the current workbook.

        :param str sheet_name:
            Name of the worksheet to create. Name of the work sheet will 
            automatically decided (like ``"Sheet1"``)
            if the ``sheet_name`` is empty.
        """

        if dataproperty.is_not_empty_string(sheet_name):
            if sheet_name in self.__sheet_table:
                # the sheet is already exists
                self.stream = self.__sheet_table.get(sheet_name)
                return

            work_sheet_name = sheet_name
        else:
            work_sheet_name = None

        worksheet = self.workbook.workbook.add_worksheet(
            work_sheet_name)

        self.__sheet_table[worksheet.name] = worksheet
        self.stream = worksheet

    def write_null_line(self):
        pass

    def write_table(self):
        """
        Write a table to the current worksheet.
        """

        self._verify_property()
        self._preprocess_property()
        self.__set_cell_width()

        self._write_header()
        self._write_value_matrix()

        self.__postprocess()

    def _write_header(self):
        if dataproperty.is_empty_list_or_tuple(self.header_list):
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

    def _write_value_matrix(self):
        col_numproperty_table = self.__get_number_property()

        for row, value_prop_list in enumerate(self._value_prop_matrix):
            sheet_row = self.first_data_row + row

            for col, prop in enumerate(value_prop_list):
                base_props = dict(self.__cell_format_property)
                key = "%d_%d" % (col, prop.typecode)

                if prop.typecode in [dataproperty.Typecode.INT, dataproperty.Typecode.FLOAT]:
                    num_props = col_numproperty_table.get(col, {})
                    base_props.update(num_props)

                    cell_format = self.__col_cell_format_cache.get(key)
                    if cell_format is None:
                        # cache miss
                        cell_format = self.__add_format(base_props)
                        self.__col_cell_format_cache[key] = cell_format

                    try:
                        self.stream.write_number(
                            sheet_row, col, float(prop.data), cell_format)
                    except TypeError:
                        pass
                else:
                    if prop.data is None:
                        base_props = dict(self.__nan_format_property)

                    cell_format = self.__col_cell_format_cache.get(key)
                    if cell_format is None:
                        # cache miss
                        cell_format = self.__add_format(base_props)
                        self.__col_cell_format_cache[key] = cell_format

                    self.stream.write(
                        sheet_row, col, prop.data, cell_format)

    def __get_number_property(self):
        dict_col_numprops = {}
        for col, col_prop in enumerate(self._column_prop_list):
            num_props = {}
            if dataproperty.is_integer(col_prop.minmax_decimal_places.max_value):
                float_digit = col_prop.minmax_decimal_places.max_value
                if float_digit > 0:
                    num_props = {"num_format": "0.%s" % ("0" * float_digit)}

            dict_col_numprops[col] = num_props

        return dict_col_numprops

    def __get_last_column(self):
        if dataproperty.is_not_empty_list_or_tuple(self.header_list):
            return len(self.header_list) - 1

        if dataproperty.is_not_empty_list_or_tuple(self.value_matrix):
            return len(self.value_matrix[0]) - 1

        raise ValueError()

    def __add_format(self, dict_property):
        return self.workbook.workbook.add_format(dict_property)

    def __set_cell_width(self):
        font_size = self.__cell_format_property.get("font_size")

        if not dataproperty.is_integer(font_size):
            return

        for col_idx, col_prop in enumerate(self._column_prop_list):
            width = (
                min(col_prop.padding_len, self.MAX_CELL_WIDTH) *
                (font_size / 10.0) + 2
            )
            self.stream.set_column(col_idx, col_idx, width=width)

    def __postprocess(self):
        self.__last_data_row = self.first_data_row + len(self.value_matrix)
        self.__last_data_col = self.__get_last_column()

        self.stream.autofilter(
            self.last_header_row, self.first_data_col,
            self.last_data_row, self.last_data_col)
        self.stream.freeze_panes(self.first_data_row, self.first_data_col)
