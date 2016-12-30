# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import dataproperty as dp
from six.moves import zip
import pathvalidate

from ._csv_writer import CsvTableWriter


class LtsvTableWriter(CsvTableWriter):
    """
    A table writer class for
    `Labeled Tab-separated Values (LTSV) <http://ltsv.org/>`__ format.

    :Examples:

        :ref:`example-ltsv-table-writer`
    """

    @property
    def support_split_write(self):
        return True

    def __init__(self):
        super(LtsvTableWriter, self).__init__()

        self.is_write_header = False

    def write_table(self):
        """
        |write_table| with
        `Labeled Tab-separated Values (LTSV) <http://ltsv.org/>`__ format.
        Invalid characters in labels/data will be removed.

        :raises pytablewriter.EmptyHeaderError: If the |header_list| is empty.
        """

        self._verify_property()
        self._preprocess()

        for value_list in self._value_matrix:
            ltsv_item_list = [
                "{:s}:{}".format(
                    pathvalidate.sanitize_ltsv_label(header_name), value)
                for header_name, value in zip(self.header_list, value_list)
                if dp.is_not_empty_string(value)
            ]

            if dp.is_empty_sequence(ltsv_item_list):
                continue

            self.stream.write("\t".join(ltsv_item_list) + "\n")

    def _verify_header(self):
        self._validate_empty_header()
