# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import dataproperty
import six


def quote_datetime_formatter(value):
    return '"{:s}"'.format(value.strftime(dataproperty.DefaultValue.DATETIME_FORMAT))


def dateutil_datetime_formatter(value):
    return 'dateutil.parser.parse("{:s}")'.format(
        value.strftime(dataproperty.DefaultValue.DATETIME_FORMAT)
    )


def dump_tabledata(value, format_name="rst_grid_table", **kwargs):
    """
    :param tabledata.TableData value: Tabular data to dump.
    :param str format_name:
        Dumped format name of tabular data.
        Available formats are described in
        :py:meth:`~pytablewriter.TableWriterFactory.create_from_format_name`

    :Example:
        .. code:: python

            >>> dump_tabledata(value)
            .. table:: sample_data

                ======  ======  ======
                attr_a  attr_b  attr_c
                ======  ======  ======
                     1     4.0  a
                     2     2.1  bb
                     3   120.9  ccc
                ======  ======  ======
    """

    from ._factory import TableWriterFactory

    if not value:
        raise TypeError("value must be a tabledata.TableData instance")

    writer = TableWriterFactory.create_from_format_name(format_name)

    for attr_name, attr_value in kwargs.items():
        setattr(writer, attr_name, attr_value)

    writer.from_tabledata(value)

    return writer.dumps()


def normalize_enum(value, enum_class):
    if value is None or not isinstance(value, six.string_types):
        return value

    try:
        return enum_class[value.upper()]
    except KeyError:
        return value
