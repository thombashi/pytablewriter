# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import abc

import six
import xlsxwriter


@six.add_metaclass(abc.ABCMeta)
class ExcelWorkbookInterface(object):

    @abc.abstractproperty
    def workbook(self):
        pass

    @abc.abstractproperty
    def file_path(self):
        pass

    @abc.abstractmethod
    def open(self, file_path):
        pass

    @abc.abstractmethod
    def close(self):
        pass


class ExcelWorkbook(ExcelWorkbookInterface):

    @property
    def workbook(self):
        return self._workbook

    @property
    def file_path(self):
        return self._file_path

    def _clear(self):
        self._workbook = None
        self._file_path = None


class ExcelWorkbookXlsx(ExcelWorkbook):

    def __init__(self, file_path):
        self.open(file_path)

    def __del__(self):
        self.close()

    def open(self, file_path):
        self._file_path = file_path
        self._workbook = xlsxwriter.Workbook(file_path)

    def close(self):
        if self.workbook is None:
            return

        self._workbook.close()
        self._clear()

    def add_worksheet(self, worksheet_name):
        worksheet = self.workbook.add_worksheet(worksheet_name)

        return worksheet
