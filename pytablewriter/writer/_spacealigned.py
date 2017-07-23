# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import copy

import dataproperty

from ._csv import CsvTableWriter


class SpaceAlignedTableWriter(CsvTableWriter):
    """
    A table writer class for space aligned format.

    .. py:method:: write_table

        |write_table| with space aligned format.

        :Example:
            :ref:`example-space-aligned-table-writer`
    """

    @property
    def format_name(self):
        return "space_aligned"

    def __init__(self):
        super(SpaceAlignedTableWriter, self).__init__()

        self.column_delimiter = "  "
        self.is_padding = True

        self._quoting_flags = copy.deepcopy(dataproperty.NOT_QUOTING_FLAGS)
