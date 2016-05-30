.. _example-pandas-dataframe-writer:

Write a Pandas DataFrame
----------------------------

|PandasDataFrameWriter| the class can write a variable definition of 
a Pandas DataFrame to the |stream| from a matrix of data.

.. code-block:: python
    :caption: Sample code

    import pytablewriter

    writer = pytablewriter.PandasDataFrameWriter()
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
    
    Timezone = pandas.DataFrame(
        {'country_code': ['AD', 'AE', 'AF', 'AG', 'AI'],
         'zone_id': [1, 2, 3, 4, 5],
         'zone_name': ['Europe/Andorra',
                       'Asia/Dubai',
                       'Asia/Kabul',
                       'America/Antigua',
                       'America/Anguilla']})
