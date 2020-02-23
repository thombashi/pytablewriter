import abc
from typing import Any, Optional, cast

from ._font import FontSize, FontStyle, FontWeight
from ._style import Style, ThousandSeparator


class StylerInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def apply(self, value: Any, style: Style) -> str:  # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def get_font_size(self, style: Style) -> Optional[str]:  # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def get_additional_char_width(self, style: Style) -> int:  # pragma: no cover
        raise NotImplementedError()


class AbstractStyler(StylerInterface):
    def __init__(self, writer):
        self._writer = writer
        self._font_size_map = self._get_font_size_map()

    def get_font_size(self, style: Style) -> Optional[str]:
        return self._font_size_map.get(style.font_size)

    def get_additional_char_width(self, style: Style) -> int:
        return 0

    def apply(self, value: Any, style: Style) -> str:
        return value

    def _get_font_size_map(self):
        return {}


class NullStyler(AbstractStyler):
    def get_font_size(self, style: Style) -> Optional[str]:
        return ""


class TextStyler(AbstractStyler):
    def apply(self, value: Any, style: Style) -> str:
        if value and style.thousand_separator == ThousandSeparator.SPACE:
            value = value.replace(",", " ")

        return value


class HtmlStyler(TextStyler):
    def _get_font_size_map(self):
        return {
            FontSize.TINY: "font-size:x-small",
            FontSize.SMALL: "font-size:small",
            FontSize.MEDIUM: "font-size:medium",
            FontSize.LARGE: "font-size:large",
        }


class LatexStyler(TextStyler):
    class Command:
        BOLD = r"\bf"
        ITALIC = r"\it"

    def get_additional_char_width(self, style: Style) -> int:
        width = 0

        if self.get_font_size(style):
            width += len(cast(str, self.get_font_size(style)))

        if style.font_weight == FontWeight.BOLD:
            width += len(self.Command.BOLD)

        if style.font_style == FontStyle.ITALIC:
            width += len(self.Command.ITALIC)

        return width

    def apply(self, value: Any, style: Style) -> str:
        value = super().apply(value, style)
        if not value:
            return value

        font_size = self.get_font_size(style)
        item_list = []

        if font_size:
            item_list.append(font_size)

        if style.font_weight == FontWeight.BOLD:
            item_list.append(self.Command.BOLD)

        if style.font_style == FontStyle.ITALIC:
            item_list.append(self.Command.ITALIC)

        item_list.append(value)
        return " ".join(item_list)

    def _get_font_size_map(self):
        return {
            FontSize.TINY: r"\tiny",
            FontSize.SMALL: r"\small",
            FontSize.MEDIUM: r"\normalsize",
            FontSize.LARGE: r"\large",
        }


class MarkdownStyler(TextStyler):
    def get_additional_char_width(self, style: Style) -> int:
        width = 0

        if style.font_weight == FontWeight.BOLD:
            width += 4

        if style.font_style == FontStyle.ITALIC:
            width += 2

        return width

    def apply(self, value: Any, style: Style) -> str:
        value = super().apply(value, style)
        if not value:
            return value

        if style.font_weight == FontWeight.BOLD:
            value = "**{}**".format(value)

        if style.font_style == FontStyle.ITALIC:
            value = "_{}_".format(value)

        return value


class ReStructuredTextStyler(TextStyler):
    def get_additional_char_width(self, style: Style) -> int:
        from ..writer import RstCsvTableWriter

        width = 0

        if style.font_weight == FontWeight.BOLD:
            width += 4
        elif style.font_style == FontStyle.ITALIC:
            width += 2

        if (
            style.thousand_separator == ThousandSeparator.COMMA
            and self._writer.format_name == RstCsvTableWriter.FORMAT_NAME
        ):
            width += 2

        return width

    def apply(self, value: Any, style: Style) -> str:
        from ..writer import RstCsvTableWriter

        value = super().apply(value, style)
        if not value:
            return value

        if style.font_weight == FontWeight.BOLD:
            value = "**{}**".format(value)
        elif style.font_style == FontStyle.ITALIC:
            # in reStructuredText, some custom style definition will be required to
            # set for both bold and italic (currently not supported)
            value = "*{}*".format(value)

        if (
            style.thousand_separator == ThousandSeparator.COMMA
            and self._writer.format_name == RstCsvTableWriter.FORMAT_NAME
        ):
            value = '"{}"'.format(value)

        return value
