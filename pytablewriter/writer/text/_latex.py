import copy
import re
from typing import Any, Final

import dataproperty as dp
import typepy
from dataproperty import ColumnDataProperty, DataProperty
from typepy import Typecode

from ...style import Align, LatexStyler, Style, StylerInterface, TextStyler
from .._table_writer import AbstractTableWriter
from ._text_writer import IndentationTextTableWriter


class LatexWriter(IndentationTextTableWriter):
    """
    A base writer class for LaTeX format.
    """

    _RE_MATH_PARTS: Final = re.compile(r"^\\?[a-zA-Z]+$")

    @property
    def support_split_write(self) -> bool:
        return True

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self._set_chars("")

        self.is_write_opening_row = True
        self.is_write_closing_row = True
        self.indent_string = kwargs.get("indent_string", "    ")
        self.column_delimiter = " & "
        self.char_right_side_row = r" \\"

        self._quoting_flags = copy.deepcopy(dp.NOT_QUOTING_FLAGS)

        self._init_cross_point_maps()

    def _is_math_parts(self, value_dp: DataProperty) -> bool:
        if value_dp.typecode in [Typecode.INTEGER, Typecode.REAL_NUMBER]:
            return False

        try:
            if self._RE_MATH_PARTS.search(value_dp.data):
                return True
        except TypeError:
            pass

        return False

    def _get_col_align_char_list(self) -> list[str]:
        col_align_list = []

        for col_dp in self._column_dp_list:
            align = self._get_col_style(col_dp.column_index).align
            if align is None or align == Align.AUTO:
                align = col_dp.align

            if align == Align.RIGHT:
                col_align = "r"
            elif align == Align.CENTER:
                col_align = "c"
            else:
                col_align = "l"

            col_align_list.append(col_align)

        return col_align_list

    def _write_opening_row(self) -> None:
        super()._write_opening_row()
        self.inc_indent_level()

    def _write_closing_row(self) -> None:
        self.dec_indent_level()
        super()._write_closing_row()

    def _to_math_parts(self, value: str) -> str:
        # dollar characters for both sides of math parts are not required in
        # Jupyter latex.
        # return r"${:s}$".format(value)

        return value

    def _create_styler(self, writer: AbstractTableWriter) -> StylerInterface:
        return LatexStyler(writer)


class LatexMatrixWriter(LatexWriter):
    """
    A matrix writer class for LaTeX environment.

        :Example:
            :ref:`example-latex-matrix-writer`

    .. py:method:: write_table

        |write_table| with LaTeX ``array`` environment.

        :Example:
            :ref:`example-latex-matrix-writer`
    """

    FORMAT_NAME = "latex_matrix"
    _RE_VAR: Final = re.compile(r"^[a-zA-Z]+_\{[a-zA-Z0-9]+\}$")

    @property
    def format_name(self) -> str:
        return self.FORMAT_NAME

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.is_write_header = False
        self.is_write_header_separator_row = False

    def _to_row_item(self, row_idx: int, col_dp: ColumnDataProperty, value_dp: DataProperty) -> str:
        row_item = super()._to_row_item(row_idx, col_dp, value_dp)

        if self._RE_VAR.search(row_item):
            return row_item

        if self._is_math_parts(value_dp):
            return self._to_math_parts(row_item)

        return row_item

    def _get_header_row_separator_items(self) -> list[str]:
        return []

    def _get_opening_row_items(self) -> list[str]:
        row_item_list = []

        if typepy.is_not_null_string(self.table_name):
            row_item_list.append(self.table_name + r" = \left( ")
        else:
            row_item_list.append(r"\left( ")

        row_item_list.extend(
            [r"\begin{array}{", "{:s}".format("".join(self._get_col_align_char_list())), "}"]
        )

        return ["".join(row_item_list)]

    def _get_closing_row_items(self) -> list[str]:
        return [r"\end{array} \right)"]

    def _write_opening_row(self) -> None:
        self._write_line(r"\begin{equation}")
        self.inc_indent_level()
        super()._write_opening_row()

    def _write_closing_row(self) -> None:
        super()._write_closing_row()
        self.dec_indent_level()
        self._write_line(r"\end{equation}")


class LatexTableWriter(LatexWriter):
    """
    A table writer for LaTeX ``array`` (default) or text-mode ``tabular``.

    Args:
        table_environment (str): Either ``"array"`` or ``"tabular"``.

        :Example:
            :ref:`example-latex-table-writer`

    .. py:method:: write_table

        |write_table| with the selected LaTeX ``array`` or ``tabular`` environment.

        :Example:
            :ref:`example-latex-table-writer`
    """

    FORMAT_NAME = "latex_table"

    @property
    def format_name(self) -> str:
        return self.FORMAT_NAME

    @property
    def table_environment(self) -> str:
        """LaTeX environment: ``array`` (default) or ``tabular``."""
        return self.__table_environment

    @table_environment.setter
    def table_environment(self, value: str) -> None:
        if value not in ("array", "tabular"):
            raise ValueError("table_environment must be 'array' or 'tabular'")
        self.__table_environment = value

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.table_environment = kwargs.get("table_environment", "array")

        self.char_right_side_row = r" \\ \hline"
        self._dp_extractor.set_type_value(Typecode.INFINITY, r"\infty")

    def _get_opening_row_items(self) -> list[str]:
        return [
            "".join(
                [
                    rf"\begin{{{self.table_environment}}}{{",
                    "{:s}".format(" | ".join(self._get_col_align_char_list())),
                    r"} \hline",
                ]
            )
        ]

    def __is_requre_verbatim(self, value_dp: DataProperty) -> bool:
        if value_dp.typecode != typepy.Typecode.STRING:
            return False

        return True

    def __verbatim(self, value: str) -> str:
        return r"\verb" + f"|{value:s}|"

    def _to_header_item(self, col_dp: ColumnDataProperty, value_dp: DataProperty) -> str:
        if self.table_environment == "tabular":
            return super()._to_header_item(col_dp, value_dp)
        return self.__verbatim(super()._to_header_item(col_dp, value_dp))

    def _to_row_item(self, row_idx: int, col_dp: ColumnDataProperty, value_dp: DataProperty) -> str:
        row_item = super()._to_row_item(row_idx, col_dp, value_dp)

        if self.table_environment == "tabular":
            return row_item

        if self._is_math_parts(value_dp):
            return self._to_math_parts(row_item)

        if self.__is_requre_verbatim(value_dp):
            return self.__verbatim(row_item)

        return row_item

    def _get_header_row_separator_items(self) -> list[str]:
        return [r"\hline"]

    def _get_closing_row_items(self) -> list[str]:
        return [rf"\end{{{self.table_environment}}}"]

    def _apply_style_to_header_item(
        self, col_dp: ColumnDataProperty, value_dp: DataProperty, style: Style
    ) -> str:
        if self.table_environment == "array":
            return super()._apply_style_to_header_item(col_dp, value_dp, style)
        return self.__tabular_cell(col_dp, value_dp, style, is_header=True)

    def _apply_style_to_row_item(
        self, row_idx: int, col_dp: ColumnDataProperty, value_dp: DataProperty, style: Style
    ) -> str:
        if self.table_environment == "array":
            return super()._apply_style_to_row_item(row_idx, col_dp, value_dp, style)
        return self.__tabular_cell(col_dp, value_dp, style, is_header=False)

    def __tabular_cell(
        self, col_dp: ColumnDataProperty, value_dp: DataProperty, style: Style, is_header: bool
    ) -> str:
        # Escape data before applying LaTeX style commands, including separators
        # introduced by numeric formatting. Headers are always literal text.
        value = TextStyler(self).apply(col_dp.dp_to_str(value_dp), style)
        if not is_header and (
            value_dp.typecode == Typecode.INFINITY
            or re.fullmatch(r"\\[a-zA-Z]+", str(value_dp.data))
        ):
            value = r"\ensuremath{" + value + "}"
        else:
            escapes = {
                "\\": r"\textbackslash{}",
                "&": r"\&",
                "%": r"\%",
                "$": r"\$",
                "#": r"\#",
                "_": r"\_",
                "{": r"\{",
                "}": r"\}",
                "~": r"\textasciitilde{}",
                "^": r"\textasciicircum{}",
                "|": r"\textbar{}",
            }
            value = "".join(escapes.get(char, " " if char.isspace() else char) for char in value)
        return self._styler.apply_align(self._styler.apply(value, style), style)
