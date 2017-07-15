# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import copy

import dataproperty
from mbstrdecoder import MultiByteStrDecoder
import pathvalidate
import typepy

import dominate.tags as tags
from six.moves import zip

from .._error import EmptyHeaderError
from ._text_writer import TextTableWriter


class HtmlTableWriter(TextTableWriter):
    """
    A table writer class for HTML format.
    """

    @property
    def format_name(self):
        return "html"

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

        self._logger.logging_start_write()

        self._verify_property()
        self._preprocess()

        if typepy.is_not_null_string(self.table_name):
            self._table_tag = tags.table(
                id=pathvalidate.sanitize_python_var_name(self.table_name))
            self._table_tag += tags.caption(
                MultiByteStrDecoder(self.table_name).unicode_str)
        else:
            self._table_tag = tags.table()

        try:
            self._write_header()
        except EmptyHeaderError:
            pass

        self._write_body()

        self._logger.logging_complete_write()

    def _write_header(self):
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
        tbody_tag = tags.tbody()

        for value_list, value_dp_list in zip(self._value_matrix, self._value_dp_matrix):
            tr_tag = tags.tr()
            for value, value_dp in zip(value_list, value_dp_list):
                td_tag = tags.td(MultiByteStrDecoder(value).unicode_str)
                td_tag["align"] = value_dp.align.align_string
                tr_tag += td_tag
            tbody_tag += tr_tag

        self._table_tag += tbody_tag
        self._write_line(self._table_tag.render(indent=self.indent_string))
