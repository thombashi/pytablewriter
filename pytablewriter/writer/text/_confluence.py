import copy
from collections.abc import Sequence
from typing import Any

import dataproperty as dp
from dataproperty import ColumnDataProperty, DataProperty, LineBreakHandling

from .._common import HEADER_ROW
from ._text_writer import TextTableWriter


class ConfluenceWikiTableWriter(TextTableWriter):
    """Write a table as Confluence Wiki markup.

    Headers use double pipes and data rows use single pipes. This format is for
    Wiki markup consumers; the new Confluence Cloud editor does not accept markup.
    See :ref:`example-confluence-table-writer` for usage and escaping rules.
    """

    FORMAT_NAME = "confluence"

    @property
    def format_name(self) -> str:
        return self.FORMAT_NAME

    @property
    def support_split_write(self) -> bool:
        return True

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("is_padding", False)
        super().__init__(**kwargs)

        self.is_write_header_separator_row = False
        self.is_write_value_separator_row = False
        self.is_write_opening_row = False
        self.is_write_closing_row = False
        self._quoting_flags = copy.deepcopy(dp.NOT_QUOTING_FLAGS)
        self.update_preprocessor(line_break_handling=LineBreakHandling.NOP)

    def _to_header_item(self, col_dp: ColumnDataProperty, value_dp: DataProperty) -> str:
        return self._escape_cell(super()._to_header_item(col_dp, value_dp))

    def _to_row_item(self, row_idx: int, col_dp: ColumnDataProperty, value_dp: DataProperty) -> str:
        return self._escape_cell(super()._to_row_item(row_idx, col_dp, value_dp))

    def _write_row(self, row: int, values: Sequence[str]) -> None:
        if not values:
            return

        delimiter = "||" if row == HEADER_ROW else "|"
        # Adjacent single pipes denote a header cell, not an empty data cell.
        self._write_line(delimiter + delimiter.join(value or " " for value in values) + delimiter)

    def _write_value_row_separator(self) -> None:
        # Split writes call this even when is_write_value_separator_row is False.
        pass

    def _get_closing_row_items(self) -> list[str]:
        # The base iterator enables the closing row for the last chunk.
        return []

    @staticmethod
    def _escape_cell(value: str) -> str:
        # A doubled literal backslash would become a Confluence line break.
        # Use the renderer's character-entity workaround for literal backslashes.
        value = value.replace("\\", "&#92;").replace("|", r"\|")
        value = value.replace("\r\n", "\n").replace("\r", "\n")
        # The space separates consecutive breaks and keeps a trailing break from
        # consuming a following cell delimiter. No physical newlines remain.
        return value.replace("\n", "\\\\ ")
