.. _example-json-table-writer:

Write a JSON table
----------------------------

|JsonTableWriter| class can write a table to the |stream| with JSON format 
from a matrix of data.
JSON format will change if the |table_name| has a valid value or not.

With a table name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
    :caption: Sample code w/ table name

    import pytablewriter

    writer = pytablewriter.JsonTableWriter()
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


.. code-block:: json
    :caption: Output
    
    {
        "zone": [
            {
                "country_code": "AD",
                "zone_id": 1,
                "zone_name": "Europe/Andorra"
            },
            {
                "country_code": "AE",
                "zone_id": 2,
                "zone_name": "Asia/Dubai"
            },
            {
                "country_code": "AF",
                "zone_id": 3,
                "zone_name": "Asia/Kabul"
            },
            {
                "country_code": "AG",
                "zone_id": 4,
                "zone_name": "America/Antigua"
            },
            {
                "country_code": "AI",
                "zone_id": 5,
                "zone_name": "America/Anguilla"
            }
        ]
    }


Without a table name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python
    :caption: Sample code w/ table name

    import pytablewriter

    writer = pytablewriter.JsonTableWriter()
    writer.header_list = ["zone_id", "country_code", "zone_name"]
    writer.value_matrix = [
        ["1", "AD", "Europe/Andorra"],
        ["2", "AE", "Asia/Dubai"],
        ["3", "AF", "Asia/Kabul"],
        ["4", "AG", "America/Antigua"],
        ["5", "AI", "America/Anguilla"],
    ]
    
    writer.write_table()


.. code-block:: json
    :caption: Output
    
    [
        {
            "country_code": "AD",
            "zone_id": 1,
            "zone_name": "Europe/Andorra"
        },
        {
            "country_code": "AE",
            "zone_id": 2,
            "zone_name": "Asia/Dubai"
        },
        {
            "country_code": "AF",
            "zone_id": 3,
            "zone_name": "Asia/Kabul"
        },
        {
            "country_code": "AG",
            "zone_id": 4,
            "zone_name": "America/Antigua"
        },
        {
            "country_code": "AI",
            "zone_id": 5,
            "zone_name": "America/Anguilla"
        }
    ]
