.. _example-type-hint-js:

JavaScript Code
-----------------------------
You can specify type hints to a writer via 
:py:attr:`~AbstractTableWriter.type_hint_list`.

:Sample Code:
    .. code-block:: python
        :caption: Using type hint to change data type to write JavaScript code

        from datetime import datetime
        import pytablewriter as ptw

        writer = ptw.JavaScriptTableWriter()
        writer.header_list = ["header_a", "header_b", "header_c"]
        writer.value_matrix = [
            [-1.1, "2017-01-02 03:04:05", datetime(2017, 1, 2, 3, 4, 5)],
            [0.12, "2017-02-03 04:05:06", datetime(2017, 2, 3, 4, 5, 6)],
        ]

        print("// without type hints: column types will be detected automatically in default")
        writer.table_name = "without type hint"
        writer.write_table()
        print()

        print("// with type hints: Integer, DateTime, String")
        writer.table_name = "with type hint"
        writer.type_hint_list = [ptw.Integer, ptw.DateTime, ptw.String]
        writer.write_table()


:Output:
    .. code-block:: javascript
        :caption: JavaScript variable declaration code with/without type hints

        // without type hints: column types will be detected automatically in default
        const without_type_hint = [
            ["header_a", "header_b", "header_c"],
            [-1.10, "2017-01-02 03:04:05", new Date("2017-01-02T03:04:05")],
            [0.12, "2017-02-03 04:05:06", new Date("2017-02-03T04:05:06")]
        ];

        // with type hints: Integer, DateTime, String
        const with_type_hint = [
            ["header_a", "header_b", "header_c"],
            [-1, new Date("2017-01-02T03:04:05"), "2017-01-02 03:04:05"],
            [0, new Date("2017-02-03T04:05:06"), "2017-02-03 04:05:06"]
        ];
