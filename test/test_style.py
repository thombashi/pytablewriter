import copy
import sys

import pytest

from pytablewriter.style import (
    Align,
    Cell,
    DecorationLine,
    FontSize,
    FontStyle,
    FontWeight,
    Style,
    ThousandSeparator,
)

from ._common import print_test_result


class Test_Cell_is_header_row:
    @pytest.mark.parametrize(
        ["row", "expected"],
        [[-1, True], [0, False], [sys.maxsize, False]],
    )
    def test_normal(self, row, expected):
        cell = Cell(row=row, col=0, value=None, default_style=None)
        assert cell.is_header_row() is expected


class Test_Style_constructor:
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            [
                {
                    "align": Align.RIGHT,
                    "decoration_line": DecorationLine.LINE_THROUGH,
                    "font_size": FontSize.TINY,
                    "font_weight": FontWeight.BOLD,
                    "thousand_separator": ThousandSeparator.SPACE,
                },
                {
                    "align": Align.RIGHT,
                    "decoration_line": DecorationLine.LINE_THROUGH,
                    "font_size": FontSize.TINY,
                    "font_weight": FontWeight.BOLD,
                    "thousand_separator": ThousandSeparator.SPACE,
                },
            ],
            [
                {
                    "align": "left",
                    "decoration_line": "underline",
                    "font_size": "small",
                    "font_weight": "bold",
                    "thousand_separator": ",",
                },
                {
                    "align": Align.LEFT,
                    "decoration_line": DecorationLine.UNDERLINE,
                    "font_size": FontSize.SMALL,
                    "font_weight": FontWeight.BOLD,
                    "thousand_separator": ThousandSeparator.COMMA,
                },
            ],
            [
                {"font_size": "TINY"},
                {
                    "align": Align.AUTO,
                    "decoration_line": DecorationLine.NONE,
                    "font_size": FontSize.TINY,
                    "font_weight": FontWeight.NORMAL,
                    "thousand_separator": ThousandSeparator.NONE,
                },
            ],
            [
                {
                    "align": None,
                    "font_size": None,
                    "font_weight": None,
                    "thousand_separator": None,
                },
                {
                    "align": Align.AUTO,
                    "decoration_line": DecorationLine.NONE,
                    "font_size": FontSize.NONE,
                    "font_weight": FontWeight.NORMAL,
                    "thousand_separator": ThousandSeparator.NONE,
                },
            ],
        ],
    )
    def test_normal(self, value, expected):
        style = Style(**value)

        print(f"expected: {expected}\nactual: {style}", file=sys.stderr)

        assert style.align is expected.get("align")
        assert style.font_size is expected.get("font_size")
        assert style.font_weight is expected.get("font_weight")
        assert style.thousand_separator is expected.get("thousand_separator")


class Test_Style_eq:
    @pytest.mark.parametrize(
        ["lhs", "rhs", "expected"],
        [
            [Style(), Style(), True],
            [Style(align=Align.RIGHT), Style(align=Align.RIGHT), True],
            [Style(align=Align.RIGHT), Style(align=Align.LEFT), False],
            [Style(align=Align.RIGHT), Style(align="right"), True],
            [Style(align=Align.RIGHT), Style(align=Align.RIGHT, font_size=FontSize.TINY), False],
            [Style(font_size=FontSize.TINY), Style(font_size=FontSize.TINY), True],
            [Style(font_size=FontSize.TINY), Style(font_size="tiny"), True],
            [Style(font_size=FontSize.TINY), Style(font_size=FontSize.LARGE), False],
            [Style(font_weight="bold"), Style(font_weight=FontWeight.BOLD), True],
            [Style(font_weight="bold"), Style(font_weight="normal"), False],
            [Style(font_style="italic"), Style(font_style=FontStyle.ITALIC), True],
            [Style(font_style="italic"), Style(font_style="normal"), False],
            [Style(thousand_separator=","), Style(thousand_separator=","), True],
            [Style(thousand_separator=","), Style(thousand_separator="comma"), True],
            [Style(thousand_separator="_"), Style(thousand_separator="underscore"), True],
            [Style(thousand_separator=""), Style(thousand_separator=","), False],
            [
                Style(thousand_separator=ThousandSeparator.COMMA),
                Style(thousand_separator=ThousandSeparator.COMMA),
                True,
            ],
            [
                Style(thousand_separator="space"),
                Style(thousand_separator=ThousandSeparator.SPACE),
                True,
            ],
            [
                Style(thousand_separator=ThousandSeparator.COMMA),
                Style(thousand_separator=ThousandSeparator.COMMA, font_size=FontSize.TINY),
                False,
            ],
            [
                Style(
                    align=Align.LEFT,
                    font_size=FontSize.TINY,
                    font_style=FontStyle.ITALIC,
                    font_weight=FontWeight.BOLD,
                    thousand_separator=ThousandSeparator.COMMA,
                ),
                Style(
                    align="left",
                    font_size="tiny",
                    font_style="italic",
                    font_weight="bold",
                    thousand_separator=",",
                ),
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
            ["invali", None, None, ValueError],
            [FontSize.TINY, None, None, TypeError],
            [None, 12, None, TypeError],
            [None, Align.LEFT, None, TypeError],
            [None, None, "invalid", TypeError],
        ],
    )
    def test_exception(self, align, font_size, thousand_separator, expected):
        with pytest.raises(expected):
            Style(align=align, font_size=font_size, thousand_separator=thousand_separator)


class Test_Style_repr:
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            [
                Style(
                    align="left",
                    padding=1,
                    vertical_align="bottom",
                    color="red",
                    bg_color="#2f2f2f",
                    decoration_line="line-through",
                    font_size="tiny",
                    font_style="italic",
                    font_weight="bold",
                    thousand_separator=",",
                ),
                "(align=left, padding=1, valign=bottom, "
                "color=Color(code=#cd3131, rgb=(205, 49, 49), name=RED), "
                "bg_color=Color(code=#2f2f2f, rgb=(47, 47, 47)), "
                "decoration_line=line_through, "
                "font_size=tiny, font_style=italic, font_weight=bold, "
                "thousand_separator=comma)",
            ],
            [Style(), "(align=auto, valign=baseline, font_style=normal, font_weight=normal)"],
        ],
    )
    def test_normal(self, value, expected):
        out = str(value)
        print_test_result(expected=expected, actual=out)

        assert out == expected


class Test_Style_update:
    def test_normal(self):
        lhs = Style(
            align="left",
            padding=1,
            vertical_align="bottom",
            color="red",
            bg_color="#2f2f2f",
            decoration_line="line-through",
            font_size="tiny",
            font_style="italic",
            font_weight="bold",
            thousand_separator=",",
        )
        rhs = copy.deepcopy(lhs)
        rhs.update(fg_color="black")
        assert lhs.color != rhs.color
        assert lhs.color == lhs.fg_color
        assert rhs.color == rhs.fg_color
        assert lhs.bg_color == rhs.bg_color

        lhs = Style(
            align="left",
            padding=1,
            vertical_align="bottom",
            fg_color="red",
            bg_color="#2f2f2f",
            decoration_line="line-through",
            font_size="tiny",
            font_style="italic",
            font_weight="bold",
            thousand_separator=",",
        )
        rhs = copy.deepcopy(lhs)
        rhs.update(color="black")
        assert lhs.color != rhs.color
        assert lhs.color == lhs.fg_color
        assert rhs.color == rhs.fg_color
        assert lhs.bg_color == rhs.bg_color
