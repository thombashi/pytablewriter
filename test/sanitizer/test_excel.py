"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import itertools
import random

import pytest
from pathvalidate.error import ErrorReason, ValidationError

from pytablewriter.sanitizer import sanitize_excel_sheet_name, validate_excel_sheet_name

from ._common import VALID_PATH_CHARS, make_random_str


random.seed(0)

INVALID_EXCEL_CHARS = ["[", "]", ":", "*", "?", "/", "\\"]


class Test_validate_excel_sheet_name:
    VALID_CHAR_LIST = set(VALID_PATH_CHARS).difference(set(INVALID_EXCEL_CHARS))
    INVALID_CHAR_LIST = INVALID_EXCEL_CHARS

    @pytest.mark.parametrize(
        ["value"],
        [
            [make_random_str(15) + invalid_char + make_random_str(15)]
            for invalid_char in VALID_CHAR_LIST
        ],
    )
    def test_normal(self, value):
        validate_excel_sheet_name(value)

    @pytest.mark.parametrize(["value"], [["あいうえお"], ["シート"]])
    def test_normal_multibyte(self, value):
        validate_excel_sheet_name(value)

    @pytest.mark.parametrize(
        ["value"],
        [
            [make_random_str(15) + invalid_char + make_random_str(15)]
            for invalid_char in INVALID_CHAR_LIST
        ],
    )
    def test_exception_invalid_char(self, value):
        with pytest.raises(ValidationError) as e:
            validate_excel_sheet_name(value)
        assert e.value.reason == ErrorReason.INVALID_CHARACTER

    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            [None, ValidationError],
            ["", ValidationError],
            [1, TypeError],
            [True, TypeError],
            ["a" * 32, ValidationError],
        ],
    )
    def test_exception(self, value, expected):
        with pytest.raises(expected):
            validate_excel_sheet_name(value)


class Test_sanitize_excel_sheet_name:
    SANITIZE_CHAR_LIST = INVALID_EXCEL_CHARS
    NOT_SANITIZE_CHAR_LIST = set(VALID_PATH_CHARS).difference(set(INVALID_EXCEL_CHARS))
    REPLACE_TEXT_LIST = ["", "_"]

    @pytest.mark.parametrize(
        ["value", "replace_text", "expected"],
        [
            ["A" + c + "B", rep, "A" + rep + "B"]
            for c, rep in itertools.product(SANITIZE_CHAR_LIST, REPLACE_TEXT_LIST)
        ]
        + [
            ["A" + c + "B", rep, "A" + c + "B"]
            for c, rep in itertools.product(NOT_SANITIZE_CHAR_LIST, REPLACE_TEXT_LIST)
        ]
        + [["a" * 32, "", "a" * 31]],
    )
    def test_normal(self, value, replace_text, expected):
        sanitized_name = sanitize_excel_sheet_name(value, replace_text)
        assert sanitized_name == expected
        validate_excel_sheet_name(sanitized_name)

    @pytest.mark.parametrize(["value", "expected"], [["あい*うえお", "あいうえお"], ["シー?ト", "シート"]])
    def test_normal_multibyte(self, value, expected):
        sanitize_excel_sheet_name(value)

    @pytest.mark.parametrize(
        ["value", "expected"], [[None, ValueError], [1, ValueError], [True, ValueError]]
    )
    def test_exception_type(self, value, expected):
        with pytest.raises(expected):
            sanitize_excel_sheet_name(value)
