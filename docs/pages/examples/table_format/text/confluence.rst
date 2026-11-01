.. _example-confluence-table-writer:

Confluence Wiki markup
======================

``ConfluenceWikiTableWriter`` writes double-pipe header cells and single-pipe
data cells, following the `Confluence Wiki markup table syntax
<https://support.atlassian.com/confluence-cloud/docs/insert-confluence-wiki-markup/>`__.
Use it with consumers that accept Wiki markup. The new Confluence Cloud editor
does not support inserting markup. This writer does not connect to Confluence
or produce its XML storage format.

.. literalinclude:: ../../../../../examples/confluence_table.py
    :language: python
    :caption: Write a Confluence Wiki table

Output::

    ||Name||Count||Notes||
    |Alice|2|a\|b|
    |雪|3|first\\ second|

The factory accepts ``confluence`` and ``confluence_wiki`` (case insensitive).
No file extension is registered; choose the format by name when writing a file.

Escaping and formatting
-----------------------

The same structural escaping applies to headers and data values after the usual
type conversion and formatting:

* A pipe becomes ``\|`` so it cannot introduce another cell.
* A literal backslash becomes ``&#92;`` instead of doubling it: two backslashes
  mean a line break in the Wiki renderer. This uses the character-entity
  workaround described in `Atlassian's renderer issue
  <https://jira.atlassian.com/browse/JRASERVER-23558>`__.
* CRLF, LF, and standalone CR become an explicit line break (``\\`` followed by
  a space). The space separates consecutive breaks and keeps the next cell
  delimiter separate. See `Confluence text breaks
  <https://confluence.atlassian.com/conf101/confluence-wiki-markup-1652924946.html#ConfluenceWikiMarkup-TextBreaks>`__.
* Empty data values, including ``None``, use a space to keep adjacent cell
  delimiters from becoming a header marker. Headers follow the usual conversion
  to strings (for example, a header of ``None`` is written as ``None``).

Padding is disabled by default. Margins, numeric precision, type hints, column
formatting, and ``is_write_header`` use the existing text writer interface.
``table_name`` is metadata and does not add a caption or a heading.
``write_table_iter()`` accepts chunks through ``value_matrix`` and writes the
header once; use consistent column types and formatting across chunks.
With ``is_padding=True``, each chunk calculates its own column widths.
Other inline Wiki markup in cells is left to the consumer. This is structural
escaping, not a general Wiki markup sanitizer.

Tests check output and table boundaries locally. They do not validate rendering
in a live Confluence instance or Cloud editor.
