.. _example-yaml-table-writer:

YAML
----------------------------
|YamlTableWriter| class can write a
`YAML <https://yaml.org/>`__
format table to the |stream| from a data matrix.

:Sample Code:
    .. code-block:: python
        :caption: Write a YAML table

        import pytablewriter as ptw

        def main():
            writer = ptw.YamlTableWriter()
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
    .. code-block:: yaml

        example_table:
        - bool: true
          float: 0.1
          int: 0
          mix: 0
          str: hoge
          time: 2017-01-01 03:04:05+0900
        - bool: false
          float: -2.23
          int: 2
          mix: ''
          str: foo
          time: 2017-12-23 45:01:23+0900
        - bool: true
          float: 0
          int: 3
          mix: .inf
          str: bar
          time: 2017-03-03 33:44:55+0900
        - bool: false
          float: -9.9
          int: -10
          mix: .nan
          str: ''
          time: 2017-01-01 00:00:00+0900
