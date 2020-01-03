.. _example-sqlite-table-writer:

SQLite
----------------------------
|SqliteTableWriter| class can write a table to
a SQLite database file from a matrix of data.

:Sample Code:
    .. code-block:: python
        :caption: Write a SQLite table

        import pytablewriter

        def main():
            writer = pytablewriter.SqliteTableWriter()
            writer.open("sample.sqlite")

            # create the first table
            writer.table_name = "example"
            writer.headers = ["int", "float", "str", "bool", "mix", "time"]
            writer.value_matrix = [
                [0,   0.1,      "hoge", True,   0,      "2017-01-01 03:04:05+0900"],
                [2,   "-2.23",  "foo",  False,  None,   "2017-12-23 12:34:51+0900"],
                [3,   0,        "bar",  "true",  "inf", "2017-03-03 22:44:55+0900"],
                [-10, -9.9,     "",     "FALSE", "nan", "2017-01-01 00:00:00+0900"],
            ]
            writer.write_table()

            # write the second table
            writer.table_name = "Timezone"
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
    .. code-block:: none

        $ sqlite3 sample.sqlite
        sqlite> .schema
        CREATE TABLE 'example' (int INTEGER, float REAL, str TEXT, bool TEXT, mix REAL, time TEXT);
        CREATE TABLE 'Timezone' ("zone_id" INTEGER, abbreviation TEXT, "time_start" INTEGER, "gmt_offset" INTEGER, dst INTEGER);
        sqlite> select * from example;
        0|0.1|hoge|1|0.0|2017-01-01 03:04:05+0900
        2|-2.23|foo|0||2017-12-23 12:34:51+0900
        3|0.0|bar|1|Inf|2017-03-03 22:44:55+0900
        -10|-9.9||0||2017-01-01 00:00:00+0900
        sqlite> select * from Timezone;
        1|CEST|1017536400|7200|1
        1|CEST|1048986000|7200|1
        1|CEST|1080435600|7200|1
        1|CEST|1111885200|7200|1
        1|CEST|1143334800|7200|1
