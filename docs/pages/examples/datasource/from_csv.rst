.. _example-from-csv:

Using CSV as tabular data source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from CSV text
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Sample Code:
    .. code-block:: python
        :caption: Write a table from CSV text

        import pytablewriter

        csv_data = u""""i","f","c","if","ifc","bool","inf","nan","mix_num","time"
        1,1.10,"aa",1.0,"1",True,Infinity,NaN,1,"2017-01-01 00:00:00+09:00"
        2,2.20,"bbb",2.2,"2.2",False,Infinity,NaN,Infinity,"2017-01-02 03:04:05+09:00"
        3,3.33,"cccc",-3.0,"ccc",True,Infinity,NaN,NaN,"2017-01-01 00:00:00+09:00"
        """

        writer = pytablewriter.RstGridTableWriter()
        writer.from_csv(csv_data)
        writer.write_table()


:Output:
    .. code-block:: ReST

        .. table:: csv1

            +-+----+----+----+---+-----+--------+---+--------+-------------------------+
            |i| f  | c  | if |ifc|bool |  inf   |nan|mix_num |          time           |
            +=+====+====+====+===+=====+========+===+========+=========================+
            |1|1.10|aa  | 1.0|1  |True |Infinity|NaN|       1|2017-01-01 00:00:00+09:00|
            +-+----+----+----+---+-----+--------+---+--------+-------------------------+
            |2|2.20|bbb | 2.2|2.2|False|Infinity|NaN|Infinity|2017-01-02 03:04:05+09:00|
            +-+----+----+----+---+-----+--------+---+--------+-------------------------+
            |3|3.33|cccc|-3.0|ccc|True |Infinity|NaN|     NaN|2017-01-01 00:00:00+09:00|
            +-+----+----+----+---+-----+--------+---+--------+-------------------------+


from a CSV file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:Sample Code:
    .. code-block:: python
        :caption: Write a table from a CSV file

        import io
        import pytablewriter

        filename = "sample.csv"
        csv_data = u""""i","f","c","if","ifc","bool","inf","nan","mix_num","time"
        1,1.10,"aa",1.0,"1",True,Infinity,NaN,1,"2017-01-01 00:00:00+09:00"
        2,2.20,"bbb",2.2,"2.2",False,Infinity,NaN,Infinity,"2017-01-02 03:04:05+09:00"
        3,3.33,"cccc",-3.0,"ccc",True,Infinity,NaN,NaN,"2017-01-01 00:00:00+09:00"
        """

        with io.open(filename, "w", encoding="utf8") as f:
            f.write(csv_data)

        writer = pytablewriter.RstGridTableWriter()
        writer.from_csv(filename)
        writer.write_table()
