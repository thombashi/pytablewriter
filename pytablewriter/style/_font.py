# encoding: utf-8

from __future__ import absolute_import

import enum


@enum.unique
class FontSize(enum.Enum):
    NONE = 0
    TINY = 1
    SMALL = 2
    MEDIUM = 3
    LARGE = 4


@enum.unique
class FontWeight(enum.Enum):
    NORMAL = 0
    BOLD = 1
