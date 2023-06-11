.. _example-configure-stream:

Configure Output Stream
========================

Reference: :py:attr:`~AbstractTableWriter.stream`.

:Sample Code:
    .. code-block:: python
        :caption: Change the output stream of a writer object

        import io
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

            # writer instance writes a table to stdout by default
            writer.write_table()

            # change the stream to a string buffer to get the output as a string
            # you can also get the tabular text by using dumps method
            writer.stream = io.StringIO()
            writer.write_table()
            print(writer.stream.getvalue())

            # change the output stream to a file
            with open("sample.md", "w") as f:
                writer.stream = f
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

        # zone
        |zone_id|country_code|   zone_name    |
        |------:|------------|----------------|
        |      1|AD          |Europe/Andorra  |
        |      2|AE          |Asia/Dubai      |
        |      3|AF          |Asia/Kabul      |
        |      4|AG          |America/Antigua |
        |      5|AI          |America/Anguilla|
