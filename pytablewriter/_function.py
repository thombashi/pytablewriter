# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
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
