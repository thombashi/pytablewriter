.. _example-python-code-table-writer:

Write a Python code table
----------------------------

|PythonCodeTableWriter| the class can write a variable definition of 
a Python nested list to the |stream| from a matrix of data.

.. code-block:: python
    :caption: Sample code that writes a Python code

    import pytablewriter

    writer = pytablewriter.PythonCodeTableWriter()
    writer.table_name = "example_table"
    writer.header_list = ["int", "float", "str", "bool", "mix", "time"]
    writer.value_matrix = [
        [0,   0.1,      "hoge", True,   0,      "2017-01-01 03:04:05+0900"],
        [2,   "-2.23",  "foo",  False,  None,   "2017-12-23 45:01:23+0900"],
        [3,   0,        "bar",  "true",  "inf", "2017-03-03 33:44:55+0900"],
        [-10, -9.9,     "",     "FALSE", "nan", "2017-01-01 00:00:00+0900"],
    ]
    
    writer.write_table()

.. code-block:: python
    :caption: Output of Python code

    example_table = [
        ["int", "float", "str", "bool", "mix", "time"],
        [0, 0.1, "hoge", True, 0, "2017-01-01 03:04:05+0900"],
        [2, -2.2, "foo", False, None, "2017-12-23 12:34:51+0900"],
        [3, 0.0, "bar", True, float("inf"), "2017-03-03 22:44:55+0900"],
        [-10, -9.9, "", False, float("nan"), "2017-01-01 00:00:00+0900"],
    ]


Write datetime as str
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Just add ``writer.is_datetime_instance_formatting = False`` to the example given above.

.. code-block:: python
    :caption: Sample code that writes a Python code w/ str-datetime

    import pytablewriter

    writer = pytablewriter.PythonCodeTableWriter()
    writer.table_name = "example_table"
    writer.header_list = ["int", "float", "str", "bool", "mix", "time"]
    writer.value_matrix = [
        [0,   0.1,      "hoge", True,   0,      "2017-01-01 03:04:05+0900"],
        [2,   "-2.23",  "foo",  False,  None,   "2017-12-23 45:01:23+0900"],
        [3,   0,        "bar",  "true",  "inf", "2017-03-03 33:44:55+0900"],
        [-10, -9.9,     "",     "FALSE", "nan", "2017-01-01 00:00:00+0900"],
    ]
    writer.is_datetime_instance_formatting = False  # add this line
    
    writer.write_table()

.. code-block:: python

    example_table = [
        ["int", "float", "str", "bool", "mix", "time"],
        [0, 0.1, "hoge", True, 0, "2017-01-01 03:04:05+0900"],
        [2, -2.2, "foo", False, None, "2017-12-23 12:34:51+0900"],
        [3, 0.0, "bar", True, float("inf"), "2017-03-03 22:44:55+0900"],
        [-10, -9.9, "", False, float("nan"), "2017-01-01 00:00:00+0900"],
    ]
