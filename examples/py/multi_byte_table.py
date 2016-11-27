#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import print_function

import pytablewriter


writer = pytablewriter.RstSimpleTableWriter()
writer.table_name = "生成に関するパターン"
writer.header_list = ["パターン名", "概要", "GoF", "Code Complete[1]"]
writer.value_matrix = [
    ["Abstract Factory", "関連する一連のインスタンスを状況に応じて、適切に生成する方法を提供する。", "Yes", "Yes"],
    ["Builder", "複合化されたインスタンスの生成過程を隠蔽する。", "Yes", "No"],
    ["Factory Method", "実際に生成されるインスタンスに依存しない、インスタンスの生成方法を提供する。", "Yes", "Yes"],
    ["Prototype", "同様のインスタンスを生成するために、原型のインスタンスを複製する。", "Yes", "No"],
    ["Singleton", "あるクラスについて、インスタンスが単一であることを保証する。", "Yes", "Yes"],
]
writer.write_table()
