import copy
from typing import List, Sequence

import dataproperty as dp
import typepy
from dataproperty import ColumnDataProperty, DataProperty, LineBreakHandling
from mbstrdecoder import MultiByteStrDecoder

from ...style import Align
from ...style._styler import get_align_char
from ._text_writer import TextTableWriter


class AsciiDocTableWriter(TextTableWriter):
    """
    A table writer class for `AsciiDoc <https://asciidoc.org/>`__ format.
    """

    FORMAT_NAME = "asciidoc"

    @property
    def format_name(self) -> str:
        return self.FORMAT_NAME

    @property
    def support_split_write(self) -> bool:
        return True

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.column_delimiter = "\n"

        self.is_padding = False
        self.is_write_header_separator_row = True
        self.is_write_value_separator_row = True
        self.is_write_opening_row = True
        self.is_write_closing_row = True

        self.update_preprocessor(line_break_handling=LineBreakHandling.NOP)

        self._quoting_flags = copy.deepcopy(dp.NOT_QUOTING_FLAGS)

    def _write_value_row(
        self, row: int, values: Sequence[str], value_dp_list: Sequence[DataProperty]
    ) -> None:
        self._write_row(
            row,
            [
                self.__modify_row_element(col_idx, value, value_dp)
                for col_idx, (value, value_dp), in enumerate(zip(values, value_dp_list))
            ],
        )

    def _get_opening_row_items(self) -> List[str]:
        cols = ", ".join(
            f"{get_align_char(col_dp.align)}{col_dp.ascii_char_width}"
            for col_dp in self._column_dp_list
        )
        rows = [f'[cols="{cols}" options="header"]']

        if typepy.is_not_null_string(self.table_name):
            rows.append("." + MultiByteStrDecoder(self.table_name).unicode_str)

        rows.append("|===")

        return ["\n".join(rows)]

    def _get_header_row_separator_items(self) -> List[str]:
        return [""]

    def _get_value_row_separator_items(self) -> List[str]:
        return self._get_header_row_separator_items()

    def _get_closing_row_items(self) -> List[str]:
        return ["|==="]

    def _get_header_format_string(self, col_dp: ColumnDataProperty, value_dp: DataProperty) -> str:
        return f"{get_align_char(Align.CENTER)}|{{}}"

    def __modify_row_element(self, col_idx: int, value: str, value_dp: DataProperty):
        if value_dp.align != self._column_dp_list[col_idx].align:
            forma_stirng = "{0:s}|{1:s}"
        else:
            forma_stirng = "|{1:s}"

        return forma_stirng.format(get_align_char(value_dp.align), value)
