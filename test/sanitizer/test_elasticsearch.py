"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import itertools

import pytest

from pytablewriter.sanitizer import ElasticsearchIndexNameSanitizer


INVALID_ES_CHARS = ["\\", "," "*", "?", '"', "<", ">", "|", " "]


class Test_ElasticsearchIndexNameSanitizer:
    SANITIZE_CHAR_LIST = INVALID_ES_CHARS
    NOT_SANITIZE_CHAR_LIST = ["_"]
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
        ],
    )
    def test_normal(self, value, replace_text, expected):
        sanitized_name = ElasticsearchIndexNameSanitizer(value).sanitize(replace_text)

        assert sanitized_name == expected

        ElasticsearchIndexNameSanitizer(sanitized_name).validate()

    @pytest.mark.parametrize(
        ["value", "replace_text", "expected"],
        [[invalid_char + "hoge_123", "_", "hoge_123"] for invalid_char in "_"]
        + [[invalid_char + "hoge_123", "a", "ahoge_123"] for invalid_char in "_"],
    )
    def test_normal_invalid_first_char_x1(self, value, replace_text, expected):
        sanitized_name = ElasticsearchIndexNameSanitizer(value).sanitize(replace_text)

        assert sanitized_name == expected

        ElasticsearchIndexNameSanitizer(sanitized_name).validate()

    @pytest.mark.parametrize(
        ["value", "replace_text", "expected"],
        [[invalid_char * 2 + "hoge_123", "_", "hoge_123"] for invalid_char in "_"]
        + [[invalid_char * 2 + "hoge_123", "a", "aahoge_123"] for invalid_char in "_"],
    )
    def test_normal_invalid_first_char_x2(self, value, replace_text, expected):
        sanitized_name = ElasticsearchIndexNameSanitizer(value).sanitize(replace_text)

        assert sanitized_name == expected

        ElasticsearchIndexNameSanitizer(sanitized_name).validate()

    @pytest.mark.parametrize(
        ["value", "expected"], [[None, ValueError], [1, TypeError], [True, TypeError]]
    )
    def test_exception_type(self, value, expected):
        with pytest.raises(expected):
            ElasticsearchIndexNameSanitizer(value).validate()
