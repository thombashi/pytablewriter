.. _example-python-code-table-writer:

Write a Python code table
----------------------------

|PythonCodeTableWriter| the class can write a variable definition of 
a Python nested list to the |stream| from a matrix of data.

.. code-block:: python
    :caption: Sample code

    import pytablewriter

    writer = pytablewriter.PythonCodeTableWriter()
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


.. code-block:: python
    :caption: Output
        
    zone = [
        ["zone_id", "country_code", "zone_name"],
        [1, "AD", "Europe/Andorra"],
        [2, "AE", "Asia/Dubai"],
        [3, "AF", "Asia/Kabul"],
        [4, "AG", "America/Antigua"],
        [5, "AI", "America/Anguilla"],
    ]
