# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import dataproperty as dp
import dominate.tags as tags
from mbstrdecoder import MultiByteStrDecoder
import pathvalidate
from six.moves import zip

from .._error import EmptyHeaderError
from ._text_writer import TextTableWriter


class HtmlTableWriter(TextTableWriter):
    """
    Concrete class of a table writer for HTML format.

    :Examples:

        :ref:`example-html-table-writer`
    """

    @property
    def support_split_write(self):
        return False

    def __init__(self):
        super(HtmlTableWriter, self).__init__()

        self.is_padding = False
        self.is_quote_header = False
        self.indent_string = u"    "
        self.is_quote_header = False
        self.is_quote_table[dp.Typecode.STRING] = False
        self.is_quote_table[dp.Typecode.DATETIME] = False

        self._table_tag = None

    def write_table(self):
        """
        |write_table| with HTML table format.

        .. note::

            - |None| is not written
        """

        self._verify_property()
        self._preprocess()

        if dp.is_not_empty_string(self.table_name):
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

    def _write_header(self):
        if not self.is_write_header:
            return

        if dp.is_empty_sequence(self.header_list):
            raise EmptyHeaderError()

        tr_tag = tags.tr()
        for header in self.header_list:
            tr_tag += tags.th(MultiByteStrDecoder(header).unicode_str)

        thead_tag = tags.thead()
        thead_tag += tr_tag

        self._table_tag += thead_tag

    def _write_body(self):
        tbody_tag = tags.tbody()

        for value_list, value_prop_list in zip(self._value_matrix, self._value_prop_matrix):
            tr_tag = tags.tr()
            for value, value_prop in zip(value_list, value_prop_list):
                td_tag = tags.td(MultiByteStrDecoder(value).unicode_str)
                td_tag["align"] = value_prop.align.align_string
                tr_tag += td_tag
            tbody_tag += tr_tag

        self._table_tag += tbody_tag
        self._write_line(self._table_tag.render(indent=self.indent_string))
