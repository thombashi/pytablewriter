.. _example-latex-matrix-writer:

LaTeX matrix
-------------------------------------------
|LatexMatrixWriter| class can write a table with LaTeX ``array`` environment to the |stream| from a data matrix.

:Sample Code 1:
    .. code-block:: python

        import pytablewriter

        def main():
            writer = pytablewriter.LatexMatrixWriter()
            writer.table_name = "A"
            writer.value_matrix = [
                [0.01, 0.00125, 0.0],
                [1.0, 99.9,  0.01],
                [1.2, 999999.123, 0.001],
            ]
            writer.write_table()

        if __name__ == "__main__":
            main()

:Output 1:
    .. code-block:: TeX

        \begin{equation}
            A = \left( \begin{array}{rrr}
                0.01 &      0.0012 & 0.000 \\
                1.00 &     99.9000 & 0.010 \\
                1.20 & 999999.1230 & 0.001 \\
            \end{array} \right)
        \end{equation}

:Rendering Result 1:
    .. figure:: ss/latex_matrix_num.png
       :scale: 100%
       :alt: latex_matrix_num


:Sample Code 2:
    .. code-block:: python

        import pytablewriter

        def main():
            writer = pytablewriter.LatexMatrixWriter()
            writer.table_name = "B"
            writer.value_matrix = [
                ["a_{11}", "a_{12}", "\\ldots", "a_{1n}"],
                ["a_{21}", "a_{22}", "\\ldots", "a_{2n}"],
                [r"\vdots", "\\vdots", "\\ddots", "\\vdots"],
                ["a_{n1}", "a_{n2}", "\\ldots", "a_{nn}"],
            ]
            writer.write_table()

        if __name__ == "__main__":
            main()

:Output 2:
    .. code-block:: TeX

        \begin{equation}
            B = \left( \begin{array}{llll}
                a_{11} & a_{12} & \ldots & a_{1n} \\
                a_{21} & a_{22} & \ldots & a_{2n} \\
                \vdots & \vdots & \ddots & \vdots \\
                a_{n1} & a_{n2} & \ldots & a_{nn} \\
            \end{array} \right)
        \end{equation}

:Rendering Result 2:
    .. figure:: ss/latex_matrix_var.png
       :scale: 100%
       :alt: latex_matrix_var
