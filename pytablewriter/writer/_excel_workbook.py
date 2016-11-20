# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import abc

import dataproperty as dp
import pathvalidate
import six
import xlsxwriter
import xlwt


@six.add_metaclass(abc.ABCMeta)
class ExcelWorkbookInterface(object):

    @abc.abstractproperty
    def workbook(self):  # pragma: no cover
        pass

    @abc.abstractproperty
    def file_path(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def open(self, file_path):  # pragma: no cover
        pass

    @abc.abstractmethod
    def close(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def add_worksheet(self, worksheet_name):  # pragma: no cover
        pass


class ExcelWorkbook(ExcelWorkbookInterface):

    @property
    def workbook(self):
        return self._workbook

    @property
    def file_path(self):
        return self._file_path

    def __init__(self, file_path):
        self._clear()
        self._file_path = file_path

    def __del__(self):
        self.close()

    def _clear(self):
        self._workbook = None
        self._file_path = None
        self._worksheet_table = {}


class ExcelWorkbookXls(ExcelWorkbook):

    def __init__(self, file_path):
        super(ExcelWorkbookXls, self).__init__(file_path)

        self.open(file_path)

    def open(self, file_path):
        self._workbook = xlwt.Workbook()

    def close(self):
        if self.workbook is None:
            return

        self.workbook.save(self._file_path)
        self._clear()

    def add_worksheet(self, worksheet_name):
        worksheet_name = pathvalidate.sanitize_excel_sheet_name(worksheet_name)

        if dp.is_not_empty_string(worksheet_name):
            if worksheet_name in self._worksheet_table:
                # the work sheet is already exists
                return self._worksheet_table.get(worksheet_name)
        else:
            sheet_id = 1
            while True:
                worksheet_name = "Sheet{:d}".format(sheet_id)
                if worksheet_name not in self._worksheet_table:
                    break
                sheet_id += 1

        worksheet = self.workbook.add_sheet(worksheet_name)
        self._worksheet_table[worksheet_name] = worksheet

        return worksheet


class ExcelWorkbookXlsx(ExcelWorkbook):

    def __init__(self, file_path):
        super(ExcelWorkbookXlsx, self).__init__(file_path)

        self.open(file_path)

    def open(self, file_path):
        self._workbook = xlsxwriter.Workbook(file_path)

    def close(self):
        if self.workbook is None:
            return

        self._workbook.close()
        self._clear()

    def add_worksheet(self, worksheet_name):
        worksheet_name = pathvalidate.sanitize_excel_sheet_name(worksheet_name)

        if dp.is_not_empty_string(worksheet_name):
            if worksheet_name in self._worksheet_table:
                # the work sheet is already exists
                return self._worksheet_table.get(worksheet_name)
        else:
            worksheet_name = None

        worksheet = self.workbook.add_worksheet(worksheet_name)
        self._worksheet_table[worksheet_name] = worksheet

        return worksheet
