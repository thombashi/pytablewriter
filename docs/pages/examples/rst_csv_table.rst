.. _example-rst-csv-table-writer:

Write a reStructuredText CSV table
-------------------------------------------

|RstCsvTableWriter| the class can write a table 
with reStructuredText CSV table format to the |stream| from a matrix of data.

.. code-block:: python
    :caption: Sample code

    import pytablewriter

    writer = pytablewriter.RstCsvTableWriter()
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
    
    .. csv-table:: zone
        :header: "zone_id", "country_code", "zone_name"
        :widths: 7, 12, 16
        
        1, "AD", "Europe/Andorra"
        2, "AE", "Asia/Dubai"
        3, "AF", "Asia/Kabul"
        4, "AG", "America/Antigua"
        5, "AI", "America/Anguilla"


Rendering result
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. csv-table:: zone
    :header: "zone_id", "country_code", "zone_name"
    :widths: 7, 12, 16
    
    1, "AD", "Europe/Andorra"
    2, "AE", "Asia/Dubai"
    3, "AF", "Asia/Kabul"
    4, "AG", "America/Antigua"
    5, "AI", "America/Anguilla"
