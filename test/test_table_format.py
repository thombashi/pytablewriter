"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import pytest

from pytablewriter import FormatAttr, TableFormat


class Test_TableFormat_search_table_format:
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            [
                FormatAttr.TEXT,
                [
                    TableFormat.ASCIIDOC,
                    TableFormat.BOLD_UNICODE,
                    TableFormat.BORDERLESS,
                    TableFormat.CSS,
                    TableFormat.CSV,
                    TableFormat.HTML,
                    TableFormat.JAVASCRIPT,
                    TableFormat.JSON,
                    TableFormat.JSON_LINES,
                    TableFormat.LATEX_MATRIX,
                    TableFormat.LATEX_TABLE,
                    TableFormat.LTSV,
                    TableFormat.MARKDOWN,
                    TableFormat.MEDIAWIKI,
                    TableFormat.NUMPY,
                    TableFormat.PANDAS,
                    TableFormat.PYTHON,
                    TableFormat.RST_CSV_TABLE,
                    TableFormat.RST_GRID_TABLE,
                    TableFormat.RST_SIMPLE_TABLE,
                    TableFormat.SPACE_ALIGNED,
                    TableFormat.TOML,
                    TableFormat.TSV,
                    TableFormat.UNICODE,
                    TableFormat.YAML,
                ],
            ],
            [
                FormatAttr.FILE,
                [
                    TableFormat.ASCIIDOC,
                    TableFormat.CSS,
                    TableFormat.CSV,
                    TableFormat.EXCEL_XLS,
                    TableFormat.EXCEL_XLSX,
                    TableFormat.HTML,
                    TableFormat.JAVASCRIPT,
                    TableFormat.JSON,
                    TableFormat.JSON_LINES,
                    TableFormat.LATEX_MATRIX,
                    TableFormat.LATEX_TABLE,
                    TableFormat.LTSV,
                    TableFormat.MARKDOWN,
                    TableFormat.MEDIAWIKI,
                    TableFormat.NUMPY,
                    TableFormat.PANDAS,
                    TableFormat.PANDAS_PICKLE,
                    TableFormat.PYTHON,
                    TableFormat.RST_CSV_TABLE,
                    TableFormat.RST_GRID_TABLE,
                    TableFormat.RST_SIMPLE_TABLE,
                    TableFormat.SPACE_ALIGNED,
                    TableFormat.SQLITE,
                    TableFormat.TOML,
                    TableFormat.TSV,
                    TableFormat.YAML,
                ],
            ],
            [
                FormatAttr.BIN,
                [
                    TableFormat.EXCEL_XLS,
                    TableFormat.EXCEL_XLSX,
                    TableFormat.SQLITE,
                    TableFormat.PANDAS_PICKLE,
                ],
            ],
            [FormatAttr.API, [TableFormat.ELASTICSEARCH]],
            [0, []],
        ],
    )
    def test_normal(self, value, expected):
        assert set(TableFormat.find_all_attr(value)) == set(expected)


class Test_TableFormat_from_name:
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["csv", TableFormat.CSV],
            ["CSV", TableFormat.CSV],
            ["excel", TableFormat.EXCEL_XLSX],
        ],
    )
    def test_normal(self, value, expected):
        assert TableFormat.from_name(value) == expected


class Test_TableFormat_from_file_extension:
    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            ["csv", TableFormat.CSV],
            [".CSV", TableFormat.CSV],
            ["xlsx", TableFormat.EXCEL_XLSX],
            ["md", TableFormat.MARKDOWN],
        ],
    )
    def test_normal(self, value, expected):
        assert TableFormat.from_file_extension(value) == expected
