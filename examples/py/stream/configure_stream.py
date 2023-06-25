#!/usr/bin/env python3

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import io

import pytablewriter as ptw


def main() -> None:
    writer = ptw.MarkdownTableWriter(
        table_name="zone",
        headers=["zone_id", "country_code", "zone_name"],
        value_matrix=[
            ["1", "AD", "Europe/Andorra"],
            ["2", "AE", "Asia/Dubai"],
            ["3", "AF", "Asia/Kabul"],
            ["4", "AG", "America/Antigua"],
            ["5", "AI", "America/Anguilla"],
        ],
    )

    # writer instance writes a table to stdout by default
    writer.write_table()
    writer.write_null_line()

    # change the stream to a string buffer to get the output as a string
    # you can also get tabular text by using dumps method
    writer.stream = io.StringIO()
    writer.write_table()
    print(writer.stream.getvalue())

    # change the output stream to a file
    with open("sample.md", "w") as f:
        writer.stream = f
        writer.write_table()

    # or you can use dump method to file if you just output a table to a file
    # writer.dump("sample.md")


if __name__ == "__main__":
    main()
