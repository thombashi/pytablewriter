.. _example-type-hint-python:

Python Code
-----------------------------

You can specify type hints to a writer via 
:py:attr:`~AbstractTableWriter.type_hint_list`.

:Sample Code:
    .. code-block:: python
        :caption: Using type hint to change data type to write Python code

        from datetime import datetime
        import pytablewriter as ptw

        writer = ptw.PythonCodeTableWriter()
        writer.value_matrix = [
            [-1.1, float("inf"), "2017-01-02 03:04:05", datetime(2017, 1, 2, 3, 4, 5)],
            [0.12, float("nan"), "2017-02-03 04:05:06", datetime(2017, 2, 3, 4, 5, 6)],
        ]

        # column types will be detected automatically in default
        writer.table_name = "python variable without type hints"
        writer.header_list = ["float", "infnan", "string", "datetime"]
        writer.write_table()
        print()
        
        # set type hints
        writer.table_name = "python variable with type hints"
        writer.header_list = ["hint_int", "hint_str", "hint_datetime", "hint_str"]
        writer.type_hint_list = [ptw.Integer, ptw.String, ptw.DateTime, ptw.String]
        writer.write_table()


:Output:
    .. code-block:: python
        :caption: Python variable declaration code with/without type hints

        python_variable_without_type_hints = [
            ["float", "infnan", "string", "datetime"],
            [-1.10, float("inf"), "2017-01-02 03:04:05", dateutil.parser.parse("2017-01-02T03:04:05")],
            [0.12, float("nan"), "2017-02-03 04:05:06", dateutil.parser.parse("2017-02-03T04:05:06")],
        ]

        python_variable_with_type_hints = [
            ["hint_int", "hint_str", "hint_datetime", "hint_str"],
            [-1, "inf", dateutil.parser.parse("2017-01-02T03:04:05"), "2017-01-02 03:04:05"],
            [0, "nan", dateutil.parser.parse("2017-02-03T04:05:06"), "2017-02-03 04:05:06"],
        ]
