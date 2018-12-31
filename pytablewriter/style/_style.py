# encoding: utf-8

from __future__ import absolute_import, unicode_literals

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
        self.__font_size = kwargs.pop("font_size", FontSize.NONE)

    def __repr__(self):
        return "{}".format(self.font_size)
