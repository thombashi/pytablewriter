# encoding: utf-8

from __future__ import absolute_import, unicode_literals

import enum

import six
from dataproperty import Align

from ._font import FontSize


@enum.unique
class ThousandSeparator(enum.Enum):
    NONE = 0
    COMMA = 1
    SPACE = 2


_s_to_ts = {"": ThousandSeparator.NONE, ",": ThousandSeparator.COMMA, " ": ThousandSeparator.SPACE}


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
        self.__align = self.__normalize_enum(kwargs.pop("align", None), Align)
        self.__validate_attr("align", Align)

        self.__font_size = self.__normalize_enum(kwargs.pop("font_size", FontSize.NONE), FontSize)
        self.__validate_attr("font_size", FontSize)

        self.__thousand_separator = self.__normalie_thousand_separator(
            self.__normalize_enum(
                kwargs.pop("thousand_separator", ThousandSeparator.NONE), ThousandSeparator
            )
        )

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
                self.align is other.align,
                self.font_size is other.font_size,
                self.thousand_separator is other.thousand_separator,
            ]
        )

    def __ne__(self, other):
        equal = self.__eq__(other)
        return NotImplemented if equal is NotImplemented else not equal

    def __validate_attr(self, attr_name, expected_type):
        value = getattr(self, attr_name)
        if value is not None and not isinstance(value, expected_type):
            raise TypeError("align must be a {} instancce".format(expected_type.__name__))

    @staticmethod
    def __normalize_enum(value, enum_class):
        if value is None or not isinstance(value, six.string_types):
            return value

        for enum_value in enum_class:
            if value.upper() == enum_value.name:
                return enum_value

        return value

    @staticmethod
    def __normalie_thousand_separator(value):
        if isinstance(value, ThousandSeparator):
            return value

        norm_value = _s_to_ts.get(value)
        if norm_value is None:
            return value

        return norm_value
