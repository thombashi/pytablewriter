# encoding: utf-8

from __future__ import absolute_import, unicode_literals

import abc

import six

from ._font import FontSize
from ._style import Style, ThousandSeparator


@six.add_metaclass(abc.ABCMeta)
class StylerInterface(object):
    @abc.abstractmethod
    def apply(self, value):  # pragma: no cover
        raise NotImplementedError()

    @abc.abstractproperty
    def font_size(self):  # pragma: no cover
        raise NotImplementedError()


class AbstractStyler(StylerInterface):
    @property
    def _font_size_map(self):
        return {}

    @property
    def font_size(self):
        return self._font_size_map.get(self._style.font_size)

    def __init__(self, style):
        if not isinstance(style, Style):
            raise TypeError("style must be a Style instance")

        self._style = style

    def apply(self, value):
        return value


class NullStyler(AbstractStyler):
    @property
    def font_size(self):
        return self._style.font_size


class TextStyler(AbstractStyler):
    def apply(self, value):
        if value and self._style.thousand_separator == ThousandSeparator.SPACE:
            value = value.replace(",", " ")

        return value


class HtmlStyler(TextStyler):
    @property
    def _font_size_map(self):
        return {
            FontSize.TINY: "font-size:x-small",
            FontSize.SMALL: "font-size:small",
            FontSize.MEDIUM: "font-size:medium",
            FontSize.LARGE: "font-size:large",
        }


class LatexStyler(TextStyler):
    @property
    def _font_size_map(self):
        return {
            FontSize.TINY: r"\tiny",
            FontSize.SMALL: r"\small",
            FontSize.MEDIUM: r"\normalsize",
            FontSize.LARGE: r"\large",
        }

    def apply(self, value):
        value = super(LatexStyler, self).apply(value)
        font_size = self.font_size

        if font_size is None:
            return value

        return "{style} {value}".format(style=font_size, value=value)
