"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from textwrap import dedent

import pytest

from pytablewriter import BoldUnicodeTableWriter, UnicodeTableWriter

from ..._common import print_test_result
from ...data import vut_style_tabledata, vut_styles
from ._common import regexp_ansi_escape, strip_ansi_escape


try:
    import pandas as pd

    SKIP_DATAFRAME_TEST = False
except ImportError:
    SKIP_DATAFRAME_TEST = True


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
    def test_normal_styles(self):
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
        assert strip_ansi_escape(out) == expected

    @pytest.mark.skipif(SKIP_DATAFRAME_TEST, reason="required package not found")
    def test_normal_numbers(self):
        writer = UnicodeTableWriter(
            dataframe=pd.DataFrame(
                {"realnumber": ["0.000000000000001", "1"], "long": ["1,000,000,000,000", "1"]}
            ),
            margin=1,
        )

        expected = dedent(
            """\
            ┌───────────────────┬───────────────┐
            │    realnumber     │     long      │
            ├───────────────────┼───────────────┤
            │ 0.000000000000001 │ 1000000000000 │
            ├───────────────────┼───────────────┤
            │ 1.000000000000000 │             1 │
            └───────────────────┴───────────────┘
            """
        )

        output = writer.dumps()
        print_test_result(expected=expected, actual=output)
        assert output == expected

    def test_normal_max_precision(self):
        writer = UnicodeTableWriter(
            headers=["realnumber", "long"],
            value_matrix=[
                ["0.000000000000001", "1,000,000,000,000"],
                ["1", "1"],
            ],
            margin=1,
            max_precision=3,
        )

        expected = dedent(
            """\
            ┌────────────┬───────────────┐
            │ realnumber │     long      │
            ├────────────┼───────────────┤
            │      0.000 │ 1000000000000 │
            ├────────────┼───────────────┤
            │      1.000 │             1 │
            └────────────┴───────────────┘
            """
        )

        output = writer.dumps()
        print_test_result(expected=expected, actual=output)
        assert output == expected


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
        assert strip_ansi_escape(out) == expected
