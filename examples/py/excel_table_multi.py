#!/usr/bin/env python3

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from pytablewriter import ExcelXlsxTableWriter


def main() -> None:
    writer = ExcelXlsxTableWriter()
    filepath = "multi_sheet_example.xlsx"

    # write the first worksheet
    writer.table_name = "example"
    writer.headers = ["int", "float", "str", "bool", "mix", "time"]
    writer.value_matrix = [
        [0, 0.1, "hoge", True, 0, "2017-01-01 03:04:05+0900"],
        [2, "-2.23", "foo", False, None, "2017-12-23 12:34:51+0900"],
        [3, 0, "bar", "true", "inf", "2017-03-03 22:44:55+0900"],
        [-10, -9.9, "", "FALSE", "nan", "2017-01-01 00:00:00+0900"],
    ]
    writer.dump(filepath, close_after_write=False)

    # write the second worksheet
    writer.table_name = "Timezone"
    writer.headers = [
        "zone_id",
        "abbreviation",
        "time_start",
        "gmt_offset",
        "dst",
    ]
    writer.value_matrix = [
        ["1", "CEST", "1017536400", "7200", "1"],
        ["1", "CEST", "1048986000", "7200", "1"],
        ["1", "CEST", "1080435600", "7200", "1"],
        ["1", "CEST", "1111885200", "7200", "1"],
        ["1", "CEST", "1143334800", "7200", "1"],
    ]
    writer.dump(filepath)


if __name__ == "__main__":
    main()
