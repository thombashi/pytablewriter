.. _example-ltsv-table-writer:

LTSV
----------------------------
|LtsvTableWriter| class can write a
`Labeled Tab-separated Values (LTSV) <http://ltsv.org/>`__
table to the |stream| from a data matrix.

:Sample Code:
    .. code-block:: python
        :caption: Write an LTSV table

        import pytablewriter

        def main():
            writer = pytablewriter.LtsvTableWriter()
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
    .. code-block:: none

        int:0	float:0.10	str:"hoge"	bool:True	mix:0	time:"2017-01-01 03:04:05+0900"
        int:2	float:-2.23	str:"foo"	bool:False	time:"2017-12-23 12:34:51+0900"
        int:3	float:0.00	str:"bar"	bool:True	mix:Infinity	time:"2017-03-03 22:44:55+0900"
        int:-10	float:-9.90	bool:False	mix:NaN	time:"2017-01-01 00:00:00+0900"
