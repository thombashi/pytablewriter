# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import

import dataproperty

from ._text_writer import SourceCodeTableWriter


class PandasDataFrameWriter(SourceCodeTableWriter):
    """
    Concrete class of a writer for Pandas DataFrame format.

    :Examples:

        :ref:`example-pandas-dataframe-writer`
    """

    def __init__(self):
        super(PandasDataFrameWriter, self).__init__()

        self.table_name = u""

    def write_table(self):
        """
        |write_table| with Pandas DataFrame variable definition format.
        """

        import pprint

        self._verify_property()
        self._preprocess()

        if dataproperty.is_not_empty_string(self.table_name):
            self._write_line(self.table_name + u" = pandas.DataFrame(")
        else:
            self._write_line(u"pandas.DataFrame(")

        self.inc_indent_level()
        data_frame_text = (
            u"\n".join([
                self._get_indent_string() + line
                for line in
                pprint.pformat(self._value_matrix, indent=1).splitlines()
            ]) +
            u")"
        )
        self.dec_indent_level()

        self.dec_indent_level()
        self._write_line(data_frame_text)
        self.inc_indent_level()

    def _preprocess_value_matrix(self):
        if self._preprocessed_value_matrix:
            return

        self._value_matrix = [
            [dataproperty.convert_value(value) for value in value_list]
            for value_list in self.value_matrix
        ]
        self._value_matrix = dict(zip(self.header_list, self._value_matrix))

        self._preprocessed_value_matrix = True
