# encoding: utf-8

from __future__ import absolute_import, unicode_literals

import copy
import warnings

import dataproperty
import typepy
from mbstrdecoder import MultiByteStrDecoder
from six.moves import zip

from ...error import EmptyHeaderError
from ...sanitizer import sanitize_python_var_name
from ...style import FontStyle, FontWeight, HtmlStyler
from .._common import import_error_msg_template
from ._text_writer import TextTableWriter


def _get_tags_module():
    try:
        from dominate import tags

        return tags
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

        tags = _get_tags_module()

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
        tags = _get_tags_module()

        if not self.is_write_header:
            return

        if typepy.is_empty_sequence(self.headers):
            raise EmptyHeaderError("headers is empty")

        tr_tag = tags.tr()
        for header in self.headers:
            tr_tag += tags.th(MultiByteStrDecoder(header).unicode_str)

        thead_tag = tags.thead()
        thead_tag += tr_tag

        self._table_tag += thead_tag

    def _write_body(self):
        tags = _get_tags_module()
        tbody_tag = tags.tbody()

        for values, value_dp_list in zip(self._table_value_matrix, self._table_value_dp_matrix):
            tr_tag = tags.tr()
            for value, value_dp, styler in zip(values, value_dp_list, self._styler_list):
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
        styles = []

        if styler.font_size:
            styles.append(styler.font_size)
        if styler._style.font_weight == FontWeight.BOLD:
            styles.append("font-weight:bold")
        if styler._style.font_style == FontStyle.ITALIC:
            styles.append("font-style:italic")

        if not styles:
            return None

        return "; ".join(styles)

    def _create_styler(self, style, writer):
        return HtmlStyler(style, writer)
