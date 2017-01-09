.. _example-type-hint-js:

JavaScript Code
-----------------------------

Reference: :py:attr:`AbstractTableWriter.type_hint_list`

.. code-block:: python
    :caption: Sample code that using type hint to change data type to write JavaScript code

    from datetime import datetime
    import pytablewriter as ptw

    writer = ptw.JavaScriptTableWriter()
    writer.header_list = ["float", "infnan", "string", "datetime"]
    writer.value_matrix = [
        [-1.1, float("inf"), "2017-01-02 03:04:05", datetime(2017, 1, 2, 3, 4, 5)],
        [0.12, float("nan"), "2017-02-03 04:05:06", datetime(2017, 2, 3, 4, 5, 6)],
    ]

    # column types will be detected automatically in default
    writer.table_name = "without type hint"
    writer.write_table()

    # set type hints
    writer.table_name = "with type hint"
    writer.type_hint_list = [ptw.IntegerType, ptw.StringType, ptw.DateTimeType, ptw.StringType]
    writer.write_table()


.. code-block:: javascript
    :caption: Output of JavaScript variable declaration code with/without type hints

    const without_type_hint = [
        ["float", "infnan", "string", "datetime"],
        [-1.10, Infinity, "2017-01-02 03:04:05", new Date("2017-01-02T03:04:05")],
        [0.12, NaN, "2017-02-03 04:05:06", new Date("2017-02-03T04:05:06")]
    ];
    const with_type_hint = [
        ["float", "infnan", "string", "datetime"],
        [-1, "inf", new Date("2017-01-02T03:04:05"), "2017-01-02 03:04:05"],
        [0, "nan", new Date("2017-02-03T04:05:06"), "2017-02-03 04:05:06"]
    ];
