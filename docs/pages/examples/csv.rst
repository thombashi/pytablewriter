.. _example-csv-table-writer:

Write a CSV table
----------------------------

|CsvTableWriter| class can write a table to the |stream| from a matrix of data.

.. code-block:: python
    :caption: Sample code

    import pytablewriter

    writer = pytablewriter.CsvTableWriter()
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
        
    1,"AD","Europe/Andorra"
    2,"AE","Asia/Dubai"
    3,"AF","Asia/Kabul"
    4,"AG","America/Antigua"
    5,"AI","America/Anguilla"
