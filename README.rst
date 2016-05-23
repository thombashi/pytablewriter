pytablewriter
=============

.. image:: https://img.shields.io/pypi/pyversions/pytablewriter.svg
   :target: https://pypi.python.org/pypi/pytablewriter
.. image:: https://travis-ci.org/thombashi/pytablewriter.svg?branch=master
    :target: https://travis-ci.org/thombashi/pytablewriter
.. image:: https://coveralls.io/repos/github/thombashi/pytablewriter/badge.svg?branch=master
    :target: https://coveralls.io/github/thombashi/pytablewriter?branch=master

Summary
-------

pytablewriter is a python library to write a table in various formats: CSV/HTML/JavaScript/JSON/Markdown/Excel/Pandas/Python/reStructuredText

Examples
========

Write a Markdown table
----------------------------

.. code:: python

    import pytablewriter

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

    writer.write_table()

.. code::

    # zone
    zone_id|country_code|   zone_name
    ------:|------------|----------------
          1|AD          |Europe/Andorra
          2|AE          |Asia/Dubai
          3|AF          |Asia/Kabul
          4|AG          |America/Antigua
          5|AI          |America/Anguilla


Rendering result
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: ss/markdown.png
   :scale: 80%
   :alt: markdown_ss

   Rendered markdown at GitHub

Write a JavaScript table (variable definition of nested list )
----------------------------------------------------------------

.. code:: python

    import pytablewriter

    writer = pytablewriter.JavaScriptTableWriter()
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

.. code:: js

    var zone = [
        ["zone_id", "country_code", "zone_name"],
        [1, "AD", "Europe/Andorra"],
        [2, "AE", "Asia/Dubai"],
        [3, "AF", "Asia/Kabul"],
        [4, "AG", "America/Antigua"],
        [5, "AI", "America/Anguilla"]
    ];

Write an Excel table
----------------------------

.. code:: python

    import pytablewriter

    writer = pytablewriter.ExcelTableWriter()
    writer.open_workbook("sample_single.xlsx")

    writer.make_worksheet("zone")
    writer.header_list = ["zone_id", "country_code", "zone_name"]
    writer.value_matrix = [
        ["1", "AD", "Europe/Andorra"],
        ["2", "AE", "Asia/Dubai"],
        ["3", "AF", "Asia/Kabul"],
        ["4", "AG", "America/Antigua"],
        ["5", "AI", "America/Anguilla"],
    ]
    writer.write_table()

    writer.close()

Output
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: ss/excel_single.png
   :scale: 100%
   :alt: excel_single

   Output excel file (``sample_single.xlsx``)

For more information
--------------------
More examples are available at 
http://pytablewriter.readthedocs.org/en/latest/pages/examples/index.html


Installation
============

::

    pip install pytablewriter


Dependencies
============

Python 2.6+ or 3.3+

- `DataPropery <https://github.com/thombashi/DataProperty>`__
- `dominate <http://github.com/Knio/dominate/>`__
- `pathvalidate <https://github.com/thombashi/pathvalidate>`__
- `six <https://pypi.python.org/pypi/six/>`__
- `XlsxWriter <http://xlsxwriter.readthedocs.io/>`__


Test dependencies
-----------------

- `pytest <http://pytest.org/latest/>`__
- `pytest-runner <https://pypi.python.org/pypi/pytest-runner>`__
- `SimpleSQLite <https://github.com/thombashi/SimpleSQLite>`__
- `tox <https://testrun.org/tox/latest/>`__

Documentation
=============

http://pytablewriter.readthedocs.org/en/latest/

