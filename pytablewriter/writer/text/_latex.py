# encoding: utf-8

from __future__ import absolute_import, unicode_literals

import copy
import re

import dataproperty as dp
import typepy
from typepy import Typecode

from ...style import Align, LatexStyler
from ._text_writer import IndentationTextTableWriter


class LatexWriter(IndentationTextTableWriter):
    """
    A base writer class for LaTeX format.
    """

    _RE_MATH_PARTS = re.compile("^[\\]?[a-zA-z]+$")

    @property
    def support_split_write(self):
        return True

    def __init__(self):
        super(LatexWriter, self).__init__()

        self.is_write_opening_row = True
        self.is_write_closing_row = True
        self.indent_string = "    "
        self.column_delimiter = " & "
        self.char_right_side_row = r" \\"

        self._quoting_flags = copy.deepcopy(dp.NOT_QUOTING_FLAGS)

    def _is_math_parts(self, value_dp):
        if value_dp.typecode in [Typecode.INTEGER, Typecode.REAL_NUMBER]:
            return False

        try:
            if self._RE_MATH_PARTS.search(value_dp.data):
                return True
        except TypeError:
            pass

        return False

    def _get_col_align_char_list(self):
        col_align_list = []

        for col_dp in self._column_dp_list:
            align = self._get_style_attr_from_style(col_dp.column_index, "align")
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

    def _write_opening_row(self):
        super(LatexWriter, self)._write_opening_row()
        self.inc_indent_level()

    def _write_closing_row(self):
        self.dec_indent_level()
        super(LatexWriter, self)._write_closing_row()

    def _to_math_parts(self, value):
        # dollar characters for both sides of math parts are not required in
        # Jupyter latex.
        # return r"${:s}$".format(value)

        return value

    def _create_styler(self, style, writer):
        return LatexStyler(style, writer)


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
    _RE_VAR = re.compile(r"^[a-zA-Z]+_\{[a-zA-Z0-9]+\}$")

    @property
    def format_name(self):
        return self.FORMAT_NAME

    def __init__(self):
        super(LatexMatrixWriter, self).__init__()

        self.is_write_header = False
        self.is_write_header_separator_row = False

    def _to_row_item(self, col_dp, value_dp):
        row_item = super(LatexMatrixWriter, self)._to_row_item(col_dp, value_dp)

        if self._RE_VAR.search(row_item):
            return row_item

        if self._is_math_parts(value_dp):
            return self._to_math_parts(row_item)

        return row_item

    def _get_header_row_separator_item_list(self):
        return []

    def _get_opening_row_item_list(self):
        row_item_list = []

        if typepy.is_not_null_string(self.table_name):
            row_item_list.append(self.table_name + r" = \left( ")
        else:
            row_item_list.append(r"\left( ")

        row_item_list.extend(
            [r"\begin{array}{", "{:s}".format("".join(self._get_col_align_char_list())), "}"]
        )

        return ["".join(row_item_list)]

    def _get_closing_row_item_list(self):
        return [r"\end{array} \right)"]

    def _write_opening_row(self):
        self._write_line(r"\begin{equation}")
        self.inc_indent_level()
        super(LatexMatrixWriter, self)._write_opening_row()

    def _write_closing_row(self):
        super(LatexMatrixWriter, self)._write_closing_row()
        self.dec_indent_level()
        self._write_line(r"\end{equation}")


class LatexTableWriter(LatexWriter):
    """
    A matrix writer class for LaTeX environment.

        :Example:
            :ref:`example-latex-table-writer`

    .. py:method:: write_table

        |write_table| with LaTeX ``array`` environment.

        :Example:
            :ref:`example-latex-table-writer`
    """

    FORMAT_NAME = "latex_table"

    @property
    def format_name(self):
        return self.FORMAT_NAME

    def __init__(self):
        super(LatexTableWriter, self).__init__()

        self.char_right_side_row = r" \\ \hline"
        self._dp_extractor.type_value_map[Typecode.INFINITY] = r"\infty"

    def _get_opening_row_item_list(self):
        return [
            "".join(
                [
                    r"\begin{array}{",
                    "{:s}".format(" | ".join(self._get_col_align_char_list())),
                    r"} \hline",
                ]
            )
        ]

    def __is_requre_verbatim(self, value_dp):
        if value_dp.typecode != typepy.Typecode.STRING:
            return False

        return True

    def __verbatim(self, value):
        return r"\verb" + "|{:s}|".format(value)

    def _to_header_item(self, col_dp, value_dp):
        return self.__verbatim(super(LatexTableWriter, self)._to_header_item(col_dp, value_dp))

    def _to_row_item(self, col_dp, value_dp):
        row_item = super(LatexTableWriter, self)._to_row_item(col_dp, value_dp)

        if self._is_math_parts(value_dp):
            return self._to_math_parts(row_item)

        if self.__is_requre_verbatim(value_dp):
            return self.__verbatim(row_item)

        return row_item

    def _get_header_row_separator_item_list(self):
        return [r"\hline"]

    def _get_closing_row_item_list(self):
        return [r"\end{array}"]
