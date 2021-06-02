import importlib
import pkgutil
import re
from collections import namedtuple
from typing import Any, Dict, Optional, Sequence

from .._logger import logger
from ..style import Cell, Style


try:
    from typing import Protocol
except ImportError:
    # typing.Protocol is only available starting from Python 3.8.
    from .._typing import Protocol  # noqa


KNOWN_PLUGINS = ("altrow",)

Theme = namedtuple("Theme", "style_filter col_separator_style_filter")


class StyleFilterFunc(Protocol):
    def __call__(self, cell: Cell, **kwargs: Any) -> Optional[Style]:
        ...


class ColSeparatorStyleFilterFunc(Protocol):
    def __call__(
        self, left_cell: Optional[Cell], right_cell: Optional[Cell], **kwargs: Any
    ) -> Optional[Style]:
        ...


def list_themes() -> Sequence[str]:
    return list(load_ptw_plugins())


def load_ptw_plugins() -> Dict[str, Theme]:
    plugin_regexp = re.compile("^pytablewriter_.+_theme", re.IGNORECASE)
    discovered_plugins = {
        name: importlib.import_module(name)
        for finder, name, ispkg in pkgutil.iter_modules()
        if plugin_regexp.search(name) is not None
    }

    logger.debug(f"discovered_plugins: {list(discovered_plugins)}")

    return {
        theme: Theme(
            plugin.style_filter if hasattr(plugin, "style_filter") else None,  # type: ignore
            plugin.col_separator_style_filter  # type: ignore
            if hasattr(plugin, "col_separator_style_filter")
            else None,
        )
        for theme, plugin in discovered_plugins.items()
    }


def fetch_theme(plugin_name: str) -> Theme:
    loaded_themes = load_ptw_plugins()

    if plugin_name not in loaded_themes:
        err_msgs = [f"{plugin_name} theme not installed."]

        if plugin_name in KNOWN_PLUGINS:
            err_msgs.append(f"try 'pip install {plugin_name}'")

        raise RuntimeError(" ".join(err_msgs))

    return loaded_themes[plugin_name]
