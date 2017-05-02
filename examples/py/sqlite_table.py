#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import pytablewriter


writer = pytablewriter.SqliteTableWriter()
writer.open("sample.sqlite")

# create the first table
writer.table_name = "example"
writer.header_list = ["int", "float", "str", "bool", "mix", "time"]
writer.value_matrix = [
    [0,   0.1,      "hoge", True,   0,      "2017-01-01 03:04:05+0900"],
    [2,   "-2.23",  "foo",  False,  None,   "2017-12-23 12:34:51+0900"],
    [3,   0,        "bar",  "true",  "inf", "2017-03-03 22:44:55+0900"],
    [-10, -9.9,     "",     "FALSE", "nan", "2017-01-01 00:00:00+0900"],
]
writer.write_table()

# write the second table
writer.table_name = "Timezone"
writer.header_list = [
    "zone_id", "abbreviation", "time_start", "gmt_offset", "dst",
]
writer.value_matrix = [
    ["1", "CEST", "1017536400", "7200", "1"],
    ["1", "CEST", "1048986000", "7200", "1"],
    ["1", "CEST", "1080435600", "7200", "1"],
    ["1", "CEST", "1111885200", "7200", "1"],
    ["1", "CEST", "1143334800", "7200", "1"],
]
writer.write_table()

writer.close()
