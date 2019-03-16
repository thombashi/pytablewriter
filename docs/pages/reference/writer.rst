Table Writer Classes
====================================

Text formats
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

CSV table writer classes
-------------------------------

CSV writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.CsvTableWriter
    :members:

TSV writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.TsvTableWriter


LTSV writer
-------------------------------
.. autoclass:: pytablewriter.LtsvTableWriter


LaTeX writer classes
-------------------------------

LaTeX matrix writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.LatexMatrixWriter

LaTeX table writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.LatexTableWriter


Markup language writer classes
-------------------------------

HTML table writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.HtmlTableWriter

MediaWiki table writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.MediaWikiTableWriter

Markdown table writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.MarkdownTableWriter


JSON writer class
-------------------------------
.. autoclass:: pytablewriter.JsonTableWriter


Line-delimited JSON(LDJSON) writer class
--------------------------------------------------------------
.. autoclass:: pytablewriter.JsonLinesTableWriter


Source code writer classes
-------------------------------

JavaScript writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.JavaScriptTableWriter

NumPy table writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.NumpyTableWriter

Pandas DataFrame writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.PandasDataFrameWriter

Python table writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.PythonCodeTableWriter


reStructuredText writer classes
-------------------------------

reStructuredText CSV table writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.RstCsvTableWriter

reStructuredText grid table writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.RstGridTableWriter

reStructuredText simple table writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.RstSimpleTableWriter


Space aligned table writer
-------------------------------
.. autoclass:: pytablewriter.SpaceAlignedTableWriter


TOML table writer class
-------------------------------
.. autoclass:: pytablewriter.TomlTableWriter


Unicode table writer class
-------------------------------
.. autoclass:: pytablewriter.UnicodeTableWriter


Binary formats
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Excel writer classes
-------------------------------

Xlsx table writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.ExcelXlsxTableWriter

Xls table writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.ExcelXlsTableWriter


SQLite writer class
-------------------------------
.. autoclass:: pytablewriter.SqliteTableWriter



Application specific formats
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Elasticsearch writer
-------------------------------
.. autoclass:: pytablewriter.ElasticsearchWriter



Base writers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: pytablewriter.writer._table_writer.TableWriterInterface
    :members:

.. autoclass:: pytablewriter.writer._table_writer.AbstractTableWriter
    :members:

.. autoclass:: pytablewriter.writer.text._text_writer.TextTableWriter
    :members:

.. autoclass:: pytablewriter.writer.text._text_writer.IndentationTextTableWriter
    :members:
