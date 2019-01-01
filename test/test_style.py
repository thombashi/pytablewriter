# encoding: utf-8

from __future__ import print_function, unicode_literals

import pytest
from pytablewriter.style import Align, FontSize, Style, ThousandSeparator


class Test_Style_eq(object):
    @pytest.mark.parametrize(
        ["lhs", "rhs", "expected"],
        [
            [Style(), Style(), True],
            [Style(align=Align.RIGHT), Style(align=Align.RIGHT), True],
            [Style(align=Align.RIGHT), Style(align=Align.LEFT), False],
            [
                Style(thousand_separator=ThousandSeparator.COMMA),
                Style(thousand_separator=ThousandSeparator.COMMA),
                True,
            ],
            [Style(font_size=FontSize.TINY), Style(font_size=FontSize.TINY), True],
            [Style(font_size=FontSize.TINY), Style(font_size=FontSize.LARGE), False],
            [Style(align=Align.RIGHT), Style(align=Align.RIGHT, font_size=FontSize.TINY), False],
            [
                Style(font_size=FontSize.TINY),
                Style(align=Align.RIGHT, font_size=FontSize.TINY),
                False,
            ],
            [
                Style(thousand_separator=ThousandSeparator.COMMA),
                Style(thousand_separator=ThousandSeparator.COMMA, font_size=FontSize.TINY),
                False,
            ],
            [
                Style(align=Align.RIGHT, font_size=FontSize.TINY),
                Style(align=Align.RIGHT, font_size=FontSize.TINY),
                True,
            ],
            [Style(), None, False],
        ],
    )
    def test_normal(self, lhs, rhs, expected):
        assert (lhs == rhs) == expected
        assert (lhs != rhs) != expected

    @pytest.mark.parametrize(
        ["align", "font_size", "thousand_separator", "expected"],
        [
            ["left", None, None, TypeError],
            [FontSize.TINY, None, None, TypeError],
            [None, "small", None, TypeError],
            [None, Align.LEFT, None, TypeError],
            [None, None, "comma", TypeError],
            [None, None, Align.LEFT, TypeError],
        ],
    )
    def test_exception(self, align, font_size, thousand_separator, expected):
        with pytest.raises(expected):
            Style(align=align, font_size=font_size, thousand_separator=thousand_separator)
