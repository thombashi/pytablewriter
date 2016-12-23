# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import dataproperty as dp
from mbstrdecoder import MultiByteStrDecoder

from ._text_writer import IndentationTextTableWriter


class RstTableWriter(IndentationTextTableWriter):
    """
    Base class of reStructuredText table writer.
    """

    def __init__(self):
        super(RstTableWriter, self).__init__()

        self.char_header_row_separator = u"="
        self.char_cross_point = u"+"
        self.indent_string = u"    "
        self.is_write_header_separator_row = True
        self.is_write_value_separator_row = True
        self.is_write_opening_row = True
        self.is_write_closing_row = True
        self.is_quote_header = False
        self.is_quote_table[dp.Typecode.STRING] = False
        self.is_quote_table[dp.Typecode.DATETIME] = False

        self._is_remove_line_break = True

        self.table_name = u""

    def _write_table(self):
        self._verify_property()

        if dp.is_empty_string(self.table_name):
            self._write_line(u".. table:: ")
        else:
            self._write_line(u".. table:: {}".format(
                MultiByteStrDecoder(self.table_name).unicode_str))

        self._write_line()
        self.inc_indent_level()
        super(RstTableWriter, self).write_table()
        self.dec_indent_level()


class RstCsvTableWriter(RstTableWriter):
    """
    Concrete class of a table writer for reStructuredText
    `CSV table <http://docutils.sourceforge.net/docs/ref/rst/directives.html#id4>`__
    format.

    :Examples:

        :ref:`example-rst-csv-table-writer`
    """

    @property
    def support_split_write(self):
        return True

    def __init__(self):
        super(RstCsvTableWriter, self).__init__()

        self.column_delimiter = u", "
        self.char_cross_point = u""
        self.is_padding = False
        self.is_write_header_separator_row = False
        self.is_write_value_separator_row = False
        self.is_write_closing_row = False
        self.is_quote_table[dp.Typecode.STRING] = True
        self.is_quote_table[dp.Typecode.DATETIME] = True

    def write_table(self):
        """
        |write_table| with reStructuredText CSV table format.

        :raises pytablewriter.EmptyTableDataError:
            If the |header_list| and the |value_matrix| is empty.

        .. note::

            - |None| values will be written as an empty string.
        """

        self._verify_property()
        self._preprocess()

        self.inc_indent_level()
        super(RstCsvTableWriter, self).write_table()
        self.dec_indent_level()

    def _get_opening_row_item_list(self):
        directive = u".. csv-table:: "

        if dp.is_empty_string(self.table_name):
            return [directive]

        return [directive + MultiByteStrDecoder(self.table_name).unicode_str]

    def _write_opening_row(self):
        self.dec_indent_level()
        super(RstTableWriter, self)._write_opening_row()
        self.inc_indent_level()

    def _write_header(self):
        if not self.is_write_header:
            return

        if dp.is_not_empty_sequence(self.header_list):
            self._write_line(u':header: "{:s}"'.format(u'", "'.join(
                [
                    MultiByteStrDecoder(header).unicode_str
                    for header in self.header_list
                ]))
            )

        self._write_line(u":widths: " + u", ".join([
            str(col_prop.padding_len)
            for col_prop in self._column_prop_list
        ]))
        self._write_line()

    def _get_value_row_separator_item_list(self):
        return []

    def _get_closing_row_item_list(self):
        return []


class RstGridTableWriter(RstTableWriter):
    """
    Concrete class of a table writer for reStructuredText
    `grid tables <http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#grid-tables>`__
    format.

    :Examples:

        :ref:`example-rst-grid-table-writer`
    """

    @property
    def support_split_write(self):
        return False

    def __init__(self):
        super(RstGridTableWriter, self).__init__()

        self.char_left_side_row = u"|"
        self.char_right_side_row = u"|"

    def write_table(self):
        """
        |write_table| with reStructuredText grid tables format.

        .. note::

            - |None| values will be written as an empty string.
        """

        self._write_table()


class RstSimpleTableWriter(RstTableWriter):
    """
    Concrete class of a table writer for reStructuredText
    `simple tables <http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#simple-tables>`__
    format.

    :Examples:

        :ref:`example-rst-simple-table-writer`
    """

    @property
    def support_split_write(self):
        return False

    def __init__(self):
        super(RstSimpleTableWriter, self).__init__()

        self.column_delimiter = u"  "
        self.char_cross_point = u"  "

        self.char_opening_row = u"="
        self.char_closing_row = u"="

        self.is_write_value_separator_row = False

    def write_table(self):
        """
        |write_table| with reStructuredText simple tables format.

        .. note::

            - |None| values will be written as an empty string.
        """

        self._write_table()
