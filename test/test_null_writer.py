# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import collections

import pytablewriter
import pytest


table_writer_class = pytablewriter.NullTableWriter


class Test_NullTableWriter_set_indent_level:

    def test_smoke(self, capsys):
        writer = table_writer_class()
        writer.set_indent_level(0)


class Test_NullTableWriter_inc_indent_level:

    def test_smoke(self, capsys):
        writer = table_writer_class()
        writer.inc_indent_level()


class Test_NullTableWriter_dec_indent_level:

    def test_smoke(self, capsys):
        writer = table_writer_class()
        writer.dec_indent_level()


class Test_NullTableWriter_write_new_line:

    def test_smoke(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, err = capsys.readouterr()
        assert out == ""


class Test_NullTableWriter_write_table:

    def test_smoke(self, capsys):
        writer = table_writer_class()
        writer.write_table()

        out, err = capsys.readouterr()
        assert out == ""
