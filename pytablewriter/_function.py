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

    return data_prop.data
