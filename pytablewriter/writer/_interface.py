# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import abc

import six


@six.add_metaclass(abc.ABCMeta)
class TableWriterInterface(object):
    """
    Interface class of writing table.
    """

    @abc.abstractproperty
    def support_split_write(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def write_table(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def write_table_iter(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def close(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def _write_value_row_separator(self):  # pragma: no cover
        pass


@six.add_metaclass(abc.ABCMeta)
class TextWriterInterface(object):
    """
    Interface class of writing texts.
    """

    @abc.abstractmethod
    def write_null_line(self):  # pragma: no cover
        pass


@six.add_metaclass(abc.ABCMeta)
class IndentationInterface(object):
    """
    Interface class of indentation methods.
    """

    @abc.abstractmethod
    def set_indent_level(self, indent_level):  # pragma: no cover
        pass

    @abc.abstractmethod
    def inc_indent_level(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def dec_indent_level(self):  # pragma: no cover
        pass
