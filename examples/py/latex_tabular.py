"""Generate a table for the body of a LaTeX document (outside math mode)."""

from pytablewriter import TableWriterFactory
from pytablewriter.style import Align, Style


def main() -> None:
    writer = TableWriterFactory.create_from_format_name(
        "latex_table",
        table_environment="tabular",
        headers=["Item name", "Measured value"],
        value_matrix=[["cost & tax (50%)", 12.5], ["upper limit", float("inf")]],
        column_styles=[Style(align=Align.LEFT), Style(align=Align.RIGHT)],
        enable_ansi_escape=False,
    )
    writer.write_table()


if __name__ == "__main__":
    main()
