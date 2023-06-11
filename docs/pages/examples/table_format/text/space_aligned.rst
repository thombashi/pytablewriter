.. _example-space-aligned-table-writer:

Space Aligned
----------------------------
|SpaceAlignedTableWriter| class can write a table
that aligned column with multiple spaces, to the |stream| from a data matrix.

:Sample Code:
    .. code-block:: python
        :caption: Write a space-aligned table

        import pytablewriter

        def main():
            writer = pytablewriter.SpaceAlignedTableWriter()
            writer.headers = ["PID", "USER", "PR", "NI", "VIRT", "RES", "SHR", "S", "%CPU", "%MEM", "TIME+", "COMMAND"]
            writer.value_matrix = csv1 = [
                [32866, "root", 20, 0, 48344, 3924, 3448, "R", 5.6, 0.2, "0:00.03", "top"],
                [1, "root", 20, 0, 212080, 7676, 5876, "S", 0, 0.4, "1:06.56", "systemd"],
                [2, "root", 20, 0, 0, 0, 0, "S", 0, 0, "0:01.92", "kthreadd"],
                [4, "root", 0, -20, 0, 0, 0, "S", 0, 0, "0:00.00", "kworker/0:0H"],
            ]

            writer.write_table()

        if __name__ == "__main__":
            main()

:Output:
    .. code-block:: none

         PID   USER  PR  NI    VIRT   RES   SHR   S  %CPU  %MEM   TIME+     COMMAND
        32866  root  20    0   48344  3924  3448  R   5.6   0.2  0:00.03  top
            1  root  20    0  212080  7676  5876  S     0   0.4  1:06.56  systemd
            2  root  20    0       0     0     0  S     0     0  0:01.92  kthreadd
            4  root   0  -20       0     0     0  S     0     0  0:00.00  kworker/0:0H
