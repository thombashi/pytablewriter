# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import typepy

from ..._function import (
    quote_datetime_formatter,
    dateutil_datetime_formatter
)
from ._python import PythonCodeTableWriter


class NumpyTableWriter(PythonCodeTableWriter):
    """
    A table writer class for ``numpy`` source code format.

    :Examples:

        :ref:`example-python-code-table-writer`

    .. py:method:: write_table

        |write_table| with ``numpy.array`` format.
        The tabular data will be written as nested list variable definition
        for Python format.

        :raises pytablewriter.EmptyTableNameError:
            If the |table_name| is empty.
        :raises pytablewriter.EmptyTableDataError:
            If the |header_list| and the |value_matrix| is empty.

        .. note::

            Values in the tabular data which described below will be converted
            when writing:

            - |None|: written as ``None``
            - |inf|: written as ``float("inf")``
            - |nan|: written as ``float("nan")``
            - |datetime| instances determined by |is_datetime_instance_formatting| attribute:
                - |True|: written as `dateutil.parser <https://dateutil.readthedocs.io/en/stable/parser.html>`__
                - |False|: written as |str|

            .. seealso::

                :ref:`example-type-hint-python`
    """

    @property
    def format_name(self):
        return "numpy"

    def __init__(self):
        super(NumpyTableWriter, self).__init__()

        self.import_numpy_as = "np"
        self._dp_extractor.type_value_mapping[typepy.Typecode.INFINITY] = (
            "{:s}.inf".format(self.import_numpy_as))
        self._dp_extractor.type_value_mapping[typepy.Typecode.NAN] = (
            "{:s}.nan".format(self.import_numpy_as))

    def _get_opening_row_item_list(self):
        array_def = "{:s}.array([".format(self.import_numpy_as)

        if typepy.is_not_null_string(self.table_name):
            return ["{} = {}".format(self.variable_name, array_def)]

        return array_def

    def _get_closing_row_item_list(self):
        return "])"
