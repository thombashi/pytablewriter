"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""


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
