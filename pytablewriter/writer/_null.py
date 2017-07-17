# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

from ._interface import (
    TableWriterInterface,
    TextWriterInterface,
    IndentationInterface
)


class NullTableWriter(
        IndentationInterface, TextWriterInterface, TableWriterInterface):

    @property
    def format_name(self):
        return "null"

    @property
    def support_split_write(self):
        return True

    def set_indent_level(self, indent_level):
        pass

    def inc_indent_level(self):
        pass

    def dec_indent_level(self):
        pass

    def write_null_line(self):
        pass

    def write_table(self):
        pass

    def _write_table_iter(self):
        pass

    def close(self):
        pass

    def _write_value_row_separator(self):
        pass
