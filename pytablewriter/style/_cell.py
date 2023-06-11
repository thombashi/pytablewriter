from dataclasses import dataclass
from typing import Any

from ._style import Style


@dataclass(frozen=True)
class Cell:
    """
    A data class representing a cell in a table.
    """

    row: int
    """row index. ``-1`` means that the table header row."""

    col: int
    """column index."""

    value: Any
    """data for the cell."""

    default_style: Style
    """default |Style| for the cell."""

    def is_header_row(self) -> bool:
        """
        Return |True| if the cell is a header.
        """

        return self.row < 0
