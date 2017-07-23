# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

from mbstrdecoder import MultiByteStrDecoder
import typepy

from ..._error import EmptyTableNameError
from ._numpy import NumpyTableWriter


class PandasDataFrameWriter(NumpyTableWriter):
    """
    A writer class for Pandas DataFrame format.

    .. py:attribute:: import_pandas_as

        Specify ``pandas`` module import name. Defaults to ``"pd"``.

    .. py:attribute:: import_numpy_as

        Specify ``numpy`` module import name. Defaults to ``"np"``.

    .. py:method:: write_table

        |write_table| with Pandas DataFrame format.
        The tabular data are written as a ``pandas.DataFrame`` class
        instance definition.

        :raises pytablewriter.EmptyTableNameError:
            If the |table_name| is empty.
        :raises pytablewriter.EmptyHeaderError: If the |header_list| is empty.
        :Example:
            :ref:`example-pandas-dataframe-writer`

        .. note::
            Specific values in the tabular data are converted when writing:

            - |None|: written as ``None``
            - |inf|: written as ``numpy.inf``
            - |nan|: written as ``numpy.nan``
            - |datetime| instances determined by |is_datetime_instance_formatting| attribute:
                - |True|: written as `dateutil.parser <https://dateutil.readthedocs.io/en/stable/parser.html>`__
                - |False|: written as |str|

            .. seealso::
                :ref:`example-type-hint-python`
    """

    @property
    def format_name(self):
        return "pandas"

    def __init__(self):
        super(PandasDataFrameWriter, self).__init__()

        self.table_name = ""
        self.import_pandas_as = "pd"
        self.is_write_header = False

    def _get_opening_row_item_list(self):
        return ["{} = {}.DataFrame([".format(
            self.variable_name, self.import_pandas_as)]

    def _get_closing_row_item_list(self):
        if typepy.is_not_empty_sequence(self.header_list):
            return [
                "], columns=[{}])".format(", ".join([
                    '"{}"'.format(MultiByteStrDecoder(header).unicode_str)
                    for header in self.header_list
                ]))
            ]

        return ["])"]

    def _verify_property(self):
        super(PandasDataFrameWriter, self)._verify_property()

        if typepy.is_null_string(self.table_name):
            raise EmptyTableNameError(
                "table_name must be a string of one or more characters")
