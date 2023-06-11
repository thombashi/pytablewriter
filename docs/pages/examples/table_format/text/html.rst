.. _example-html-table-writer:

HTML
----------------------------
|HtmlTableWriter| class can write a table to a stream with
``table`` tag format from a data matrix.

:Sample Code:
    .. code-block:: python
        :caption: Write an HTML table

        import pytablewriter

        def main():
            writer = pytablewriter.HtmlTableWriter()
            writer.table_name = "example_table"
            writer.headers = ["int", "float", "str", "bool", "mix", "time"]
            writer.value_matrix = [
                [0,   0.1,      "hoge", True,   0,      "2017-01-01 03:04:05+0900"],
                [2,   "-2.23",  "foo",  False,  None,   "2017-12-23 45:01:23+0900"],
                [3,   0,        "bar",  "true",  "inf", "2017-03-03 33:44:55+0900"],
                [-10, -9.9,     "",     "FALSE", "nan", "2017-01-01 00:00:00+0900"],
            ]

            writer.write_table()

        if __name__ == "__main__":
            main()

:Output:
    .. code-block:: html

        <table id="example_table">
            <caption>example_table</caption>
            <thead>
                <tr>
                    <th>int</th>
                    <th>float</th>
                    <th>str</th>
                    <th>bool</th>
                    <th>mix</th>
                    <th>time</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td align="right">0</td>
                    <td align="right">0.10</td>
                    <td align="left">hoge</td>
                    <td align="left">True</td>
                    <td align="right">0</td>
                    <td align="left">2017-01-01 03:04:05+0900</td>
                </tr>
                <tr>
                    <td align="right">2</td>
                    <td align="right">-2.23</td>
                    <td align="left">foo</td>
                    <td align="left">False</td>
                    <td align="left"></td>
                    <td align="left">2017-12-23 12:34:51+0900</td>
                </tr>
                <tr>
                    <td align="right">3</td>
                    <td align="right">0.00</td>
                    <td align="left">bar</td>
                    <td align="left">True</td>
                    <td align="left">Infinity</td>
                    <td align="left">2017-03-03 22:44:55+0900</td>
                </tr>
                <tr>
                    <td align="right">-10</td>
                    <td align="right">-9.90</td>
                    <td align="left"></td>
                    <td align="left">False</td>
                    <td align="left">NaN</td>
                    <td align="left">2017-01-01 00:00:00+0900</td>
                </tr>
            </tbody>
        </table>

:Rendering Result:
    .. raw:: html

        <table id="example_table">
            <caption>example_table</caption>
            <thead>
                <tr>
                    <th>int</th>
                    <th>float</th>
                    <th>str</th>
                    <th>bool</th>
                    <th>mix</th>
                    <th>time</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td align="right">0</td>
                    <td align="right">0.1</td>
                    <td align="left">hoge</td>
                    <td align="left">True</td>
                    <td align="right">0</td>
                    <td align="left">2017-01-01 03:04:05+0900</td>
                </tr>
                <tr>
                    <td align="right">2</td>
                    <td align="right">-2.2</td>
                    <td align="left">foo</td>
                    <td align="left">False</td>
                    <td align="left"></td>
                    <td align="left">2017-12-23 12:34:51+0900</td>
                </tr>
                <tr>
                    <td align="right">3</td>
                    <td align="right">0.0</td>
                    <td align="left">bar</td>
                    <td align="left">True</td>
                    <td align="left">inf</td>
                    <td align="left">2017-03-03 22:44:55+0900</td>
                </tr>
                <tr>
                    <td align="right">-10</td>
                    <td align="right">-9.9</td>
                    <td align="left"></td>
                    <td align="left">False</td>
                    <td align="left">nan</td>
                    <td align="left">2017-01-01 00:00:00+0900</td>
                </tr>
            </tbody>
        </table>
