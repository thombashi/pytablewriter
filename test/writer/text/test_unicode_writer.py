"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from textwrap import dedent

import pytest

from pytablewriter import BoldUnicodeTableWriter, UnicodeTableWriter

from ..._common import print_test_result
from ...data import vut_style_tabledata, vut_styles
from ._common import regexp_ansi_escape


class Test_UnicodeTableWriter_write_new_line:
    @pytest.mark.parametrize(
        ["table_writer_class"],
        [
            [UnicodeTableWriter],
            [BoldUnicodeTableWriter],
        ],
    )
    def test_normal(self, capsys, table_writer_class):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_UnicodeTableWriter_write_table:
    def test_normal_styles(self, capsys):
        writer = UnicodeTableWriter()
        writer.from_tabledata(vut_style_tabledata)
        writer.column_styles = vut_styles
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
        assert regexp_ansi_escape.search(out)
        assert regexp_ansi_escape.sub("", out) == expected


class Test_BoldUnicodeTableWriter_write_table:
    def test_normal_styles(self, capsys):
        writer = BoldUnicodeTableWriter()
        writer.from_tabledata(vut_style_tabledata)
        writer.column_styles = vut_styles
        writer.write_table()

        expected = dedent(
            """\
            ┏━━━━┳━━━━━┳━━━━┳━━━━━┳━━━━━━┳━━━━━┳━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━┓
            ┃none┃empty┃tiny┃small┃medium┃large┃null w/ bold┃L bold┃S italic┃L bold italic┃
            ┣━━━━╋━━━━━╋━━━━╋━━━━━╋━━━━━━╋━━━━━╋━━━━━━━━━━━━╋━━━━━━╋━━━━━━━━╋━━━━━━━━━━━━━┫
            ┃ 111┃  111┃ 111┃  111┃   111┃  111┃            ┃   111┃     111┃          111┃
            ┣━━━━╋━━━━━╋━━━━╋━━━━━╋━━━━━━╋━━━━━╋━━━━━━━━━━━━╋━━━━━━╋━━━━━━━━╋━━━━━━━━━━━━━┫
            ┃1234┃ 1234┃1234┃ 1234┃ 1,234┃1 234┃            ┃  1234┃    1234┃         1234┃
            ┗━━━━┻━━━━━┻━━━━┻━━━━━┻━━━━━━┻━━━━━┻━━━━━━━━━━━━┻━━━━━━┻━━━━━━━━┻━━━━━━━━━━━━━┛
            """
        )

        out = writer.dumps()
        print_test_result(expected=expected, actual=out)
        assert regexp_ansi_escape.search(out)
        assert regexp_ansi_escape.sub("", out) == expected
