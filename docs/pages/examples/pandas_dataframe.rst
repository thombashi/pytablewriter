.. _example-pandas-dataframe-writer:

Write a Pandas DataFrame
----------------------------

|PandasDataFrameWriter| the class can write a variable definition of Pandas DataFrame to the |stream| from a matrix of data.

.. code-block:: python
    :caption: Sample code that writes a Pandas DataFrame definition

    import pytablewriter

    writer = pytablewriter.PandasDataFrameWriter()
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
    :caption: Output of DataFrame definition

    example_table = pandas.DataFrame(
        {'bool': [True, False, True, False],
         'float': [0.1, -2.23, 0, -9.9],
         'int': [0, 2, 3, -10],
         'mix': [0, None, numpy.inf, numpy.nan],
         'str': ['hoge', 'foo', 'bar', ''],
         'time': ['2017-01-01 03:04:05+0900',
                  '2017-12-23 12:34:51+0900',
                  '2017-03-03 22:44:55+0900',
                  '2017-01-01 00:00:00+0900']})
