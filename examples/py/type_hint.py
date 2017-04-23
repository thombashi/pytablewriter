#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import print_function

from datetime import datetime

import pytablewriter as ptw

writer = ptw.JavaScriptTableWriter()
writer.header_list = ["header_a", "header_b", "header_c"]
writer.value_matrix = [
    [-1.1, "2017-01-02 03:04:05", datetime(2017, 1, 2, 3, 4, 5)],
    [0.12, "2017-02-03 04:05:06", datetime(2017, 2, 3, 4, 5, 6)],
]

print("// without type hints: column types will be detected automatically in default")
writer.table_name = "without type hint"
writer.write_table()
print()


print("// with type hints: Integer, DateTime, String")
writer.table_name = "with type hint"
writer.type_hint_list = [ptw.Integer, ptw.DateTime, ptw.String]
writer.write_table()
