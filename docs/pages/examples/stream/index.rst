.. _example-configure-stream:

Configure Output Stream
========================

Reference: :py:attr:`~AbstractTableWriter.stream`.

:Sample Code:
    .. code-block:: python
        :caption: Change output stream of a writer object

        import pytablewriter
        import six

        writer = pytablewriter.MarkdownTableWriter()
        writer.table_name = "zone"
        writer.header_list = ["zone_id", "country_code", "zone_name"]
        writer.value_matrix = [
            ["1", "AD", "Europe/Andorra"],
            ["2", "AE", "Asia/Dubai"],
            ["3", "AF", "Asia/Kabul"],
            ["4", "AG", "America/Antigua"],
            ["5", "AI", "America/Anguilla"],
        ]

        # writer instance will write a table to stdout in default
        writer.write_table()

        # change stream to string buffer to get output as a string
        writer.stream = six.StringIO()
        writer.write_table()
        print()
        print(writer.stream.getvalue())

        # change output stream to a file
        with open("sample.md", "w") as f:
            writer.stream = f
            writer.write_table()


:Output:
    .. code-block:: none

        # zone
        zone_id|country_code|   zone_name
        ------:|------------|----------------
              1|AD          |Europe/Andorra
              2|AE          |Asia/Dubai
              3|AF          |Asia/Kabul
              4|AG          |America/Antigua
              5|AI          |America/Anguilla

        # zone
        zone_id|country_code|   zone_name
        ------:|------------|----------------
              1|AD          |Europe/Andorra
              2|AE          |Asia/Dubai
              3|AF          |Asia/Kabul
              4|AG          |America/Antigua
              5|AI          |America/Anguilla
