# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import pathvalidate
import typepy

from six.moves import zip

from ._csv import CsvTableWriter


class LtsvTableWriter(CsvTableWriter):
    """
    A table writer class for
    `Labeled Tab-separated Values (LTSV) <http://ltsv.org/>`__ format.
    """

    @property
    def format_name(self):
        return "ltsv"

    @property
    def support_split_write(self):
        return True

    def __init__(self):
        super(LtsvTableWriter, self).__init__()

        self.is_write_header = False

        self._is_require_header = True

    def write_table(self):
        """
        |write_table| with
        `Labeled Tab-separated Values (LTSV) <http://ltsv.org/>`__ format.
        Invalid characters in labels/data are removed.

        :raises pytablewriter.EmptyHeaderError: If the |header_list| is empty.
        :Example:
            :ref:`example-ltsv-table-writer`
        """

        self._logger.logging_start_write()

        self._verify_property()
        self._preprocess()

        for value_list in self._value_matrix:
            ltsv_item_list = [
                "{:s}:{}".format(
                    pathvalidate.sanitize_ltsv_label(header_name), value)
                for header_name, value in zip(self.header_list, value_list)
                if typepy.is_not_null_string(value)
            ]

            if typepy.is_empty_sequence(ltsv_item_list):
                continue

            self.stream.write("\t".join(ltsv_item_list) + "\n")

        self._logger.logging_complete_write()
