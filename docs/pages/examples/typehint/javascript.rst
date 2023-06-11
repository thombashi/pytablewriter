.. _example-type-hint-js:

Type Hint: JavaScript Code
-----------------------------
You can specify type hints to a writer via
:py:attr:`~AbstractTableWriter.type_hints`.

:Sample Code:
    .. code-block:: python
        :caption: Using type hint to change the data type to write JavaScript code

        from datetime import datetime
        from pytablewriter import JavaScriptTableWriter

        def main():
            writer = JavaScriptTableWriter()
            writer.headers = ["header_a", "header_b", "header_c"]
            writer.value_matrix = [
                [-1.1, "2017-01-02 03:04:05", datetime(2017, 1, 2, 3, 4, 5)],
                [0.12, "2017-02-03 04:05:06", datetime(2017, 2, 3, 4, 5, 6)],
            ]

            print("// without type hints: column data types are detected automatically by default")
            writer.table_name = "without type hint"
            writer.write_table()

            print("// with type hints: values will be converted with type hints if possible")
            writer.table_name = "with type hint"
            writer.type_hints = ["int", "datetime", "str"]
            writer.write_table()

        if __name__ == "__main__":
            main()

:Output:
    .. code-block:: javascript
        :caption: JavaScript variable declaration code with/without type hints

        // without type hints: column data types are detected automatically by default
        const without_type_hint = [
            ["header_a", "header_b", "header_c"],
            [-1.1, "2017-01-02 03:04:05", new Date("2017-01-02T03:04:05")],
            [0.12, "2017-02-03 04:05:06", new Date("2017-02-03T04:05:06")]
        ];

        // with type hints: values will be converted with type hints if possible
        const with_type_hint = [
            ["header_a", "header_b", "header_c"],
            [-1, new Date("2017-01-02T03:04:05"), "2017-01-02 03:04:05"],
            [0, new Date("2017-02-03T04:05:06"), "2017-02-03 04:05:06"]
        ];
