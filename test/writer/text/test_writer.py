from typing import Optional

from pytablewriter import TableWriterFactory
from pytablewriter.style import Cell, Style


class Test_text_writer:
    def test_normal_style_filter(self):
        def style_filter(cell: Cell, **kwargs) -> Optional[Style]:
            if cell.is_header_row():
                return None

            if isinstance(cell.value, int):
                return Style(align="left")

            if cell.value == "c":
                return Style(align="center")

            if cell.value == "r":
                return Style(align="right")

            return None

        writer = TableWriterFactory.create_from_format_name(
            format_name="html",
            table_name="style filter",
            headers=["A", "B", "C"],
            value_matrix=[
                [1, "c", "r"],
                [2.2, "left", "left"],
            ],
            margin=1,
        )
        writer.add_style_filter(style_filter)
        output_w_filter = writer.dumps()

        writer.disable_style_filter()
        output_wo_filter = writer.dumps()
        assert output_w_filter != output_wo_filter

        writer.enable_style_filter()
        output_wo_filter_2 = writer.dumps()
        assert output_w_filter == output_wo_filter_2
