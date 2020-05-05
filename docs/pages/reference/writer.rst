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
    :show-inheritance:

TSV writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.TsvTableWriter
    :members:
    :show-inheritance:


LTSV writer
-------------------------------
.. autoclass:: pytablewriter.LtsvTableWriter
    :members:
    :show-inheritance:


LaTeX writer classes
-------------------------------

LaTeX matrix writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.LatexMatrixWriter
    :members:
    :show-inheritance:

LaTeX table writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.LatexTableWriter
    :members:
    :show-inheritance:


Markup language writer classes
-------------------------------

HTML table writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.HtmlTableWriter
    :members:
    :show-inheritance:

MediaWiki table writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.MediaWikiTableWriter
    :members:
    :show-inheritance:

Markdown table writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.MarkdownTableWriter
    :members:
    :show-inheritance:


JSON writer class
-------------------------------
.. autoclass:: pytablewriter.JsonTableWriter
    :members:
    :show-inheritance:


Line-delimited JSON(LDJSON) writer class
--------------------------------------------------------------
.. autoclass:: pytablewriter.JsonLinesTableWriter
    :members:
    :show-inheritance:


Source code writer classes
-------------------------------

JavaScript writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.JavaScriptTableWriter
    :members:
    :show-inheritance:

NumPy table writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.NumpyTableWriter
    :members:
    :show-inheritance:

Pandas DataFrame writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.PandasDataFrameWriter
    :members:
    :show-inheritance:

Python table writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.PythonCodeTableWriter
    :members:
    :show-inheritance:


reStructuredText writer classes
-------------------------------

reStructuredText CSV table writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.RstCsvTableWriter
    :members:
    :show-inheritance:

reStructuredText grid table writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.RstGridTableWriter
    :members:
    :show-inheritance:

reStructuredText simple table writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.RstSimpleTableWriter
    :members:
    :show-inheritance:


Space aligned table writer
-------------------------------
.. autoclass:: pytablewriter.SpaceAlignedTableWriter
    :members:
    :show-inheritance:


TOML table writer class
-------------------------------
.. autoclass:: pytablewriter.TomlTableWriter
    :members:
    :show-inheritance:


YAML table writer class
-------------------------------
.. autoclass:: pytablewriter.YamlTableWriter
    :members:
    :show-inheritance:


Unicode table writer classes
-------------------------------
.. autoclass:: pytablewriter.UnicodeTableWriter
    :members:
    :show-inheritance:

.. autoclass:: pytablewriter.BoldUnicodeTableWriter
    :members:
    :show-inheritance:


Borderless table writer class
-------------------------------
.. autoclass:: pytablewriter.BorderlessTableWriter
    :members:
    :show-inheritance:


CSS table writer class
-------------------------------
.. autoclass:: pytablewriter.CssTableWriter
    :members:
    :show-inheritance:


Binary formats
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Excel writer classes
-------------------------------

Xlsx table writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.ExcelXlsxTableWriter
    :members:
    :show-inheritance:

Xls table writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.ExcelXlsTableWriter
    :members:
    :show-inheritance:


SQLite writer class
-------------------------------
.. autoclass:: pytablewriter.SqliteTableWriter
    :members:
    :show-inheritance:



Application specific formats
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Elasticsearch writer
-------------------------------
.. autoclass:: pytablewriter.ElasticsearchWriter
    :members:
    :show-inheritance:



Base writer classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Base writer classes of text formats
--------------------------------------------------------------
.. autoclass:: pytablewriter.writer._interface.TableWriterInterface
    :members:

.. autoclass:: pytablewriter.AbstractTableWriter
    :members:
    :show-inheritance:

.. autoclass:: pytablewriter.writer.text._text_writer.TextTableWriter
    :members:
    :show-inheritance:

.. autoclass:: pytablewriter.writer.text._text_writer.IndentationTextTableWriter
    :members:
    :show-inheritance:

Base writer classes of binary formats
--------------------------------------------------------------
.. autoclass:: pytablewriter.writer.binary._interface.BinaryWriterInterface
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: pytablewriter.writer.binary._interface.AbstractBinaryTableWriter
    :members:
    :undoc-members:
    :show-inheritance:

