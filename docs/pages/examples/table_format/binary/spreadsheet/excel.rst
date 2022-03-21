.. _example-excel-table-writer:

Excel Sheet
-------------------------------------------
|ExcelXlsxTableWriter| class can write a table to worksheet(s) in
an Excel workbook file (``.xlsx`` format) from a matrix of data.

.. include:: excel_single_example.txt


Excel Sheets
-------------------------------------------
:Sample Code:
    .. code-block:: python
        :caption: Write two Excel sheets

        import pytablewriter

        def main():
            writer = pytablewriter.ExcelXlsxTableWriter()
            writer.open("sample.xlsx")

            # write the first worksheet
            writer.make_worksheet("example")
            writer.headers = ["int", "float", "str", "bool", "mix", "time"]
            writer.value_matrix = [
                [0,   0.1,      "hoge", True,   0,      "2017-01-01 03:04:05+0900"],
                [2,   "-2.23",  "foo",  False,  None,   "2017-12-23 12:34:51+0900"],
                [3,   0,        "bar",  "true",  "inf", "2017-03-03 22:44:55+0900"],
                [-10, -9.9,     "",     "FALSE", "nan", "2017-01-01 00:00:00+0900"],
            ]
            writer.write_table()

            # write the second worksheet
            writer.make_worksheet("Timezone")
            writer.headers = [
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

        if __name__ == "__main__":
            main()

:Output:
    .. figure:: ss/excel_multi.png
       :scale: 100%
       :alt: excel_multi

       Output excel file (``sample_multi.xlsx``)
