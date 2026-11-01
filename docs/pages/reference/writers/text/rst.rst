reStructuredText writer classes
-------------------------------

reStructuredText CSV table writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.RstCsvTableWriter
    :members:
    :inherited-members:
    :show-inheritance:

reStructuredText grid table writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Grid table cells and headers preserve line breaks (LF, CRLF, and CR), empty
lines, and relative indentation. Column widths use the longest physical line;
row separators are written between logical rows only. For example:

.. code-block:: python

    from pytablewriter import RstGridTableWriter

    writer = RstGridTableWriter(
        headers=["Description", "Status"],
        value_matrix=[["First paragraph\n\nSecond paragraph", "Ready"]],
    )
    writer.write_table()

Multiline cells are aligned as a block, preserving the indentation required by
nested lists, literal blocks, and directives. Bold and italic styles decorate
each nonempty physical line; use the normal font style for cells containing
block markup such as directives. Disable ``enable_ansi_escape`` when using
terminal font styles to produce RST for a document, or use ``dump()`` (which
disables terminal escapes automatically).

Type conversion and style-filter row indices refer to logical cells, and the
input ``value_matrix`` is not split into extra rows. Grid tables do not support
``write_table_iter()``. These multiline rules do not apply to the simple or CSV
table writers.

.. autoclass:: pytablewriter.RstGridTableWriter
    :members:
    :inherited-members:
    :show-inheritance:

reStructuredText simple table writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.RstSimpleTableWriter
    :members:
    :inherited-members:
    :show-inheritance:
