# encoding: utf-8

import abc

import six


@six.add_metaclass(abc.ABCMeta)
class BinaryWriterInterface(object):
    @abc.abstractmethod
    def open(self, file_path):  # pragma: no cover
        pass
