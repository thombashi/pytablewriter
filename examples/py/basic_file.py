#!/usr/bin/env python
# encoding: utf-8

import six
import pytablewriter


filename = "sample.rst"

writer = pytablewriter.RstGridTableWriter()
writer.table_name = "zone"
writer.header_list = ["zone_id", "country_code", "zone_name"]
writer.value_matrix = [
    ["1", "AD", "Europe/Andorra"],
    ["2", "AE", "Asia/Dubai"],
    ["3", "AF", "Asia/Kabul"],
    ["4", "AG", "America/Antigua"],
    ["5", "AI", "America/Anguilla"],
]

with open(filename, "w") as f:
    writer.stream = f
    writer.write_table()

with open(filename) as f:
    six.print_(f.read())
