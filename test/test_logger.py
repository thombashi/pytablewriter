"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""


import pytest

from pytablewriter import set_log_level, set_logger


logbook = pytest.importorskip("logbook", minversion="0.12.3")

import logbook  # isort:skip


class Test_set_logger:
    @pytest.mark.parametrize(["value"], [[True], [False]])
    def test_smoke(self, value):
        set_logger(value)


class Test_set_log_level:
    @pytest.mark.parametrize(
        ["value"],
        [
            [logbook.CRITICAL],
            [logbook.ERROR],
            [logbook.WARNING],
            [logbook.NOTICE],
            [logbook.INFO],
            [logbook.DEBUG],
            [logbook.TRACE],
            [logbook.NOTSET],
        ],
    )
    def test_smoke(self, value):
        set_log_level(value)

    @pytest.mark.parametrize(
        ["value", "expected"], [[None, LookupError], ["unexpected", LookupError]]
    )
    def test_exception(self, value, expected):
        with pytest.raises(expected):
            set_log_level(value)
