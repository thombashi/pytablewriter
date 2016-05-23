.. _example-html-table-writer:

Write a HTML table
----------------------------

|HtmlTableWriter| class can write a table to a stream with 
``table`` tag format from a matrix of data.

.. code-block:: python
    :caption: Sample code

    import pytablewriter

    writer = pytablewriter.HtmlTableWriter()
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


.. code-block:: html
    :caption: Output
                
    <table id="zone">
      <caption>zone</caption>
      <thead>
        <tr>
          <th>zone_id</th>
          <th>country_code</th>
          <th>zone_name</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td align="right">1</td>
          <td align="left">AD</td>
          <td align="left">Europe/Andorra</td>
        </tr>
        <tr>
          <td align="right">2</td>
          <td align="left">AE</td>
          <td align="left">Asia/Dubai</td>
        </tr>
        <tr>
          <td align="right">3</td>
          <td align="left">AF</td>
          <td align="left">Asia/Kabul</td>
        </tr>
        <tr>
          <td align="right">4</td>
          <td align="left">AG</td>
          <td align="left">America/Antigua</td>
        </tr>
        <tr>
          <td align="right">5</td>
          <td align="left">AI</td>
          <td align="left">America/Anguilla</td>
        </tr>
      </tbody>
    </table>



Rendering result
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

    <table id="zone">
      <caption>zone</caption>
      <thead>
        <tr>
          <th>zone_id</th>
          <th>country_code</th>
          <th>zone_name</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td align="right">1</td>
          <td align="left">AD</td>
          <td align="left">Europe/Andorra</td>
        </tr>
        <tr>
          <td align="right">2</td>
          <td align="left">AE</td>
          <td align="left">Asia/Dubai</td>
        </tr>
        <tr>
          <td align="right">3</td>
          <td align="left">AF</td>
          <td align="left">Asia/Kabul</td>
        </tr>
        <tr>
          <td align="right">4</td>
          <td align="left">AG</td>
          <td align="left">America/Antigua</td>
        </tr>
        <tr>
          <td align="right">5</td>
          <td align="left">AI</td>
          <td align="left">America/Anguilla</td>
        </tr>
      </tbody>
    </table>
