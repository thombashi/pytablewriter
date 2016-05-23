# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import


class EmptyTableNameError(Exception):
    """
    Raised when a table writer class of the |table_name| attribute is empty
    and the writer is not permitted empty |table_name|.
    """


class EmptyHeaderError(Exception):
    """
    Raised when a table writer class of the |header_list| attribute is empty
    and the writer is not permitted empty |header_list|.
    """


class EmptyValueError(Exception):
    """
    Raised when a table writer class of the |value_matrix| attribute is empty.
    """
