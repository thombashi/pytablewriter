# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
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
