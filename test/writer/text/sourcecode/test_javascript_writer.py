"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import collections
import datetime
from textwrap import dedent

import pytest
import typepy

import pytablewriter

from ...._common import print_test_result
from ....data import (
    headers,
    mix_header_list,
    mix_value_matrix,
    value_matrix,
    value_matrix_iter,
    value_matrix_with_none,
)


Data = collections.namedtuple(
    "Data", "table indent header value is_write_header is_dti_fmt expected"
)

normal_test_data_list = [
    Data(
        table="table-name ho'ge",
        indent=0,
        header=headers,
        value=value_matrix,
        is_write_header=True,
        is_dti_fmt=True,
        expected=dedent(
            """\
            const table_name_ho_ge = [
                ["a", "b", "c", "dd", "e"],
                [1, 123.1, "a", 1, 1],
                [2, 2.2, "bb", 2.2, 2.2],
                [3, 3.3, "ccc", 3, "cccc"]
            ];
            """
        ),
    ),
    Data(
        table="null value",
        indent=0,
        header=headers,
        value=None,
        is_write_header=True,
        is_dti_fmt=True,
        expected=dedent(
            """\
            const null_value = [
                ["a", "b", "c", "dd", "e"]
            ];
            """
        ),
    ),
    Data(
        table="null table",
        indent=0,
        header=headers,
        value=None,
        is_write_header=False,
        is_dti_fmt=True,
        expected=dedent(
            """\
            const null_table = [
            ];
            """
        ),
    ),
    Data(
        table="table name",
        indent=0,
        header=None,
        value=value_matrix,
        is_write_header=True,
        is_dti_fmt=True,
        expected=dedent(
            """\
            const table_name = [
                [1, 123.1, "a", 1, 1],
                [2, 2.2, "bb", 2.2, 2.2],
                [3, 3.3, "ccc", 3, "cccc"]
            ];
            """
        ),
    ),
    Data(
        table="tablename",
        indent=1,
        header=headers,
        value=value_matrix,
        is_write_header=True,
        is_dti_fmt=True,
        expected="""\
    const tablename = [
        ["a", "b", "c", "dd", "e"],
        [1, 123.1, "a", 1, 1],
        [2, 2.2, "bb", 2.2, 2.2],
        [3, 3.3, "ccc", 3, "cccc"]
    ];
""",
    ),
    Data(
        table="tablename",
        indent=0,
        header=headers,
        value=value_matrix_with_none,
        is_write_header=True,
        is_dti_fmt=True,
        expected=dedent(
            """\
            const tablename = [
                ["a", "b", "c", "dd", "e"],
                [1, null, "a", 1, null],
                [null, 2.2, null, 2.2, 2.2],
                [3, 3.3, "ccc", null, "cccc"],
                [null, null, null, null, null]
            ];
            """
        ),
    ),
    Data(
        table="tablename",
        indent=0,
        header=mix_header_list,
        value=mix_value_matrix,
        is_write_header=True,
        is_dti_fmt=True,
        expected=dedent(
            """\
            const tablename = [
                ["i", "f", "c", "if", "ifc", "bool", "inf", "nan", "mix_num", "time"],
                [1, 1.1, "aa", 1, 1, true, Infinity, NaN, 1, new Date("2017-01-01T00:00:00")],
                [2, 2.2, "bbb", 2.2, 2.2, false, Infinity, NaN, Infinity, "2017-01-02 03:04:05+09:00"],
                [3, 3.33, "cccc", -3, "ccc", true, Infinity, NaN, NaN, new Date("2017-01-01T00:00:00")]
            ];
            """
        ),
    ),
    Data(
        table="tablename",
        indent=0,
        header=mix_header_list,
        value=mix_value_matrix,
        is_write_header=True,
        is_dti_fmt=False,
        expected=dedent(
            """\
            const tablename = [
                ["i", "f", "c", "if", "ifc", "bool", "inf", "nan", "mix_num", "time"],
                [1, 1.1, "aa", 1, 1, true, Infinity, NaN, 1, "2017-01-01T00:00:00"],
                [2, 2.2, "bbb", 2.2, 2.2, false, Infinity, NaN, Infinity, "2017-01-02 03:04:05+09:00"],
                [3, 3.33, "cccc", -3, "ccc", true, Infinity, NaN, NaN, "2017-01-01T00:00:00"]
            ];
            """
        ),
    ),
    Data(
        table="float-with-null",
        indent=0,
        header=["a", "b"],
        value=[
            ["0.03785679191278808", "826.21158713263"],
            [None, "826.21158713263"],
            [0.1, "1.0499675627886724"],
        ],
        is_write_header=True,
        is_dti_fmt=False,
        expected=dedent(
            """\
            const float_with_null = [
                ["a", "b"],
                [0.03785679191278808, 826.21158713263],
                [null, 826.21158713263],
                [0.1, 1.0499675627886724]
            ];
            """
        ),
    ),
    Data(
        table="line breaks",
        indent=0,
        header=["a\nb", "\nc\n\nd\n", "e\r\nf"],
        value=[["v1\nv1", "v2\n\nv2", "v3\r\nv3"]],
        is_write_header=True,
        is_dti_fmt=False,
        expected=dedent(
            """\
            const line_breaks = [
                ["a b", " c  d ", "e f"],
                ["v1 v1", "v2  v2", "v3 v3"]
            ];
            """
        ),
    ),
    Data(
        table="empty",
        indent=0,
        header=[],
        value=[],
        is_write_header=False,
        is_dti_fmt=False,
        expected="",
    ),
]

exception_test_data_list = [
    Data(
        table="",
        indent=normal_test_data_list[0].indent,
        header=normal_test_data_list[0].header,
        value=normal_test_data_list[0].value,
        is_write_header=True,
        is_dti_fmt=True,
        expected=pytablewriter.EmptyTableNameError,
    )
]

table_writer_class = pytablewriter.JavaScriptTableWriter


class Test_JavaScriptTableWriter_write_new_line:
    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_JavaScriptTableWriter_type_hint:
    DATATIME_DATA = datetime.datetime(2017, 1, 2, 3, 4, 5)
    STR_DATA = "2017-01-02 03:04:05"
    DATA_MATRIX = [[STR_DATA, DATATIME_DATA], [STR_DATA, DATATIME_DATA]]

    @pytest.mark.parametrize(
        ["table", "header", "value", "type_hint", "expected"],
        [
            [
                "th_none_none",
                ["string", "datetime"],
                DATA_MATRIX,
                [None, None],
                dedent(
                    """\
                    const th_none_none = [
                        ["string", "datetime"],
                        ["2017-01-02 03:04:05", new Date("2017-01-02T03:04:05")],
                        ["2017-01-02 03:04:05", new Date("2017-01-02T03:04:05")]
                    ];
                    """
                ),
            ],
            [
                "typehint_datetime-string",
                ["string", "datetime"],
                DATA_MATRIX,
                [typepy.DateTime, typepy.String],
                dedent(
                    """\
                    const typehint_datetime_string = [
                        ["string", "datetime"],
                        [new Date("2017-01-02T03:04:05"), "2017-01-02 03:04:05"],
                        [new Date("2017-01-02T03:04:05"), "2017-01-02 03:04:05"]
                    ];
                    """
                ),
            ],
        ],
    )
    def test_normal(self, capsys, table, header, value, type_hint, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.headers = header
        writer.value_matrix = value
        writer.type_hints = type_hint

        writer.write_table()

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected
        assert writer.dumps() == expected
        assert str(writer) == expected

        # margin setting must be ignored
        writer.margin = 1
        out = writer.dumps()
        print_test_result(expected=expected, actual=out)
        assert out == expected


class Test_JavaScriptTableWriter_write_table:
    @pytest.mark.parametrize(
        ["table", "indent", "header", "value", "is_write_header", "is_dti_fmt", "expected"],
        [
            [
                data.table,
                data.indent,
                data.header,
                data.value,
                data.is_write_header,
                data.is_dti_fmt,
                data.expected,
            ]
            for data in normal_test_data_list
        ],
    )
    def test_normal_single(
        self, capsys, table, indent, header, value, is_write_header, is_dti_fmt, expected
    ):
        writer = table_writer_class()
        writer.table_name = table
        writer.set_indent_level(indent)
        writer.headers = header
        writer.value_matrix = value
        writer.is_write_header = is_write_header
        writer.is_datetime_instance_formatting = is_dti_fmt

        writer.write_table()

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected

    def test_normal_variable_declaration(self, capsys):
        writer = table_writer_class()
        writer.table_name = "$change variable declaration"
        writer.variable_declaration = "var"
        writer.value_matrix = value_matrix
        writer.write_table()

        expected = dedent(
            """\
            var $change_variable_declaration = [
                [1, 123.1, "a", 1, 1],
                [2, 2.2, "bb", 2.2, 2.2],
                [3, 3.3, "ccc", 3, "cccc"]
            ];
            """
        )

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected

    def test_normal_escape_quotes_1(self, capsys):
        writer = table_writer_class()

        expected = r"""const escape_quotes_1 = [
    [8, "data = ["],
    [9, "    [0,   0.1,      \"hoge\", True,   0,      \"2017-01-01 03:04:05+0900\"],"],
    [10, "    [2,   \"-2.23\",  \"foo\",  False,  None,   \"2017-12-23 12:34:51+0900\"],"],
    [11, "    [3,   0,        \"bar\",  \"true\",  \"inf\", \"2017-03-03 22:44:55+0900\"],"],
    [12, "    [-10, -9.9,     \"\",     \"FALSE\", \"nan\", \"2017-01-01 00:00:00+0900\"],"],
    [13, "]"]
];
"""
        writer.table_name = "escape quotes 1"
        writer.value_matrix = [
            [8, "data = ["],
            [9, '    [0,   0.1,      "hoge", True,   0,      "2017-01-01 03:04:05+0900"],'],
            [10, '    [2,   "-2.23",  "foo",  False,  None,   "2017-12-23 12:34:51+0900"],'],
            [11, '    [3,   0,        "bar",  "true",  "inf", "2017-03-03 22:44:55+0900"],'],
            [12, '    [-10, -9.9,     "",     "FALSE", "nan", "2017-01-01 00:00:00+0900"],'],
            [13, "]"],
        ]
        writer.write_table()

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected

    def test_normal_escape_quotes_2(self, capsys):
        writer = table_writer_class()

        expected = r"""const escape_quotes_2 = [
    [2, "writer.from_csv("],
    [3, "    dedent(\"\"\"\\"],
    [4, "        USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND"],
    [5, "        root         1  0.0  0.4  77664  8784 ?        Ss   May11   0:02 /sbin/init"],
    [6, "        root         2  0.0  0.0      0     0 ?        S    May11   0:00 [kthreadd]"],
    [7, "        root         4  0.0  0.0      0     0 ?        I<   May11   0:00 [kworker/0:0H]"],
    [8, "        root         6  0.0  0.0      0     0 ?        I<   May11   0:00 [mm_percpu_wq]"],
    [9, "        root         7  0.0  0.0      0     0 ?        S    May11   0:01 [ksoftirqd/0]"],
    [10, "    \"\"\"),"],
    [11, "    delimiter=\" \")"]
];
"""
        writer.table_name = "escape quotes 2"
        writer.value_matrix = [
            [2, "writer.from_csv("],
            [3, '    dedent("""\\'],
            [4, "        USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND"],
            [
                5,
                "        root         1  0.0  0.4  77664  8784 ?        Ss   May11   0:02 /sbin/init",
            ],
            [
                6,
                "        root         2  0.0  0.0      0     0 ?        S    May11   0:00 [kthreadd]",
            ],
            [
                7,
                "        root         4  0.0  0.0      0     0 ?        I<   May11   0:00 [kworker/0:0H]",
            ],
            [
                8,
                "        root         6  0.0  0.0      0     0 ?        I<   May11   0:00 [mm_percpu_wq]",
            ],
            [
                9,
                "        root         7  0.0  0.0      0     0 ?        S    May11   0:01 [ksoftirqd/0]",
            ],
            [10, '    """),'],
            [11, '    delimiter=" ")'],
        ]
        writer.write_table()

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected

    @pytest.mark.parametrize(
        ["table", "indent", "header", "value", "is_write_header", "expected"],
        [
            [data.table, data.indent, data.header, data.value, data.is_write_header, data.expected]
            for data in exception_test_data_list
        ],
    )
    def test_exception(self, table, indent, header, value, is_write_header, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.set_indent_level(indent)
        writer.headers = header
        writer.value_matrix = value
        writer.is_write_header = is_write_header

        with pytest.raises(expected):
            writer.write_table()


class Test_JavaScriptTableWriter_write_table_iter:
    @pytest.mark.parametrize(
        ["table", "header", "value", "iter_len", "expected"],
        [
            [
                "tablename",
                ["ha", "hb", "hc"],
                value_matrix_iter,
                len(value_matrix_iter),
                dedent(
                    """\
                    const tablename = [
                        ["ha", "hb", "hc"],
                        [1, 2, 3],
                        [11, 12, 13],
                        [1, 2, 3],
                        [11, 12, 13],
                        [101, 102, 103],
                        [1001, 1002, 1003]
                    ];
                    """
                ),
            ],
            [
                "tablename",
                ["ha", "hb", "hc"],
                value_matrix_iter,
                len(value_matrix_iter) - 1,
                dedent(
                    """\
                    const tablename = [
                        ["ha", "hb", "hc"],
                        [1, 2, 3],
                        [11, 12, 13],
                        [1, 2, 3],
                        [11, 12, 13]
                    ];
                    """
                ),
            ],
        ],
    )
    def test_normal(self, capsys, table, header, value, iter_len, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.headers = header
        writer.value_matrix = value
        writer.iteration_length = iter_len
        writer.write_table_iter()

        out, _err = capsys.readouterr()
        assert out == expected

    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [[data.table, data.header, data.value, data.expected] for data in exception_test_data_list],
    )
    def test_exception(self, table, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.headers = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table_iter()
