import copy
import warnings
from typing import Any, Optional, Tuple, cast  # noqa

import dataproperty
import typepy
from mbstrdecoder import MultiByteStrDecoder

from ...error import EmptyHeaderError
from ...sanitizer import sanitize_python_var_name
from ...style import FontStyle, FontWeight, HtmlStyler, Style, StylerInterface
from .._common import import_error_msg_template
from .._table_writer import AbstractTableWriter
from ._text_writer import TextTableWriter


def _get_tags_module() -> Tuple:
    try:
        from dominate import tags
        from dominate.util import raw

        return tags, raw
    except ImportError:
        warnings.warn(import_error_msg_template.format("html"))
        raise


class HtmlTableWriter(TextTableWriter):
    """
    A table writer class for HTML format.

        :Example:
            :ref:`example-html-table-writer`
    """

    FORMAT_NAME = "html"

    @property
    def format_name(self) -> str:
        return self.FORMAT_NAME

    @property
    def support_split_write(self) -> bool:
        return False

    def __init__(self) -> None:
        super().__init__()

        self.is_padding = False
        self.indent_string = "    "

        self._dp_extractor.preprocessor.line_break_repl = "<br>"
        self._dp_extractor.preprocessor.is_escape_html_tag = False
        self._quoting_flags = copy.deepcopy(dataproperty.NOT_QUOTING_FLAGS)
        self._table_tag = None  # type: Any

    def write_table(self) -> None:
        """
        |write_table| with HTML table format.

        :Example:
            :ref:`example-html-table-writer`

        .. note::
            - |None| is not written
        """

        tags, raw = _get_tags_module()

        with self._logger:
            self._verify_property()
            self._preprocess()

            if typepy.is_not_null_string(self.table_name):
                self._table_tag = tags.table(id=sanitize_python_var_name(self.table_name))
                self._table_tag += tags.caption(MultiByteStrDecoder(self.table_name).unicode_str)
            else:
                self._table_tag = tags.table()

            try:
                self._write_header()
            except EmptyHeaderError:
                pass

            self._write_body()

    def _write_header(self) -> None:
        tags, raw = _get_tags_module()

        if not self.is_write_header:
            return

        if typepy.is_empty_sequence(self._table_headers):
            raise EmptyHeaderError("headers is empty")

        tr_tag = tags.tr()
        for header in self._table_headers:
            tr_tag += tags.th(raw(MultiByteStrDecoder(header).unicode_str))

        thead_tag = tags.thead()
        thead_tag += tr_tag

        self._table_tag += thead_tag

    def _write_body(self) -> None:
        tags, raw = _get_tags_module()
        tbody_tag = tags.tbody()

        for values, value_dp_list in zip(self._table_value_matrix, self._table_value_dp_matrix):
            tr_tag = tags.tr()
            for value, value_dp, column_dp in zip(values, value_dp_list, self._column_dp_list):
                td_tag = tags.td(raw(MultiByteStrDecoder(value).unicode_str))
                td_tag["align"] = value_dp.align.align_string

                style_tag = self.__make_style_tag(style=self._get_col_style(column_dp.column_index))
                if style_tag:
                    td_tag["style"] = style_tag

                tr_tag += td_tag
            tbody_tag += tr_tag

        self._table_tag += tbody_tag
        self._write_line(self._table_tag.render(indent=self.indent_string))

    def __make_style_tag(self, style: Style) -> Optional[str]:
        styles = []  # List[str]

        if self._styler.get_font_size(style):
            styles.append(cast(str, self._styler.get_font_size(style)))
        if style.font_weight == FontWeight.BOLD:
            styles.append("font-weight:bold")
        if style.font_style == FontStyle.ITALIC:
            styles.append("font-style:italic")

        if not styles:
            return None

        return "; ".join(styles)

    def _create_styler(self, writer: AbstractTableWriter) -> StylerInterface:
        return HtmlStyler(writer)
