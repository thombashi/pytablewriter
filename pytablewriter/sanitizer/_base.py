# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import abc
import re

from pathvalidate import InvalidCharError, NullNameError, ReservedNameError
from typepy import is_null_string

from ._interface import NameSanitizer


def _preprocess(name):
    return name.strip()


class VarNameSanitizer(NameSanitizer):
    @abc.abstractproperty
    def _invalid_var_name_head_re(self):  # pragma: no cover
        pass

    @abc.abstractproperty
    def _invalid_var_name_re(self):  # pragma: no cover
        pass

    def validate(self):
        self._validate(self._value)

    def sanitize(self, replacement_text=""):
        sanitized_var_name = self._invalid_var_name_re.sub(replacement_text, self._str)

        # delete invalid char(s) in the beginning of the variable name
        is_require_remove_head = any(
            [
                is_null_string(replacement_text),
                self._invalid_var_name_head_re.search(replacement_text) is not None,
            ]
        )

        if is_require_remove_head:
            sanitized_var_name = self._invalid_var_name_head_re.sub("", sanitized_var_name)
        else:
            match = self._invalid_var_name_head_re.search(sanitized_var_name)
            if match is not None:
                sanitized_var_name = match.end() * replacement_text + self._invalid_var_name_head_re.sub(
                    "", sanitized_var_name
                )

        try:
            self._validate(sanitized_var_name)
        except ReservedNameError as e:
            if e.reusable_name is False:
                sanitized_var_name += "_"
        except NullNameError:
            pass

        return sanitized_var_name

    def _validate(self, value):
        self._validate_null_string(value)

        unicode_var_name = _preprocess(value)

        if self._is_reserved_keyword(unicode_var_name):
            raise ReservedNameError(
                "{:s} is a reserved keyword by python".format(unicode_var_name), reusable_name=False
            )

        match = self._invalid_var_name_re.search(unicode_var_name)
        if match is not None:
            raise InvalidCharError(
                "invalid char found in the variable name: '{}'".format(re.escape(match.group()))
            )

        match = self._invalid_var_name_head_re.search(unicode_var_name)
        if match is not None:
            raise InvalidCharError(
                "the first character of the variable name is invalid: '{}'".format(
                    re.escape(match.group())
                )
            )
