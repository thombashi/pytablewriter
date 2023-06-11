.. _example-toml-table-writer:

TOML
----------------------------
|TomlTableWriter| class can write a
`TOML <https://github.com/toml-lang/toml>`__
format table to the |stream| from a data matrix.

:Sample Code:
    .. code-block:: python
        :caption: Write a TOML table

        import pytablewriter

        def main():
            writer = pytablewriter.TomlTableWriter()
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
    .. code-block:: toml

        [[example_table]]
        int = 0
        float = 0.1
        str = "hoge"
        bool = true
        mix = 0
        time = "2017-01-01 03:04:05+0900"

        [[example_table]]
        int = 2
        float = -2.23
        str = "foo"
        bool = false
        time = "2017-12-23 45:01:23+0900"

        [[example_table]]
        int = 3
        float = 0
        str = "bar"
        bool = true
        mix = inf
        time = "2017-03-03 33:44:55+0900"

        [[example_table]]
        int = -10
        float = -9.9
        str = ""
        bool = false
        mix = nan
        time = "2017-01-01 00:00:00+0900"
