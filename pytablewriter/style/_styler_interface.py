import abc
from typing import Any, Optional

from ._style import Style


class StylerInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def apply(self, value: Any, style: Style) -> str:  # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def apply_align(self, value: str, style: Style) -> str:  # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def apply_terminal_style(self, value: str, style: Style) -> str:  # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def get_font_size(self, style: Style) -> Optional[str]:  # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def get_additional_char_width(self, style: Style) -> int:  # pragma: no cover
        raise NotImplementedError()
