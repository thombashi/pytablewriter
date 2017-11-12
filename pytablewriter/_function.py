# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import dataproperty


def quote_datetime_formatter(value):
    return '"{:s}"'.format(
        value.strftime(dataproperty.DefaultValue.DATETIME_FORMAT))


def dateutil_datetime_formatter(value):
    return 'dateutil.parser.parse("{:s}")'.format(
        value.strftime(dataproperty.DefaultValue.DATETIME_FORMAT))


def convert_idx_to_alphabet(column_idx):
    if column_idx < 26:
        return chr(65 + column_idx)

    return (
        convert_idx_to_alphabet(int(column_idx / 26 - 1)) +
        convert_idx_to_alphabet(column_idx % 26))


def dump_tabledata(value, format_name="rst_grid_table"):
    """
    :param tabledata.TableData value: Tabular data to dump.
    :param str format_name:
        Dumped format name of tabular data.
        Available formats are described in
        :py:meth:`~pytablewriter.TableWriterFactory.create_from_format_name`

    :Example:
        .. code:: python

            >>>dump_tabledata(value)
            .. table:: sample_data

                ======  ======  ======
                attr_a  attr_b  attr_c
                ======  ======  ======
                     1     4.0  a
                     2     2.1  bb
                     3   120.9  ccc
                ======  ======  ======
    """

    import six

    from ._factory import TableWriterFactory

    writer = TableWriterFactory.create_from_format_name(format_name)
    writer.from_tabledata(value)
    writer.stream = six.StringIO()
    writer.write_table()

    return writer.stream.getvalue()
