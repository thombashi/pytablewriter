#!/usr/bin/env python
# encoding: utf-8

import pytablewriter


writer = pytablewriter.ExcelTableWriter()
writer.open_workbook("sample.xlsx")

writer.make_worksheet("zone")
writer.header_list = ["zone_id", "country_code", "zone_name"]
writer.value_matrix = [
    ["1", "AD", "Europe/Andorra"],
    ["2", "AE", "Asia/Dubai"],
    ["3", "AF", "Asia/Kabul"],
    ["4", "AG", "America/Antigua"],
    ["5", "AI", "America/Anguilla"],
]
writer.write_table()

writer.close()
