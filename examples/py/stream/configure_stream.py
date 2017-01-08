#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import print_function

import pytablewriter
import six


writer = pytablewriter.MarkdownTableWriter()
writer.table_name = "zone"
writer.header_list = ["zone_id", "country_code", "zone_name"]
writer.value_matrix = [
    ["1", "AD", "Europe/Andorra"],
    ["2", "AE", "Asia/Dubai"],
    ["3", "AF", "Asia/Kabul"],
    ["4", "AG", "America/Antigua"],
    ["5", "AI", "America/Anguilla"],
]

# writer instance will write a table to stdout in default
writer.write_table()

# change stream to string buffer to get output as a string
writer.stream = six.StringIO()
writer.write_table()
print()
print(writer.stream.getvalue())

# change output stream to a file
with open("sample.md", "w") as f:
    writer.stream = f
    writer.write_table()
