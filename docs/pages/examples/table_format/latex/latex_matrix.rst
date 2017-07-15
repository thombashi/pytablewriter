.. _example-latex-matrix-writer:

LaTeX matrix
-------------------------------------------
|LatexMatrixWriter| class can writes a table 
with LaTeX ``array`` environment to the |stream| from a matrix of data.

:Sample Code 1:
    .. code-block:: python

        import pytablewriter

        writer = pytablewriter.LatexMatrixWriter()
        writer.table_name = "A"
        writer.value_matrix = [
            [0.01, 0.00125, 0.0],
            [1.0, 99.9,  0.01],
            [1.2, 999999.123, 0.001],
        ]
        writer.write_table()

:Output 1:
    .. code-block:: TeX

        \[
            A = \left( \begin{array}{rrr}
                0.01 & 0.0012 & 0.000 \\
                1.00 & 99.9000 & 0.010 \\
                1.20 & 999999.1230 & 0.001 \\
            \end{array} \right)
        \]

:Rendering Result 1:
    .. figure:: ss/latex_matrix_num.png
       :scale: 100%
       :alt: latex_matrix_num


:Sample Code 2:
    .. code-block:: python

        import pytablewriter

        writer = pytablewriter.LatexMatrixWriter()
        writer.table_name = "B"
        writer.value_matrix = [
            ["a_{11}", "a_{12}", "],
            ["a_{21}", "a_{22}", r"\ldots", "a_{2n}"],
            ["a_{31}", "a_{32}", r"\ldots", "a_{3n}"],
        ]
        writer.write_table()

:Output 2:
    .. code-block:: TeX

        \[
            B = \left( \begin{array}{llll}
                a_{11} & a_{12} & $\ldots$ & a_{1n} \\
                a_{21} & a_{22} & $\ldots$ & a_{2n} \\
                a_{31} & a_{32} & $\ldots$ & a_{3n} \\
            \end{array} \right)
        \]

:Rendering Result 2:
    .. figure:: ss/latex_matrix_var.png
       :scale: 100%
       :alt: latex_matrix_var
