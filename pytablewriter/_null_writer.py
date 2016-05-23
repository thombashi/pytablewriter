# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

from ._interface import TableWriterInterface
from ._interface import TextWriterInterface
from ._interface import IndentationInterface


class NullTableWriter(
        IndentationInterface, TextWriterInterface, TableWriterInterface):

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
