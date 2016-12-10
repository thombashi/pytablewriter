.. _example-rst-csv-table-writer:

Write a reStructuredText CSV table
-------------------------------------------

|RstCsvTableWriter| the class can writes a table 
with reStructuredText CSV table format to the |stream| from a matrix of data.

.. code-block:: python
    :caption: Sample code that write a reStructuredText CSV table

    import pytablewriter

    writer = pytablewriter.RstCsvTableWriter()
    writer.table_name = "example_table"
    writer.header_list = ["int", "float", "str", "bool", "mix", "time"]
    writer.value_matrix = [
        [0,   0.1,      "hoge", True,   0,      "2017-01-01 03:04:05+0900"],
        [2,   "-2.23",  "foo",  False,  None,   "2017-12-23 45:01:23+0900"],
        [3,   0,        "bar",  "true",  "inf", "2017-03-03 33:44:55+0900"],
        [-10, -9.9,     "",     "FALSE", "nan", "2017-01-01 00:00:00+0900"],
    ]
    
    writer.write_table()


.. code-block:: none
    :caption: Output of reStructuredText CSV table

    .. csv-table:: example_table
        :header: "int", "float", "str", "bool", "mix", "time"
        :widths: 3, 5, 4, 5, 3, 24
        
        0, 0.1, "hoge", True, 0, "2017-01-01 03:04:05+0900"
        2, -2.2, "foo", False, , "2017-12-23 12:34:51+0900"
        3, 0.0, "bar", True, inf, "2017-03-03 22:44:55+0900"
        -10, -9.9, "", False, nan, "2017-01-01 00:00:00+0900"


Rendering result
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. csv-table:: example_table
    :header: "int", "float", "str", "bool", "mix", "time"
    :widths: 3, 5, 4, 5, 3, 24
    
    0, 0.1, "hoge", True, 0, "2017-01-01 03:04:05+0900"
    2, -2.2, "foo", False, , "2017-12-23 12:34:51+0900"
    3, 0.0, "bar", True, inf, "2017-03-03 22:44:55+0900"
    -10, -9.9, "", False, nan, "2017-01-01 00:00:00+0900"
