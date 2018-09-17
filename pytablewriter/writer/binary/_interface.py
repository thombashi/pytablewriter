# encoding: utf-8

import abc

import six

from .._table_writer import AbstractTableWriter


@six.add_metaclass(abc.ABCMeta)
class BinaryWriterInterface(object):
    @abc.abstractmethod
    def open(self, file_path):  # pragma: no cover
        pass


class AbstractBinaryTableWriter(AbstractTableWriter, BinaryWriterInterface):
    def dumps(self):
        raise NotImplementedError()
