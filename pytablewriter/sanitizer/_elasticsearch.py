# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, unicode_literals

import re

from ._base import VarNameSanitizer


class ElasticsearchIndexNameSanitizer(VarNameSanitizer):

    __RE_INVALID_INDEX_NAME = re.compile("[" + re.escape('\\/*?"<>|,"') + r"\s]+")
    __RE_INVALID_INDEX_NAME_HEAD = re.compile("^[_]+")

    @property
    def reserved_keywords(self):
        return []

    @property
    def _invalid_var_name_head_re(self):
        return self.__RE_INVALID_INDEX_NAME_HEAD

    @property
    def _invalid_var_name_re(self):
        return self.__RE_INVALID_INDEX_NAME
