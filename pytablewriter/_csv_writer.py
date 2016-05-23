# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import dataproperty

from ._text_writer import TextTableWriter


class CsvTableWriter(TextTableWriter):
    """
    Concrete class of a table writer for CSV format.

    :Examples:

        :ref:`example-csv-table-writer`
    """

    def __init__(self):
        super(CsvTableWriter, self).__init__()

        self.indent_string = u""
        self.column_delimiter = u","
        self.is_padding = False
        self.is_write_header_separator_row = False

    def _verify_header(self):
        pass

    def _write_header(self):
        if dataproperty.is_empty_list_or_tuple(self.header_list):
            return

        super(CsvTableWriter, self)._write_header()
