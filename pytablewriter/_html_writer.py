# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import dataproperty
import dominate.tags as tags
import pathvalidate

from ._text_writer import TextTableWriter


class HtmlTableWriter(TextTableWriter):
    """
    Concrete class of a table writer for HTML format.

    :Examples:

        :ref:`example-html-table-writer`
    """

    def __init__(self):
        super(HtmlTableWriter, self).__init__()

        self.is_padding = False
        self.is_quote_str = False
        self.indent_string = u"    "

        self._table_tag = None

    def write_table(self):
        """
        |write_table| with HTML table format.
        """

        self._verify_property()
        self._preprocess()

        if dataproperty.is_not_empty_string(self.table_name):
            self._table_tag = tags.table(
                id=pathvalidate.sanitize_python_var_name(self.table_name))
            self._table_tag += tags.caption(self.table_name)
        else:
            self._table_tag = tags.table()

        self._write_header()
        self._write_body()

    def _write_header(self):
        if not self.is_write_header:
            return

        tr_tag = tags.tr()
        for header in self.header_list:
            tr_tag += tags.th(header)

        thead_tag = tags.thead()
        thead_tag += tr_tag

        self._table_tag += thead_tag

    def _write_body(self):
        tbody_tag = tags.tbody()

        for value_list, value_prop_list in zip(self._value_matrix, self._value_prop_matrix):
            tr_tag = tags.tr()
            for value, value_prop in zip(value_list, value_prop_list):
                td_tag = tags.td(value)
                td_tag["align"] = value_prop.align.align_string
                tr_tag += td_tag
            tbody_tag += tr_tag

        self._table_tag += tbody_tag
        self._write_line(self._table_tag.render(indent=self.indent_string))
