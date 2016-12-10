Basic usage
--------------

Basic usage of the ``pytablewriter`` is as follows:

1. Create a writer instance that corresponds to the format you want to write
2. Assign a value to instance variables (such as |table_name|/|header_list|/|value_matrix|) of the writer
3. Call the ``write_table`` method

Next examples show how to write a table to the standard output/file with reStructuredText format.

Write a table to the standard output (defaults)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The standard output is the default output stream of writers
(except the |ExcelXlsxTableWriter|).

.. code-block:: python
    :caption: Sample code that writes a table to stdout

    import pytablewriter

    writer = pytablewriter.RstGridTableWriter()
    writer.table_name = "zone"
    writer.header_list = ["zone_id", "country_code", "zone_name"]
    writer.value_matrix = [
        ["1", "AD", "Europe/Andorra"],
        ["2", "AE", "Asia/Dubai"],
        ["3", "AF", "Asia/Kabul"],
        ["4", "AG", "America/Antigua"],
        ["5", "AI", "America/Anguilla"],
    ]
    
    writer.write_table()


.. code-block:: none
    :caption: Output
    
    .. table:: zone

        +-------+------------+----------------+
        |zone_id|country_code|   zone_name    |
        +=======+============+================+
        |      1|AD          |Europe/Andorra  |
        +-------+------------+----------------+
        |      2|AE          |Asia/Dubai      |
        +-------+------------+----------------+
        |      3|AF          |Asia/Kabul      |
        +-------+------------+----------------+
        |      4|AG          |America/Antigua |
        +-------+------------+----------------+
        |      5|AI          |America/Anguilla|
        +-------+------------+----------------+


Write a table to a file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can change the output stream if you set the |stream| attribute of a writer.
This example will write a table to a ``sample.rst`` file.

.. code-block:: python
    :caption: Sample code that writes a table to a file

    import six
    import pytablewriter

    filename = "sample.rst"

    writer = pytablewriter.RstGridTableWriter()
    writer.table_name = "zone"
    writer.header_list = ["zone_id", "country_code", "zone_name"]
    writer.value_matrix = [
        ["1", "AD", "Europe/Andorra"],
        ["2", "AE", "Asia/Dubai"],
        ["3", "AF", "Asia/Kabul"],
        ["4", "AG", "America/Antigua"],
        ["5", "AI", "America/Anguilla"],
    ]

    # change output stream
    with open(filename, "w") as f:
        writer.stream = f
        writer.write_table()

    # output the result to the standard output
    with open(filename) as f:
        six.print_(f.read())


.. code-block:: none
    :caption: Output

    .. table:: zone

        +-------+------------+----------------+
        |zone_id|country_code|   zone_name    |
        +=======+============+================+
        |      1|AD          |Europe/Andorra  |
        +-------+------------+----------------+
        |      2|AE          |Asia/Dubai      |
        +-------+------------+----------------+
        |      3|AF          |Asia/Kabul      |
        +-------+------------+----------------+
        |      4|AG          |America/Antigua |
        +-------+------------+----------------+
        |      5|AI          |America/Anguilla|
        +-------+------------+----------------+
