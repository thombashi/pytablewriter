"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import pytest

import pytablewriter as ptw


class Test_CsvTableWriter_write_table:
    @pytest.mark.parametrize(
        ["format_name"],
        [[tblfmt.names[0]] for tblfmt in ptw.TableFormat.find_all_attr(ptw.FormatAttr.TEXT)],
    )
    def test_smoke_multi_byte(self, format_name):
        writer = ptw.TableWriterFactory.create_from_format_name(
            format_name,
            table_name="生成に関するパターン",
            headers=["パターン名", "概要", "GoF", "Code Complete[1]"],
            value_matrix=[
                ["Abstract Factory", "関連する一連のインスタンスを状況に応じて、適切に生成する方法を提供する。", "Yes", "Yes"],
                ["Builder", "複合化されたインスタンスの生成過程を隠蔽する。", "Yes", "No"],
                ["Factory Method", "実際に生成されるインスタンスに依存しない、インスタンスの生成方法を提供する。", "Yes", "Yes"],
                ["Prototype", "同様のインスタンスを生成するために、原型のインスタンスを複製する。", "Yes", "No"],
                ["Singleton", "あるクラスについて、インスタンスが単一であることを保証する。", "Yes", "Yes"],
            ],
        )

        assert len(writer.dumps()) > 100
