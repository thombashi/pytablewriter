.. _example-type-hint:

Configure Writing Data Type
-----------------------------------

Reference: :py:attr:`AbstractTableWriter.type_hint_list`

.. code-block:: python
    :caption: Sample code that using type hint to change writing data type

    from datetime import datetime
    import pytablewriter as ptw

    writer = ptw.JavaScriptTableWriter()
    writer.header_list = ["int", "string", "datetime"]
    writer.value_matrix = [
        [-1.1, "2017-01-02 03:04:05", datetime(2017, 1, 2, 3, 4, 5)],
        [0.12, "2017-02-03 04:05:06", datetime(2017, 2, 3, 4, 5, 6)],
    ]

    # column types will be detected automatically in default
    writer.table_name = "without type hint"
    writer.write_table()

    # set type hints
    writer.table_name = "with type hint"
    writer.type_hint_list = [ptw.IntegerType, ptw.DateTimeType, ptw.StringType]
    writer.write_table()


.. code-block:: none
    :caption: Output of with/without type hints

    const without_type_hint = [
        ["int", "string", "datetime"],
        [-1.10, "2017-01-02 03:04:05", new Date("2017-01-02T03:04:05")],
        [0.12, "2017-02-03 04:05:06", new Date("2017-02-03T04:05:06")]
    ];
    const with_type_hint = [
        ["int", "string", "datetime"],
        [-1, new Date("2017-01-02T03:04:05"), "2017-01-02 03:04:05"],
        [0, new Date("2017-02-03T04:05:06"), "2017-02-03 04:05:06"]
    ];
