import pytest

from pytablewriter import LatexTableWriter
from pytablewriter.style import FontStyle, LatexStyler, Style


class Test_LatexStyler_apply:
    @pytest.mark.parametrize(
        ["value", "style", "expected"],
        [
            ["test", Style(font_style=FontStyle.TYPEWRITER), r"\tt{test}"],
        ],
    )
    def test_normal(self, value, style, expected):
        styler = LatexStyler(writer=LatexTableWriter())
        assert styler.apply(value=value, style=style) == expected
