# encoding: utf-8

from __future__ import absolute_import, unicode_literals

from dataproperty import Align

from ._font import FontSize


class Style(object):
    @property
    def align(self):
        return self.__align

    @property
    def font_size(self):
        return self.__font_size

    def __init__(self, **kwargs):
        self.__align = kwargs.pop("align", None)
        self.__validate_attr("align", Align)

        self.__font_size = kwargs.pop("font_size", FontSize.NONE)
        self.__validate_attr("font_size", FontSize)

    def __repr__(self):
        return "{}".format(self.font_size)

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented

        return all([self.align == other.align, self.font_size == other.font_size])

    def __ne__(self, other):
        equal = self.__eq__(other)
        return NotImplemented if equal is NotImplemented else not equal

    def __validate_attr(self, attr_name, expected_type):
        value = getattr(self, attr_name)
        if value is not None and not isinstance(value, expected_type):
            raise TypeError("align must be a {} instancce".format(type(expected_type)))
