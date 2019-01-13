# encoding: utf-8

from __future__ import absolute_import

import enum


@enum.unique
class FontSize(enum.Enum):
    NONE = "none"
    TINY = "tiny"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


@enum.unique
class FontStyle(enum.Enum):
    NORMAL = "normal"
    ITALIC = "italic"


@enum.unique
class FontWeight(enum.Enum):
    NORMAL = "normal"
    BOLD = "bold"
