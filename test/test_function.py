from textwrap import dedent

import pytest
from tabledata import TableData

from pytablewriter import dumps_tabledata

from ._common import print_test_result


test_tabledata = TableData(
    "fake name and address",
    ("name", "address"),
    [
        ("vRyan Gallagher", "6317 Mary Light\nSmithview, HI 13900"),
        ("Amanda Johnson", "3608 Samuel Mews Apt. 337\nHousebury, WA 13608"),
    ],
)


class Test_dump_tabledata:
    @pytest.mark.parametrize(
        ["value", "format_name", "expected"],
        [
            [
                test_tabledata,
                "markdown",
                dedent(
                    """\
                    # fake name and address
                    |     name      |                   address                   |
                    |---------------|---------------------------------------------|
                    |vRyan Gallagher|6317 Mary Light Smithview, HI 13900          |
                    |Amanda Johnson |3608 Samuel Mews Apt. 337 Housebury, WA 13608|
                    """
                ),
            ]
        ],
    )
    def test_normal_format_name(self, value, format_name, expected):
        out = dumps_tabledata(value, format_name=format_name)
        print_test_result(expected=expected, actual=out)

        assert out == expected

    @pytest.mark.parametrize(
        ["value", "kwargs", "expected"],
        [
            [
                test_tabledata,
                {},
                dedent(
                    """\
                    .. table:: fake name and address

                        +---------------+---------------------------------------------+
                        |     name      |                   address                   |
                        +===============+=============================================+
                        |vRyan Gallagher|6317 Mary Light Smithview, HI 13900          |
                        +---------------+---------------------------------------------+
                        |Amanda Johnson |3608 Samuel Mews Apt. 337 Housebury, WA 13608|
                        +---------------+---------------------------------------------+
                    """
                ),
            ],
        ],
    )
    def test_normal_kwargs(self, value, kwargs, expected):
        out = dumps_tabledata(value, **kwargs)
        print_test_result(expected=expected, actual=out)

        assert out == expected

    @pytest.mark.parametrize(["value", "expected"], [[None, TypeError]])
    def test_exception(self, value, expected):
        with pytest.raises(expected):
            dumps_tabledata(value)
