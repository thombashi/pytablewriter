# encoding: utf-8

from __future__ import absolute_import, unicode_literals

import copy

import dataproperty
import typepy
from mbstrdecoder import MultiByteStrDecoder
from six.moves import zip

from ...error import EmptyHeaderError
from ...sanitizer import sanitize_python_var_name
from ...style import FontStyle, FontWeight, HtmlStyler
from ._text_writer import TextTableWriter


class HtmlTableWriter(TextTableWriter):
    """
    A table writer class for HTML format.

        :Example:
            :ref:`example-html-table-writer`
    """

    FORMAT_NAME = "html"

    @property
    def format_name(self):
        return self.FORMAT_NAME

    @property
    def support_split_write(self):
        return False

    def __init__(self):
        super(HtmlTableWriter, self).__init__()

        self.is_padding = False
        self.indent_string = "    "

        self._quoting_flags = copy.deepcopy(dataproperty.NOT_QUOTING_FLAGS)
        self._table_tag = None

    def write_table(self):
        """
        |write_table| with HTML table format.

        :Example:
            :ref:`example-html-table-writer`

        .. note::
            - |None| is not written
        """

        import dominate.tags as tags

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

    def _write_header(self):
        import dominate.tags as tags

        if not self.is_write_header:
            return

        if typepy.is_empty_sequence(self.header_list):
            raise EmptyHeaderError("header_list is empty")

        tr_tag = tags.tr()
        for header in self.header_list:
            tr_tag += tags.th(MultiByteStrDecoder(header).unicode_str)

        thead_tag = tags.thead()
        thead_tag += tr_tag

        self._table_tag += thead_tag

    def _write_body(self):
        import dominate.tags as tags

        tbody_tag = tags.tbody()

        for value_list, value_dp_list in zip(self._table_value_matrix, self._table_value_dp_matrix):
            tr_tag = tags.tr()
            for value, value_dp, styler in zip(value_list, value_dp_list, self._styler_list):
                td_tag = tags.td(MultiByteStrDecoder(value).unicode_str)
                td_tag["align"] = value_dp.align.align_string

                style_tag = self.__make_style_tag(styler)
                if style_tag:
                    td_tag["style"] = style_tag

                tr_tag += td_tag
            tbody_tag += tr_tag

        self._table_tag += tbody_tag
        self._write_line(self._table_tag.render(indent=self.indent_string))

    @staticmethod
    def __make_style_tag(styler):
        style_list = []

        if styler.font_size:
            style_list.append(styler.font_size)
        if styler._style.font_weight == FontWeight.BOLD:
            style_list.append("font-weight:bold")
        if styler._style.font_style == FontStyle.ITALIC:
            style_list.append("font-style:italic")

        if not style_list:
            return None

        return "; ".join(style_list)

    def _create_styler(self, style, writer):
        return HtmlStyler(style, writer)
