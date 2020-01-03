.. _example-numpy-table-writer:

NumPy array
----------------------------
|NumpyTableWriter| class can write a variable definition of ``numpy.array`` to the |stream| from a matrix of data.

:Sample Code:
    .. code-block:: python
        :caption: Write a NumPy array definition

        import pytablewriter

        def main():
            writer = pytablewriter.NumpyTableWriter()
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
    .. code-block:: python

        example_table = np.array([
            ["int", "float", "str", "bool", "mix", "time"],
            [0, 0.1, "hoge", True, 0, "2017-01-01 03:04:05+0900"],
            [2, -2.23, "foo", False, None, "2017-12-23 12:34:51+0900"],
            [3, 0, "bar", True, np.inf, "2017-03-03 22:44:55+0900"],
            [-10, -9.9, "", False, np.nan, "2017-01-01 00:00:00+0900"],
        ])
