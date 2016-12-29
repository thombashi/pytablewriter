# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from decimal import Decimal

import dataproperty


def _get_data_helper(data_prop):
    if data_prop.typecode == dataproperty.Typecode.FLOAT:
        if isinstance(data_prop.data, Decimal):
            return float(data_prop.data)
    elif data_prop.typecode == dataproperty.Typecode.DATETIME:
        full_format_str = "{:" + data_prop.format_str + "}"
        return full_format_str.format(data_prop.data)

    return data_prop.data


def str_datetime_converter(value):
    return '"{:s}"'.format(value.strftime("%Y-%m-%d %H:%M:%S%z"))


def dateutil_datetime_converter(value):
    return 'dateutil.parser.parse("{:s}")'.format(
        value.strftime("%Y-%m-%dT%H:%M:%S%z"))


def dump_tabledata(tabledata, format_name="rst_grid_table"):
    """
    :param pytablereader.TableData tabledata: Tabular data to dump.
    :param str format_name:
        Dumped format name of tabular data.
        Available formats are as follows:

            - ``csv``
            - ``excel``
            - ``html``
            - ``javascript``
            - ``js``
            - ``json``
            - ``markdown``
            - ``mediawiki``
            - ``null``
            - ``pandas``
            - ``py``/``python``
            - ``rst``/``rst_grid_table``
            - ``rst_csv_table``
            - ``rst_simple_table``

    :Examples:
        .. code:: python

            >>>dump_tabledata(tabledata)
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
    writer.from_tabledata(tabledata)
    writer.stream = six.StringIO()
    writer.write_table()

    return writer.stream.getvalue()
