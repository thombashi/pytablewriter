# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, print_function, unicode_literals

from textwrap import dedent

import pytablewriter

from ..._common import print_test_result
from ...data import style_tabledata, styles


table_writer_class = pytablewriter.UnicodeTableWriter


class Test_UnicodeTableWriter_write_new_line(object):
    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_UnicodeTableWriter_write_table(object):
    def test_normal_styles(self, capsys):
        writer = table_writer_class()
        writer.from_tabledata(style_tabledata)
        writer.styles = styles
        writer.write_table()

        expected = dedent(
            """\
            ┌────┬─────┬────┬─────┬──────┬─────┬────────────┬──────┬────────┬─────────────┐
            │none│empty│tiny│small│medium│large│null w/ bold│L bold│S italic│L bold italic│
            ├────┼─────┼────┼─────┼──────┼─────┼────────────┼──────┼────────┼─────────────┤
            │ 111│  111│ 111│  111│   111│  111│            │   111│     111│          111│
            ├────┼─────┼────┼─────┼──────┼─────┼────────────┼──────┼────────┼─────────────┤
            │1234│ 1234│1234│ 1234│ 1,234│1 234│            │  1234│    1234│         1234│
            └────┴─────┴────┴─────┴──────┴─────┴────────────┴──────┴────────┴─────────────┘
            """
        )

        out = writer.dumps()
        print_test_result(expected=expected, actual=out)
        assert out == expected
