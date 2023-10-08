import importlib
import pkgutil
import re
from typing import Any, Dict, NamedTuple, Optional, Sequence

from .._logger import logger
from ..style import Cell, Style


try:
    from typing import Protocol
except ImportError:
    # typing.Protocol is only available starting from Python 3.8.
    from .._typing import Protocol  # type: ignore

PLUGIN_NAME_PEFIX = "pytablewriter"
PLUGIN_NAME_SUFFIX = "theme"
KNOWN_PLUGINS = (
    f"{PLUGIN_NAME_PEFIX}_altrow_{PLUGIN_NAME_SUFFIX}",
    f"{PLUGIN_NAME_PEFIX}_altcol_{PLUGIN_NAME_SUFFIX}",
)


class StyleFilterFunc(Protocol):
    def __call__(self, cell: Cell, **kwargs: Any) -> Optional[Style]:
        ...


class ColSeparatorStyleFilterFunc(Protocol):
    def __call__(
        self, left_cell: Optional[Cell], right_cell: Optional[Cell], **kwargs: Any
    ) -> Optional[Style]:
        ...


class CheckStyleFilterKeywordArgsFunc(Protocol):
    def __call__(self, **kwargs: Any) -> None:
        ...


class Theme(NamedTuple):
    style_filter: Optional[StyleFilterFunc]
    col_separator_style_filter: Optional[ColSeparatorStyleFilterFunc]
    check_style_filter_kwargs: Optional[CheckStyleFilterKeywordArgsFunc]


def list_themes() -> Sequence[str]:
    return list(load_ptw_plugins())


def load_ptw_plugins() -> Dict[str, Theme]:
    plugin_regexp = re.compile(
        rf"^{PLUGIN_NAME_PEFIX}[_-].+[_-]{PLUGIN_NAME_SUFFIX}", re.IGNORECASE
    )

    discovered_plugins = {
        name: importlib.import_module(name)
        for _finder, name, _ispkg in pkgutil.iter_modules()
        if plugin_regexp.search(name) is not None
    }

    logger.debug(f"discovered_plugins: {list(discovered_plugins)}")

    themes: Dict[str, Theme] = {}
    for theme, plugin in discovered_plugins.items():
        style_filter = plugin.style_filter if hasattr(plugin, "style_filter") else None
        col_sep_style_filter = (
            plugin.col_separator_style_filter
            if hasattr(plugin, "col_separator_style_filter")
            else None
        )
        check_kwargs_func = (
            plugin.check_style_filter_kwargs
            if hasattr(plugin, "check_style_filter_kwargs")
            else None
        )
        themes[theme] = Theme(style_filter, col_sep_style_filter, check_kwargs_func)

    return themes


def fetch_theme(plugin_name: str) -> Theme:
    loaded_themes = load_ptw_plugins()
    theme_regexp = re.compile(
        rf"^{PLUGIN_NAME_PEFIX}[_-]{plugin_name}[_-]{PLUGIN_NAME_SUFFIX}", re.IGNORECASE
    )
    matched_theme = None

    for loaded_theme in loaded_themes:
        if theme_regexp.search(loaded_theme):
            matched_theme = loaded_theme
            break
    else:
        err_msgs = [f"{plugin_name} theme is not installed."]

        if plugin_name in KNOWN_PLUGINS:
            err_msgs.append(f"try 'pip install {plugin_name}' to install the theme.")

        raise RuntimeError(" ".join(err_msgs))

    return loaded_themes[matched_theme]
