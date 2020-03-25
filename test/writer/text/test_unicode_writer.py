"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from textwrap import dedent

import pytest

from pytablewriter import BoldUnicodeTableWriter, UnicodeTableWriter

from ..._common import print_test_result
from ...data import style_tabledata, styles


class Test_UnicodeTableWriter_write_new_line:
    @pytest.mark.parametrize(
        ["table_writer_class"], [[UnicodeTableWriter], [BoldUnicodeTableWriter],]
    )
    def test_normal(self, capsys, table_writer_class):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_UnicodeTableWriter_write_table:
    def test_normal_styles(self, capsys):
        writer = UnicodeTableWriter()
        writer.from_tabledata(style_tabledata)
        writer.column_styles = styles
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


class Test_BoldUnicodeTableWriter_write_table:
    def test_normal_styles(self, capsys):
        writer = BoldUnicodeTableWriter()
        writer.from_tabledata(style_tabledata)
        writer.column_styles = styles
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
        assert out == expected
