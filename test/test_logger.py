# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import print_function
from __future__ import unicode_literals

import logbook
from pytablewriter import (
    set_logger,
    set_log_level,
)
import pytest


class Test_set_logger(object):

    @pytest.mark.parametrize(["value"], [
        [True],
        [False],
    ])
    def test_smoke(self, value):
        set_logger(value)


class Test_set_log_level(object):

    @pytest.mark.parametrize(["value"], [
        [logbook.CRITICAL],
        [logbook.ERROR],
        [logbook.WARNING],
        [logbook.NOTICE],
        [logbook.INFO],
        [logbook.DEBUG],
        [logbook.TRACE],
        [logbook.NOTSET],
    ])
    def test_smoke(self, value):
        set_log_level(value)

    @pytest.mark.parametrize(["value", "expected"], [
        [None, LookupError],
        ["unexpected", LookupError],
    ])
    def test_exception(self, value, expected):
        with pytest.raises(expected):
            set_log_level(value)
