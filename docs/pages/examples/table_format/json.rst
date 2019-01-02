.. _example-json-table-writer:

JSON
----------------------------
|JsonTableWriter| class can write a table to the |stream| with JSON format
from a matrix of data.
JSON format change if the |table_name| has a valid value or not.

JSON with a table name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:Sample Code:
    .. code-block:: python
        :caption: JSON w/ table name

        from pytablewriter import JsonTableWriter

        writer = JsonTableWriter()
        writer.table_name = "example_table"
        writer.header_list = ["int", "float", "str", "bool", "mix", "time"]
        writer.value_matrix = [
            [0,   0.1,      "hoge", True,   0,      "2017-01-01 03:04:05+0900"],
            [2,   "-2.23",  "foo",  False,  None,   "2017-12-23 45:01:23+0900"],
            [3,   0,        "bar",  "true",  "inf", "2017-03-03 33:44:55+0900"],
            [-10, -9.9,     "",     "FALSE", "nan", "2017-01-01 00:00:00+0900"],
        ]

        writer.write_table()

:Output:
    .. code-block:: json

        { "example_table" : [
        {
            "bool": true,
            "float": 0.1,
            "int": 0,
            "mix": 0,
            "str": "hoge",
            "time": "2017-01-01 03:04:05+0900"
        },
        {
            "bool": false,
            "float": -2.23,
            "int": 2,
            "mix": null,
            "str": "foo",
            "time": "2017-12-23 12:34:51+0900"
        },
        {
            "bool": true,
            "float": 0,
            "int": 3,
            "mix": "Infinity",
            "str": "bar",
            "time": "2017-03-03 22:44:55+0900"
        },
        {
            "bool": false,
            "float": -9.9,
            "int": -10,
            "mix": "NaN",
            "str": "",
            "time": "2017-01-01 00:00:00+0900"
        }]}


JSON without a table name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:Sample Code:
    .. code-block:: python
        :caption: JSON w/o table name

        from pytablewriter import JsonTableWriter

        writer = JsonTableWriter()
        writer.header_list = ["int", "float", "str", "bool", "mix", "time"]
        writer.value_matrix = [
            [0,   0.1,      "hoge", True,   0,      "2017-01-01 03:04:05+0900"],
            [2,   "-2.23",  "foo",  False,  None,   "2017-12-23 45:01:23+0900"],
            [3,   0,        "bar",  "true",  "inf", "2017-03-03 33:44:55+0900"],
            [-10, -9.9,     "",     "FALSE", "nan", "2017-01-01 00:00:00+0900"],
        ]

        writer.write_table()

:Output:
    .. code-block:: json

        [
        {
            "bool": true,
            "float": 0.1,
            "int": 0,
            "mix": 0,
            "str": "hoge",
            "time": "2017-01-01 03:04:05+0900"
        },
        {
            "bool": false,
            "float": -2.23,
            "int": 2,
            "mix": null,
            "str": "foo",
            "time": "2017-12-23 12:34:51+0900"
        },
        {
            "bool": true,
            "float": 0,
            "int": 3,
            "mix": "Infinity",
            "str": "bar",
            "time": "2017-03-03 22:44:55+0900"
        },
        {
            "bool": false,
            "float": -9.9,
            "int": -10,
            "mix": "NaN",
            "str": "",
            "time": "2017-01-01 00:00:00+0900"
        }]


.. _example-jsonl-writer:

JSON lines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:Sample Code:
    .. code-block:: python
        :caption: JSON lines

        from pytablewriter import JsonLinesTableWriter

        writer = JsonLinesTableWriter()
        writer.header_list = ["int", "float", "str", "bool", "mix", "time"]
        writer.value_matrix = [
            [0,   0.1,      "hoge", True,   0,      "2017-01-01 03:04:05+0900"],
            [2,   "-2.23",  "foo",  False,  None,   "2017-12-23 45:01:23+0900"],
            [3,   0,        "bar",  "true",  "inf", "2017-03-03 33:44:55+0900"],
            [-10, -9.9,     "",     "FALSE", "nan", "2017-01-01 00:00:00+0900"],
        ]

        writer.write_table()

:Output:
    .. code-block:: json

        {"int": 0, "float": 0.1, "str": "hoge", "bool": "true", "mix": 0, "time": "2017-01-01 03:04:05+0900"}
        {"int": 2, "float": -2.23, "str": "foo", "bool": "false", "mix": "null", "time": "2017-12-23 45:01:23+0900"}
        {"int": 3, "float": 0, "str": "bar", "bool": "true", "mix": "Infinity", "time": "2017-03-03 33:44:55+0900"}
        {"int": -10, "float": -9.9, "str": "", "bool": "FALSE", "mix": "nan", "time": "2017-01-01 00:00:00+0900"}
