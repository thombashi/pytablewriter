# encoding: utf-8

from __future__ import absolute_import, unicode_literals

import abc

import six

from ._font import FontSize, FontStyle, FontWeight
from ._style import Style, ThousandSeparator


@six.add_metaclass(abc.ABCMeta)
class StylerInterface(object):
    @abc.abstractmethod
    def apply(self, value):  # pragma: no cover
        raise NotImplementedError()

    @abc.abstractproperty
    def font_size(self):  # pragma: no cover
        raise NotImplementedError()

    @abc.abstractproperty
    def additional_char_width(self):  # pragma: no cover
        raise NotImplementedError()


class AbstractStyler(StylerInterface):
    @property
    def _font_size_map(self):
        return {}

    @property
    def font_size(self):
        return self._font_size_map.get(self._style.font_size)

    @property
    def additional_char_width(self):
        return 0

    def __init__(self, style, writer):
        if not isinstance(style, Style):
            raise TypeError("style must be a Style instance")

        self._style = style
        self._writer = writer

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
    class Command(object):
        BOLD = r"\bf"
        ITALIC = r"\it"

    @property
    def _font_size_map(self):
        return {
            FontSize.TINY: r"\tiny",
            FontSize.SMALL: r"\small",
            FontSize.MEDIUM: r"\normalsize",
            FontSize.LARGE: r"\large",
        }

    @property
    def additional_char_width(self):
        width = 0

        if self.font_size:
            width += len(self.font_size)

        if self._style.font_weight == FontWeight.BOLD:
            width += len(self.Command.BOLD)

        if self._style.font_style == FontStyle.ITALIC:
            width += len(self.Command.ITALIC)

        return width

    def apply(self, value):
        value = super(LatexStyler, self).apply(value)
        if not value:
            return value

        font_size = self.font_size
        item_list = []

        if font_size:
            item_list.append(font_size)

        if self._style.font_weight == FontWeight.BOLD:
            item_list.append(self.Command.BOLD)

        if self._style.font_style == FontStyle.ITALIC:
            item_list.append(self.Command.ITALIC)

        item_list.append(value)
        return " ".join(item_list)


class MarkdownStyler(TextStyler):
    @property
    def additional_char_width(self):
        width = 0

        if self._style.font_weight == FontWeight.BOLD:
            width += 4

        if self._style.font_style == FontStyle.ITALIC:
            width += 2

        return width

    def apply(self, value):
        value = super(MarkdownStyler, self).apply(value)
        if not value:
            return value

        if self._style.font_weight == FontWeight.BOLD:
            value = "**{}**".format(value)

        if self._style.font_style == FontStyle.ITALIC:
            value = "_{}_".format(value)

        return value


class ReStructuredTextStyler(TextStyler):
    @property
    def additional_char_width(self):
        from ..writer import RstCsvTableWriter

        width = 0

        if self._style.font_weight == FontWeight.BOLD:
            width += 4
        elif self._style.font_style == FontStyle.ITALIC:
            width += 2

        if (
            self._style.thousand_separator == ThousandSeparator.COMMA
            and self._writer.format_name == RstCsvTableWriter.FORMAT_NAME
        ):
            width += 2

        return width

    def apply(self, value):
        from ..writer import RstCsvTableWriter

        value = super(ReStructuredTextStyler, self).apply(value)
        if not value:
            return value

        if self._style.font_weight == FontWeight.BOLD:
            value = "**{}**".format(value)
        elif self._style.font_style == FontStyle.ITALIC:
            # in reStructuredText, some custom style definition will be required to
            # set for both bold and italic (currently not supported)
            value = "*{}*".format(value)

        if (
            self._style.thousand_separator == ThousandSeparator.COMMA
            and self._writer.format_name == RstCsvTableWriter.FORMAT_NAME
        ):
            value = '"{}"'.format(value)

        return value
