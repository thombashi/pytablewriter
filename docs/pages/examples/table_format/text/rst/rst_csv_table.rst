.. _example-rst-csv-table-writer:

reStructuredText CSV Table
-------------------------------------------
|RstCsvTableWriter| class can write a table with reStructuredText CSV table format to the |stream| from a data matrix.

:Sample Code:
    .. code-block:: python
        :caption: Write a reStructuredText CSV table

        import pytablewriter

        def main():
            writer = pytablewriter.RstCsvTableWriter()
            writer.table_name = "example_table"
            writer.headers = ["int", "float", "str", "bool", "mix", "time"]
            writer.value_matrix = [
                [0,   0.1,      "hoge", True,   0,      "2017-01-01 03:04:05+0900"],
                [2,   "-2.23",  "foo",  False,  None,   "2017-12-23 45:01:23+0900"],
                [3,   0,        "bar",  "true",  "inf", "2017-03-03 33:44:55+0900"],
                [-10, -9.9,     "",     "FALSE", "nan", "2017-01-01 00:00:00+0900"],
            ]

            writer.write_table()

        if __name__ == "__main__":
            main()

:Output:
    .. code-block:: ReST

        .. csv-table:: example_table
            :header: "int", "float", "str", "bool", "mix", "time"
            :widths: 5, 7, 6, 6, 8, 26

            0, 0.10, "hoge", True, 0, "2017-01-01 03:04:05+0900"
            2, -2.23, "foo", False, , "2017-12-23 12:34:51+0900"
            3, 0.00, "bar", True, Infinity, "2017-03-03 22:44:55+0900"
            -10, -9.90, , False, NaN, "2017-01-01 00:00:00+0900"

:Rendering Result:
    .. csv-table:: example_table
        :header: "int", "float", "str", "bool", "mix", "time"
        :widths: 5, 7, 6, 6, 8, 26

        0, 0.10, "hoge", True, 0, "2017-01-01 03:04:05+0900"
        2, -2.23, "foo", False, , "2017-12-23 12:34:51+0900"
        3, 0.00, "bar", True, Infinity, "2017-03-03 22:44:55+0900"
        -10, -9.90, , False, NaN, "2017-01-01 00:00:00+0900"
