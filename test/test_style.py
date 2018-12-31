# encoding: utf-8

from __future__ import print_function, unicode_literals

import pytest
from pytablewriter.style import Align, FontSize, Style


class Test_Style_eq(object):
    @pytest.mark.parametrize(
        ["lhs", "rhs", "expected"],
        [
            [Style(), Style(), True],
            [Style(align=Align.RIGHT), Style(align=Align.RIGHT), True],
            [Style(align=Align.RIGHT), Style(align=Align.LEFT), False],
            [Style(font_size=FontSize.TINY), Style(font_size=FontSize.TINY), True],
            [Style(font_size=FontSize.TINY), Style(font_size=FontSize.LARGE), False],
            [Style(align=Align.RIGHT), Style(align=Align.RIGHT, font_size=FontSize.TINY), False],
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
        ["align", "font_size", "expected"],
        [
            ["left", None, TypeError],
            [FontSize.TINY, None, TypeError],
            [None, "small", TypeError],
            [None, Align.LEFT, TypeError],
        ],
    )
    def test_exception(self, align, font_size, expected):
        with pytest.raises(expected):
            Style(align=align, font_size=font_size)
