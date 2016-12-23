pytablewriter
=============

.. image:: https://badge.fury.io/py/pytablewriter.svg
    :target: https://badge.fury.io/py/pytablewriter

.. image:: https://img.shields.io/pypi/pyversions/pytablewriter.svg
   :target: https://pypi.python.org/pypi/pytablewriter

.. image:: https://img.shields.io/travis/thombashi/pytablewriter/master.svg?label=Linux
    :target: https://travis-ci.org/thombashi/pytablewriter

.. image:: https://img.shields.io/appveyor/ci/thombashi/pytablewriter/master.svg?label=Windows
    :target: https://ci.appveyor.com/project/thombashi/pytablewriter

.. image:: https://coveralls.io/repos/github/thombashi/pytablewriter/badge.svg?branch=master
    :target: https://coveralls.io/github/thombashi/pytablewriter?branch=master

Summary
-------

pytablewriter is a python library to write a table in various formats: CSV/HTML/JavaScript/JSON/LTSV/Markdown/MediaWiki/Excel/Pandas/Python/reStructuredText/TSV.

Features
--------

- Write a table in various formats:
    - CSV
    - Microsoft Excel :superscript:`TM`
        - `.xlsx` format
        - `.xls` format
    - HTML
    - JSON
    - `Labeled Tab-separated Values (LTSV) <http://ltsv.org/>`__
    - Markdown
    - MediaWiki
    - Source code
        - `Pandas <http://pandas.pydata.org/>`__ (Definition of a DataFrame variable)
        - Python code (Definition of a nested list variable)
        - JavaScript (Definition of a nested list variable)
    - reStructuredText
        - Grid tables
        - Simple tables
        - CSV table
    - Tab-separated values (TSV)
- Automatic tabular data formatting
    - Alignment
    - Padding
    - Decimal places of numbers
- Multibyte character support
- Output table to a stream such as a file or the standard output

Examples
========

Write a Markdown table
----------------------

.. code:: python

    import pytablewriter

    writer = pytablewriter.MarkdownTableWriter()
    writer.table_name = "example_table"
    writer.header_list = ["int", "float", "str", "bool", "mix", "time"]
    writer.value_matrix = [
        [0,   0.1,      "hoge", True,   0,      "2017-01-01 03:04:05+0900"],
        [2,   "-2.23",  "foo",  False,  None,   "2017-12-23 45:01:23+0900"],
        [3,   0,        "bar",  "true",  "inf", "2017-03-03 33:44:55+0900"],
        [-10, -9.9,     "",     "FALSE", "nan", "2017-01-01 00:00:00+0900"],
    ]

    writer.write_table()

.. code::

    # example_table
    int|float|str |bool |mix|          time
    --:|----:|----|-----|--:|------------------------
      0|  0.1|hoge|True |  0|2017-01-01 03:04:05+0900
      2| -2.2|foo |False|   |2017-12-23 12:34:51+0900
      3|  0.0|bar |True |inf|2017-03-03 22:44:55+0900
    -10| -9.9|    |False|nan|2017-01-01 00:00:00+0900


Rendering result
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: ss/markdown.png
   :scale: 80%
   :alt: markdown_ss

   Rendered markdown at GitHub

Write a reStructuredText table (grid tables)
--------------------------------------------


.. code:: python

    import pytablewriter

    writer = pytablewriter.RstGridTableWriter()
    writer.table_name = "example_table"
    writer.header_list = ["int", "float", "str", "bool", "mix", "time"]
    writer.value_matrix = [
        [0,   0.1,      "hoge", True,   0,      "2017-01-01 03:04:05+0900"],
        [2,   "-2.23",  "foo",  False,  None,   "2017-12-23 45:01:23+0900"],
        [3,   0,        "bar",  "true",  "inf", "2017-03-03 33:44:55+0900"],
        [-10, -9.9,     "",     "FALSE", "nan", "2017-01-01 00:00:00+0900"],
    ]

    writer.write_table()


.. code::

    .. table:: example_table

        +---+-----+----+-----+--------+------------------------+
        |int|float|str |bool |  mix   |          time          |
        +===+=====+====+=====+========+========================+
        |  0| 0.10|hoge|True |       0|2017-01-01 03:04:05+0900|
        +---+-----+----+-----+--------+------------------------+
        |  2|-2.23|foo |False|        |2017-12-23 12:34:51+0900|
        +---+-----+----+-----+--------+------------------------+
        |  3| 0.00|bar |True |Infinity|2017-03-03 22:44:55+0900|
        +---+-----+----+-----+--------+------------------------+
        |-10|-9.90|    |False|     NaN|2017-01-01 00:00:00+0900|
        +---+-----+----+-----+--------+------------------------+

Rendering result
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. table:: example_table

    +---+-----+----+-----+--------+------------------------+
    |int|float|str |bool |  mix   |          time          |
    +===+=====+====+=====+========+========================+
    |  0| 0.10|hoge|True |       0|2017-01-01 03:04:05+0900|
    +---+-----+----+-----+--------+------------------------+
    |  2|-2.23|foo |False|        |2017-12-23 12:34:51+0900|
    +---+-----+----+-----+--------+------------------------+
    |  3| 0.00|bar |True |Infinity|2017-03-03 22:44:55+0900|
    +---+-----+----+-----+--------+------------------------+
    |-10|-9.90|    |False|     NaN|2017-01-01 00:00:00+0900|
    +---+-----+----+-----+--------+------------------------+

Write a JavaScript table (variable definition of nested list)
-------------------------------------------------------------

.. code:: python

    import pytablewriter

    writer = pytablewriter.JavaScriptTableWriter()
    writer.table_name = "example_table"
    writer.header_list = ["int", "float", "str", "bool", "mix", "time"]
    writer.value_matrix = [
        [0,   0.1,      "hoge", True,   0,      "2017-01-01 03:04:05+0900"],
        [2,   "-2.23",  "foo",  False,  None,   "2017-12-23 45:01:23+0900"],
        [3,   0,        "bar",  "true",  "inf", "2017-03-03 33:44:55+0900"],
        [-10, -9.9,     "",     "FALSE", "nan", "2017-01-01 00:00:00+0900"],
    ]

    writer.write_table()

.. code:: js

    var example_table = [
        ["int", "float", "str", "bool", "mix", "time"],
        [0, 0.10, "hoge", true, 0, new Date("2017-01-01T03:04:05+0900")],
        [2, -2.23, "foo", false, null, new Date("2017-12-23T12:34:51+0900")],
        [3, 0.00, "bar", true, Infinity, new Date("2017-03-03T22:44:55+0900")],
        [-10, -9.90, "", false, NaN, new Date("2017-01-01T00:00:00+0900")]
    ];

Write a table to an Excel sheet
-------------------------------

.. code:: python

    import pytablewriter

    writer = pytablewriter.ExcelXlsxTableWriter()
    writer.open_workbook("sample.xlsx")

    writer.make_worksheet("example")
    writer.header_list = ["int", "float", "str", "bool", "mix", "time"]
    writer.value_matrix = [
        [0,   0.1,      "hoge", True,   0,      "2017-01-01 03:04:05+0900"],
        [2,   "-2.23",  "foo",  False,  None,   "2017-12-23 12:34:51+0900"],
        [3,   0,        "bar",  "true",  "inf", "2017-03-03 22:44:55+0900"],
        [-10, -9.9,     "",     "FALSE", "nan", "2017-01-01 00:00:00+0900"],
    ]
    writer.write_table()

    writer.close()


Output of Excel book
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. figure:: ss/excel_single.png
   :scale: 100%
   :alt: excel_single

   Output excel file (``sample_single.xlsx``)

Write a table with multibyte character
--------------------------------------

﻿You can use multibyte character as table data.

.. code:: python

    import pytablewriter

    writer = pytablewriter.RstSimpleTableWriter()
    writer.table_name = "生成に関するパターン"
    writer.header_list = ["パターン名", "概要", "GoF", "Code Complete[1]"]
    writer.value_matrix = [
        ["Abstract Factory", "関連する一連のインスタンスを状況に応じて、適切に生成する方法を提供する。", "Yes", "Yes"],
        ["Builder", "複合化されたインスタンスの生成過程を隠蔽する。", "Yes", "No"],
        ["Factory Method", "実際に生成されるインスタンスに依存しない、インスタンスの生成方法を提供する。", "Yes", "Yes"],
        ["Prototype", "同様のインスタンスを生成するために、原型のインスタンスを複製する。", "Yes", "No"],
        ["Singleton", "あるクラスについて、インスタンスが単一であることを保証する。", "Yes", "Yes"],
    ]
    writer.write_table()


.. figure:: ss/multi_byte_char.png
   :scale: 100%
   :alt: multi_byte_char_table

   Output of multi-byte character table


Rendering result
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. table:: 生成に関するパターン

    ================  ============================================================================  ===  ================
       パターン名                                         概要                                      GoF  Code Complete[1]
    ================  ============================================================================  ===  ================
    Abstract Factory  関連する一連のインスタンスを状況に応じて、適切に生成する方法を提供する。      Yes  Yes
    Builder           複合化されたインスタンスの生成過程を隠蔽する。                                Yes  No
    Factory Method    実際に生成されるインスタンスに依存しない、インスタンスの生成方法を提供する。  Yes  Yes
    Prototype         同様のインスタンスを生成するために、原型のインスタンスを複製する。            Yes  No
    Singleton         あるクラスについて、インスタンスが単一であることを保証する。                  Yes  Yes
    ================  ============================================================================  ===  ================



Write a table from pandas DataFrame
-----------------------------------


.. code:: python

    import pandas as pd
    import pytablewriter
    from StringIO import StringIO

    csv_data = StringIO(u""""i","f","c","if","ifc","bool","inf","nan","mix_num","time"
    1,1.10,"aa",1.0,"1",True,Infinity,NaN,1,"2017-01-01 00:00:00+09:00"
    2,2.20,"bbb",2.2,"2.2",False,Infinity,NaN,Infinity,"2017-01-02 03:04:05+09:00"
    3,3.33,"cccc",-3.0,"ccc",True,Infinity,NaN,NaN,"2017-01-01 00:00:00+09:00"
    """)
    df = pd.read_csv(csv_data, sep=',')

    writer = pytablewriter.MarkdownTableWriter()
    writer.from_dataframe(df)
    writer.write_table()


.. code::

     i | f  | c  | if |ifc|bool |  inf   |nan|mix_num |          time
    --:|---:|----|---:|---|-----|--------|---|-------:|-------------------------
      1|1.10|aa  | 1.0|1  |True |Infinity|NaN|       1|2017-01-01 00:00:00+09:00
      2|2.20|bbb | 2.2|2.2|False|Infinity|NaN|Infinity|2017-01-02 03:04:05+09:00
      3|3.33|cccc|-3.0|ccc|True |Infinity|NaN|     NaN|2017-01-01 00:00:00+09:00

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

Python 2.7+ or 3.3+

- `DataPropery <https://github.com/thombashi/DataProperty>`__
- `dominate <http://github.com/Knio/dominate/>`__
- `mbstrdecoder <https://github.com/thombashi/mbstrdecoder>`__
- `pathvalidate <https://github.com/thombashi/pathvalidate>`__
- `six <https://pypi.python.org/pypi/six/>`__
- `XlsxWriter <http://xlsxwriter.readthedocs.io/>`__
- `xlwt <http://www.python-excel.org/>`__


Test dependencies
-----------------

- `pytablereader <https://github.com/thombashi/pytablereader>`__
- `pytest <http://pytest.org/latest/>`__
- `pytest-runner <https://pypi.python.org/pypi/pytest-runner>`__
- `tox <https://testrun.org/tox/latest/>`__

Documentation
=============

http://pytablewriter.readthedocs.org/en/latest/

Related Project
===============

- `pytablereader <https://github.com/thombashi/pytablereader>`__
    - Tabular data loaded by ``pytablereader`` can be written another tabular data format with ``pytablewriter``.

