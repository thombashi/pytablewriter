# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pytablewriter as ptw
import pytest


class Test_CsvTableWriter_write_table:

    @pytest.mark.parametrize(["format_name"], [
        [format_name]
        for format_name in ptw.TableWriterFactory.get_format_name_list()
        if format_name not in ["null", "excel"]
    ])
    def test_smoke_multi_byte(self, capsys, format_name):
        writer = ptw.TableWriterFactory.create_from_format_name(format_name)
        writer.table_name = "生成に関するパターン"
        writer.header_list = ["パターン名", "概要", "GoF", "Code Complete[1]"]
        writer.value_matrix = [
            ["Abstract Factory",
                "関連する一連のインスタンスを状況に応じて、適切に生成する方法を提供する。", "Yes", "Yes"],
            ["Builder", "複合化されたインスタンスの生成過程を隠蔽する。", "Yes", "No"],
            ["Factory Method",
                "実際に生成されるインスタンスに依存しない、インスタンスの生成方法を提供する。", "Yes", "Yes"],
            ["Prototype", "同様のインスタンスを生成するために、原型のインスタンスを複製する。", "Yes", "No"],
            ["Singleton", "あるクラスについて、インスタンスが単一であることを保証する。", "Yes", "Yes"],
        ]

        writer.write_table()

        out, _err = capsys.readouterr()

        assert len(out) > 100
