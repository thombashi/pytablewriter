.. _example-toml-table-writer:

Write a TOML table
----------------------------

|TomlTableWriter| class can write a
`TOML <https://github.com/toml-lang/toml>`__
format table to the |stream| from a matrix of data.

.. code-block:: python
    :caption: Sample code that writes a TOML table

    import pytablewriter

    writer = pytablewriter.TomlTableWriter()
    writer.header_list = ["int", "float", "str", "bool", "mix", "time"]
    writer.value_matrix = [
        [0,   0.1,      "hoge", True,   0,      "2017-01-01 03:04:05+0900"],
        [2,   "-2.23",  "foo",  False,  None,   "2017-12-23 45:01:23+0900"],
        [3,   0,        "bar",  "true",  "inf", "2017-03-03 33:44:55+0900"],
        [-10, -9.9,     "",     "FALSE", "nan", "2017-01-01 00:00:00+0900"],
    ]
    
    writer.write_table()


.. code-block:: none
    :caption: Output of TOML

    [[example_table]]
    int = 0
    float = 0.1
    mix = 0
    bool = true
    str = "hoge"
    time = "2017-01-01 03:04:05+0900"
    [[example_table]]
    int = 2
    float = -2.23
    bool = false
    str = "foo"
    time = "2017-12-23 12:34:51+0900"
    [[example_table]]
    int = 3
    float = 0
    mix = Infinity
    bool = true
    str = "bar"
    time = "2017-03-03 22:44:55+0900"
    [[example_table]]
    int = -10
    float = -9.9
    mix = NaN
    bool = false
    str = ""
    time = "2017-01-01 00:00:00+0900"
