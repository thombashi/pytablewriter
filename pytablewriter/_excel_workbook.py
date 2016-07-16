# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import xlsxwriter


class ExcelWorkbookXlsx(object):

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
