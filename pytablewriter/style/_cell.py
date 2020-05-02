from typing import Any

from typing_extensions import Final  # noqa

from ._style import Style


class Cell:
    def __init__(self, row: int, col: int, value: Any, default_style: Style):
        self.row = row  # type: Final
        self.col = col  # type: Final
        self.value = value  # type: Final
        self.default_style = default_style  # type: Final
