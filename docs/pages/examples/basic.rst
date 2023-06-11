Basic usage
--------------
Basic usage of the ``pytablewriter`` is as follows:

1. Create a writer instance that corresponds to the format you want to write
2. Assign a value to instance variables (such as |table_name|/|headers|/|value_matrix|) of the writer
3. Call the ``write_table`` method

The following example shows how to write a table in markdown format:

:Sample Code:
    .. code-block:: python
        :caption: Write a table

        import pytablewriter as ptw

        def main():
            writer = ptw.MarkdownTableWriter()
            writer.table_name = "zone"
            writer.headers = ["zone_id", "country_code", "zone_name"]
            writer.value_matrix = [
                ["1", "AD", "Europe/Andorra"],
                ["2", "AE", "Asia/Dubai"],
                ["3", "AF", "Asia/Kabul"],
                ["4", "AG", "America/Antigua"],
                ["5", "AI", "America/Anguilla"],
            ]

            writer.write_table()

        if __name__ == "__main__":
            main()

:Output:
    .. code-block:: none

        # zone
        |zone_id|country_code|   zone_name    |
        |------:|------------|----------------|
        |      1|AD          |Europe/Andorra  |
        |      2|AE          |Asia/Dubai      |
        |      3|AF          |Asia/Kabul      |
        |      4|AG          |America/Antigua |
        |      5|AI          |America/Anguilla|

The default output stream is the standard output for text format writers.
Binary format writers will write to a binary file opened by the ``open`` method.
