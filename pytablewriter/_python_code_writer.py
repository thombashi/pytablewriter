# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import dataproperty

from ._text_writer import SourceCodeTableWriter


class PythonCodeTableWriter(SourceCodeTableWriter):
    """
    Concrete class of a table writer for Python code (nested list) format.

    :Examples:

        :ref:`example-python-code-table-writer`
    """

    def __init__(self):
        super(PythonCodeTableWriter, self).__init__()

        self.table_name = u""

    def write_table(self):
        """
        |write_table| with Python nested list variable definition format.
        """

        self._verify_property()

        if dataproperty.is_not_empty_string(self.table_name):
            self._write_line(self.table_name + u" = [")
        else:
            self._write_line(u"[")

        self.inc_indent_level()
        super(PythonCodeTableWriter, self).write_table()
        self.dec_indent_level()
        self._write_line(u"]")
