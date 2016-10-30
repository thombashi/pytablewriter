# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import


class NotSupportedError(Exception):
    pass


class EmptyTableNameError(Exception):
    """
    Raised when a table writer class of the |table_name| attribute is null
    and the class is not accepted null |table_name|.
    """


class EmptyHeaderError(Exception):
    """
    Raised when a table writer class of the |header_list| attribute is null
    and the class is not accepted null |header_list|.
    """


class EmptyValueError(Exception):
    """
    Raised when a table writer class of the |value_matrix| attribute is null
    and the class is not accepted null |value_matrix|.
    """


class EmptyTableDataError(Exception):
    """
    Raised when a table writer class of the |header_list| and |value_matrix|
    attributes are null
    """


class WriterNotFoundError(Exception):
    """
    Raised when appropriate loader writer found.
    """
