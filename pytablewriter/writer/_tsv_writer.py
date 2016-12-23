# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

from ._csv_writer import CsvTableWriter


class TsvTableWriter(CsvTableWriter):
    """
    Concrete class of a table writer for tab separated values (TSV) format.

    :Examples:

        :ref:`example-tsv-table-writer`
    """

    def __init__(self):
        super(TsvTableWriter, self).__init__()

        self.column_delimiter = "\t"
