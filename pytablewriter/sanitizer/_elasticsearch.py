"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import re
from typing import ClassVar, List, Pattern

from ._base import VarNameSanitizer


class ElasticsearchIndexNameSanitizer(VarNameSanitizer):
    __RE_INVALID_INDEX_NAME: ClassVar[Pattern[str]] = re.compile(
        "[" + re.escape('\\/*?"<>|,"') + r"\s]+"
    )
    __RE_INVALID_INDEX_NAME_HEAD: ClassVar[Pattern[str]] = re.compile("^[_]+")

    @property
    def reserved_keywords(self) -> List[str]:
        return []

    @property
    def _invalid_var_name_head_re(self) -> Pattern[str]:
        return self.__RE_INVALID_INDEX_NAME_HEAD

    @property
    def _invalid_var_name_re(self) -> Pattern[str]:
        return self.__RE_INVALID_INDEX_NAME
