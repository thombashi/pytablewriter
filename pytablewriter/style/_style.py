# encoding: utf-8

from __future__ import absolute_import, unicode_literals

import enum

from dataproperty import Align

from ._font import FontSize


@enum.unique
class ThousandSeparator(enum.Enum):
    NONE = 0
    COMMA = 1
    SPACE = 2


class Style(object):
    @property
    def align(self):
        return self.__align

    @property
    def font_size(self):
        return self.__font_size

    @property
    def thousand_separator(self):
        return self.__thousand_separator

    def __init__(self, **kwargs):
        self.__align = kwargs.pop("align", None)
        self.__validate_attr("align", Align)

        self.__font_size = kwargs.pop("font_size", FontSize.NONE)
        self.__validate_attr("font_size", FontSize)

        self.__thousand_separator = kwargs.pop("thousand_separator", ThousandSeparator.NONE)
        self.__validate_attr("thousand_separator", ThousandSeparator)

    def __repr__(self):
        return "align={}, font_size={}, thousand_separator={}".format(
            self.align, self.font_size, self.thousand_separator
        )

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented

        return all(
            [
                self.align == other.align,
                self.font_size == other.font_size,
                self.thousand_separator == other.thousand_separator,
            ]
        )

    def __ne__(self, other):
        equal = self.__eq__(other)
        return NotImplemented if equal is NotImplemented else not equal

    def __validate_attr(self, attr_name, expected_type):
        value = getattr(self, attr_name)
        if value is not None and not isinstance(value, expected_type):
            raise TypeError("align must be a {} instancce".format(type(expected_type)))
