# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import enum


@enum.unique
class TableFormat(enum.Enum):
    CSV = "csv"
    ELASTICSEARCH = "elasticsearch"
    EXCEL = "excel"
    HTML = "html"
    JAVASCRIPT = "javascript"
    JAVASCRIPT_ABBR = "js"
    JSON = "json"
    LTSV = "ltsv"
    MARKDOWN = "markdown"
    MEDIAWIKI = "mediawiki"
    NULL = "null"
    PANDAS = "pandas"
    PYTHON = "python"
    PYTHON_ABBR = "py"
    RST = "rst"
    RST_GRID_TABBLE = "rst_grid_table"
    RST_SIMPLE_TABBLE = "rst_simple_table"
    RST_CSV_TABBLE = "rst_csv_table"
    SQLITE = "sqlite"
    TSV = "tsv"
    TOML = "toml"
