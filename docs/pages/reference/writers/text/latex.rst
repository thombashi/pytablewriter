LaTeX writer classes
-------------------------------

LaTeX matrix writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.LatexMatrixWriter
    :members:
    :inherited-members:
    :show-inheritance:

LaTeX table writer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: pytablewriter.LatexTableWriter
    :members:
    :inherited-members:
    :show-inheritance:

Text-mode tables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``LatexTableWriter(table_environment="tabular")`` writes a text-mode
``tabular`` environment. The default, ``"array"``, retains the existing
math-mode output. The writable ``table_environment`` property accepts only
``"array"`` and ``"tabular"``; other values raise ``ValueError``.
``LatexMatrixWriter`` is unchanged.

In ``tabular``, headers are literal text. Text cells escape LaTeX special
characters, including pipes and backslashes; whitespace such as newlines
and tabs becomes spaces within a cell. Numbers use the existing formatting.
Infinity and whole-cell single LaTeX control words (for example ``r"\alpha"``)
are wrapped in ``\ensuremath{...}``. Control words must be valid mathematical
commands in the document. Other strings, including ``"$x^2$"`` and
``"x_{1}"``, are literal text, not arbitrary LaTeX expressions.

Column styles and style filters still apply after escaping. Font size,
weight, italic/typewriter and underline use the existing LaTeX commands.
Strike-through requires ``ulem``. Foreground colors retain the existing
``\textcolor{<color code>}{...}`` output; the document must provide matching
color definitions and ``xcolor``. This option does not repair existing color
naming conventions. Set ``enable_ansi_escape=False`` when generating a TeX document
with styles. Unicode support depends on the document engine and fonts.
``table_name`` is ignored, as for the default array output; no floating
``table`` wrapper or caption is generated. Split writing uses the same
opening/header/closing behavior as array writing.

For a complete executable example (including factory keyword arguments), see
``examples/py/latex_tabular.py``. Insert its output directly into the document
body, outside math delimiters::

    \documentclass{article}
    \begin{document}
    % Insert the generated tabular here.
    \end{document}
