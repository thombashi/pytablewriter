#!/usr/bin/env python3

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import pytablewriter as ptw


def main() -> None:
    writer = ptw.RstSimpleTableWriter(
        table_name="生成に関するパターン",
        headers=["パターン名", "概要", "GoF", "Code Complete[1]"],
        value_matrix=[
            [
                "Abstract Factory",
                "関連する一連のインスタンスを状況に応じて、適切に生成する方法を提供する。",
                "Yes",
                "Yes",
            ],
            ["Builder", "複合化されたインスタンスの生成過程を隠蔽する。", "Yes", "No"],
            [
                "Factory Method",
                "実際に生成されるインスタンスに依存しない、インスタンスの生成方法を提供する。",
                "Yes",
                "Yes",
            ],
            [
                "Prototype",
                "同様のインスタンスを生成するために、原型のインスタンスを複製する。",
                "Yes",
                "No",
            ],
            [
                "Singleton",
                "あるクラスについて、インスタンスが単一であることを保証する。",
                "Yes",
                "Yes",
            ],
        ],
        theme="altrow",
    )
    writer.write_table()


if __name__ == "__main__":
    main()
