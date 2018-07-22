# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import simplejson as json

from ._json import JsonTableWriter


class JsonLinesTableWriter(JsonTableWriter):
    """
    A table writer class for JSON lines format.
    """

    @property
    def format_name(self):
        return "json_lines"

    @property
    def support_split_write(self):
        return True

    def write_table(self):
        """
        |write_table| with
        `Labeled Tab-separated Values (LTSV) <http://ltsv.org/>`__ format.
        Invalid characters in labels/data are removed.

        :raises pytablewriter.EmptyHeaderError: If the |header_list| is empty.
        :Example:
            :ref:`example-ltsv-table-writer`
        """

        with self._logger:
            self._verify_property()
            self._preprocess()

            for value_list in self._table_value_matrix:
                self._write_line(json.dumps(value_list))
