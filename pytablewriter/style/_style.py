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
