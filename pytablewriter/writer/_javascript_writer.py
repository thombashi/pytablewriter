# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

from dataproperty import (
    DefaultValue,
    Typecode,
)
import six

from .._const import FormatName
from .._function import quote_datetime_formatter
from ._sourcecode_writer import SourceCodeTableWriter


def js_datetime_formatter(value):
    try:
        return 'new Date("{:s}")'.format(
            value.strftime(DefaultValue.DATETIME_FORMAT))
    except ValueError:
        # the datetime strftime() methods require year >= 1900
        return 'new Date("{}")'.format(value)


class JavaScriptTableWriter(SourceCodeTableWriter):
    """
    A table writer for class JavaScript format.

    :Examples:

        :ref:`example-js-table-writer`

    .. py:attribute:: variable_declaration

        JavaScript variable declarations type.
        The value must be either ``"var"``, ``"let"`` or ``"const"``.
        Defaults to ``"const"``.

    .. py:method:: write_table

        |write_table| with JavaScript nested list variable definition format.

        :raises pytablewriter.EmptyTableNameError:
            If the |table_name| is empty.
        :raises pytablewriter.EmptyTableDataError:
            If the |header_list| and the |value_matrix| is empty.

        .. note::

            Values in the tabular data which described below will be converted
            when writing:

            - |None|: written as ``null``
            - |inf|: written as ``Infinity``
            - |nan|: written as ``NaN``
            - |datetime| instances determined by |is_datetime_instance_formatting| attribute:
                - |True|: written as `dateutil.parser <https://dateutil.readthedocs.io/en/stable/parser.html>`__
                - |False|: written as |str|

            .. seealso::

                :ref:`example-type-hint-js`
    """

    __VALID_VAR_DECLARATION = ("var", "let", "const")

    @property
    def format_name(self):
        return FormatName.JAVASCRIPT

    @property
    def support_split_write(self):
        return True

    @property
    def variable_declaration(self):
        return self.__variable_declaration

    @variable_declaration.setter
    def variable_declaration(self, value):
        value = value.strip().lower()
        if value not in self.__VALID_VAR_DECLARATION:
            raise ValueError("declaration must be either var, let or const")

        self.__variable_declaration = value

    def __init__(self):
        super(JavaScriptTableWriter, self).__init__()

        self.variable_declaration = "const"
        self._dp_extractor.type_value_mapping = {
            Typecode.NONE: "null",
            Typecode.INFINITY: "Infinity",
            Typecode.NAN: "NaN",
        }
        self._dp_extractor.const_value_mapping = {
            True: "true", False: "false"}

    def get_variable_name(self, value):
        import pathvalidate

        return pathvalidate.sanitize_js_var_name(value, "_").lower()

    def _write_table(self):
        self._verify_property()

        if self.is_datetime_instance_formatting:
            self._dp_extractor.datetime_formatter = js_datetime_formatter
        else:
            self._dp_extractor.datetime_formatter = quote_datetime_formatter

        self._preprocess()

        org_stream = self.stream
        self.stream = six.StringIO()

        self.inc_indent_level()
        super(JavaScriptTableWriter, self)._write_table()
        self.dec_indent_level()
        data_frame_text = self.stream.getvalue().rstrip("\n")
        if self.is_write_closing_row:
            data_frame_line_list = data_frame_text.splitlines()
            data_frame_line_list[-2] = data_frame_line_list[-2].rstrip(",")
            data_frame_text = "\n".join(data_frame_line_list)

        self.stream.close()
        self.stream = org_stream

        self.dec_indent_level()
        self._write_line(data_frame_text)
        self.inc_indent_level()

    def _get_opening_row_item_list(self):
        return "{:s} {:s} = [".format(
            self.variable_declaration, self.variable_name)

    def _get_closing_row_item_list(self):
        return "];"
