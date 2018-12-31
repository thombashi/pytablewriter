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
        if self.__align is not None and not isinstance(self.__align, Align):
            return TypeError("align must be a pytablewriter.style.Align instancce")

        self.__font_size = kwargs.pop("font_size", FontSize.NONE)
        if self.__font_size is not None and not isinstance(self.__font_size, FontSize):
            return TypeError("align must be a pytablewriter.style.FontSize instancce")

    def __repr__(self):
        return "{}".format(self.font_size)

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented

        return all([self.align == other.align, self.font_size == other.font_size])

    def __ne__(self, other):
        equal = self.__eq__(other)
        return NotImplemented if equal is NotImplemented else not equal
