# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import collections
import datetime
import itertools

import pytablewriter
import pytest
import typepy.type

from .data import (
    header_list,
    value_matrix,
    value_matrix_with_none,
    mix_header_list,
    mix_value_matrix,
    value_matrix_iter,
)


Data = collections.namedtuple(
    "Data",
    "table indent header value is_write_header is_dti_fmt expected")

normal_test_data_list = [
    Data(
        table="table-name ho'ge",
        indent=0,
        header=header_list,
        value=value_matrix,
        is_write_header=True,
        is_dti_fmt=True,
        expected="""const table_name_ho_ge = [
    ["a", "b", "c", "dd", "e"],
    [1, 123.1, "a", 1, 1],
    [2, 2.2, "bb", 2.2, 2.2],
    [3, 3.3, "ccc", 3, "cccc"]
];

"""),
    Data(
        table="null value",
        indent=0,
        header=header_list,
        value=None,
        is_write_header=True,
        is_dti_fmt=True,
        expected="""const null_value = [
    ["a", "b", "c", "dd", "e"]
];

"""),
    Data(
        table="null table",
        indent=0,
        header=header_list,
        value=None,
        is_write_header=False,
        is_dti_fmt=True,
        expected="""const null_table = [
];

"""),
    Data(
        table="table name",
        indent=0,
        header=None,
        value=value_matrix,
        is_write_header=True,
        is_dti_fmt=True,
        expected="""const table_name = [
    [1, 123.1, "a", 1, 1],
    [2, 2.2, "bb", 2.2, 2.2],
    [3, 3.3, "ccc", 3, "cccc"]
];

"""),
    Data(
        table="tablename",
        indent=1,
        header=header_list,
        value=value_matrix,
        is_write_header=True,
        is_dti_fmt=True,
        expected="""    const tablename = [
        ["a", "b", "c", "dd", "e"],
        [1, 123.1, "a", 1, 1],
        [2, 2.2, "bb", 2.2, 2.2],
        [3, 3.3, "ccc", 3, "cccc"]
    ];

"""),
    Data(
        table="tablename",
        indent=0,
        header=header_list,
        value=value_matrix_with_none,
        is_write_header=True,
        is_dti_fmt=True,
        expected="""const tablename = [
    ["a", "b", "c", "dd", "e"],
    [1, null, "a", 1, null],
    [null, 2.2, null, 2.2, 2.2],
    [3, 3.3, "ccc", null, "cccc"],
    [null, null, null, null, null]
];

"""),
    Data(
        table="tablename",
        indent=0,
        header=mix_header_list,
        value=mix_value_matrix,
        is_write_header=True,
        is_dti_fmt=True,
        expected="""const tablename = [
    ["i", "f", "c", "if", "ifc", "bool", "inf", "nan", "mix_num", "time"],
    [1, 1.1, "aa", 1, 1, true, Infinity, NaN, 1, new Date("2017-01-01T00:00:00")],
    [2, 2.2, "bbb", 2.2, 2.2, false, Infinity, NaN, Infinity, "2017-01-02 03:04:05+09:00"],
    [3, 3.33, "cccc", -3, "ccc", true, Infinity, NaN, NaN, new Date("2017-01-01T00:00:00")]
];

"""),
    Data(
        table="tablename",
        indent=0,
        header=mix_header_list,
        value=mix_value_matrix,
        is_write_header=True,
        is_dti_fmt=False,
        expected="""const tablename = [
    ["i", "f", "c", "if", "ifc", "bool", "inf", "nan", "mix_num", "time"],
    [1, 1.1, "aa", 1, 1, true, Infinity, NaN, 1, "2017-01-01T00:00:00"],
    [2, 2.2, "bbb", 2.2, 2.2, false, Infinity, NaN, Infinity, "2017-01-02 03:04:05+09:00"],
    [3, 3.33, "cccc", -3, "ccc", true, Infinity, NaN, NaN, "2017-01-01T00:00:00"]
];

"""),
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
        expected="""const float_with_null = [
    ["a", "b"],
    [0.03785679191278808, 826.21158713263],
    [null, 826.21158713263],
    [0.1, 1.0499675627886724]
];

"""),
    Data(
        table="line breaks",
        indent=0,
        header=["a\nb", "\nc\n\nd\n", "e\r\nf"],
        value=[["v1\nv1", "v2\n\nv2", "v3\r\nv3"]],
        is_write_header=True,
        is_dti_fmt=False,
        expected="""const line_breaks = [
    ["a b", " c d ", "e f"],
    ["v1 v1", "v2 v2", "v3 v3"]
];

"""),
]

exception_test_data_list = [
    Data(
        table="",
        indent=normal_test_data_list[0].indent,
        header=normal_test_data_list[0].header,
        value=normal_test_data_list[0].value,
        is_write_header=True,
        is_dti_fmt=True,
        expected=pytablewriter.EmptyTableNameError)
] + [
    Data(
        table="dummy",
        indent=0,
        header=header,
        value=value,
        is_write_header=True,
        is_dti_fmt=True,
        expected=pytablewriter.EmptyTableDataError)
    for header, value in itertools.product([None, [], ""], [None, [], ""])
]

table_writer_class = pytablewriter.JavaScriptTableWriter


class Test_JavaScriptTableWriter_write_new_line(object):

    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()
        assert out == "\n"


class Test_JavaScriptTableWriter_type_hint(object):
    DATATIME_DATA = datetime.datetime(2017, 1, 2, 3, 4, 5)
    STR_DATA = "2017-01-02 03:04:05"
    DATA_MATRIX = [
        [STR_DATA, DATATIME_DATA],
        [STR_DATA, DATATIME_DATA],
    ]

    @pytest.mark.parametrize(
        ["table",  "header", "value", "type_hint", "expected"],
        [
            [
                "th_none_none",
                ["string", "datetime"],
                DATA_MATRIX,
                [None, None],
                """const th_none_none = [
    ["string", "datetime"],
    ["2017-01-02 03:04:05", new Date("2017-01-02T03:04:05")],
    ["2017-01-02 03:04:05", new Date("2017-01-02T03:04:05")]
];

""",
            ],
            [
                "th_none_none",
                ["string", "datetime"],
                DATA_MATRIX,
                [typepy.type.DateTime, typepy.type.String],
                """const th_none_none = [
    ["string", "datetime"],
    [new Date("2017-01-02T03:04:05"), "2017-01-02 03:04:05"],
    [new Date("2017-01-02T03:04:05"), "2017-01-02 03:04:05"]
];

""",
            ],
        ])
    def test_normal(self, capsys, table, header, value, type_hint, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.header_list = header
        writer.value_matrix = value
        writer.type_hint_list = type_hint

        writer.write_table()

        out, _err = capsys.readouterr()

        print("[expected]\n{}".format(expected))
        print("[actual]\n{}".format(out))

        assert out == expected


class Test_JavaScriptTableWriter_write_table(object):

    @pytest.mark.parametrize(
        [
            "table", "indent", "header", "value",
            "is_write_header", "is_dti_fmt", "expected"
        ],
        [
            [
                data.table, data.indent, data.header, data.value,
                data.is_write_header, data.is_dti_fmt, data.expected
            ]
            for data in normal_test_data_list
        ])
    def test_normal_single(
            self, capsys, table, indent, header, value,
            is_write_header, is_dti_fmt, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.set_indent_level(indent)
        writer.header_list = header
        writer.value_matrix = value
        writer.is_write_header = is_write_header
        writer.is_datetime_instance_formatting = is_dti_fmt

        writer.write_table()

        out, _err = capsys.readouterr()

        print("[expected]\n{}".format(expected))
        print("[actual]\n{}".format(out))

        assert out == expected

    def test_normal_variable_declaration(self, capsys):
        writer = table_writer_class()
        writer.table_name = "$change variable declaration"
        writer.variable_declaration = "var"
        writer.value_matrix = value_matrix
        writer.write_table()

        expected = """var $change_variable_declaration = [
    [1, 123.1, "a", 1, 1],
    [2, 2.2, "bb", 2.2, 2.2],
    [3, 3.3, "ccc", 3, "cccc"]
];

"""

        out, _err = capsys.readouterr()

        print("[expected]\n{}".format(expected))
        print("[actual]\n{}".format(out))

        assert out == expected

    @pytest.mark.parametrize(
        ["table", "indent", "header", "value", "is_write_header", "expected"],
        [
            [
                data.table, data.indent, data.header, data.value,
                data.is_write_header, data.expected
            ]
            for data in exception_test_data_list
        ])
    def test_exception(
            self, table, indent, header, value, is_write_header, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.set_indent_level(indent)
        writer.header_list = header
        writer.value_matrix = value
        writer.is_write_header = is_write_header

        with pytest.raises(expected):
            writer.write_table()


class Test_JavaScriptTableWriter_write_table_iter(object):

    @pytest.mark.parametrize(
        ["table", "header", "value", "iter_len", "expected"],
        [
            [
                "tablename",
                ["ha", "hb", "hc"],
                value_matrix_iter,
                len(value_matrix_iter),
                """const tablename = [
    ["ha", "hb", "hc"],
    [1, 2, 3],
    [11, 12, 13],
    [1, 2, 3],
    [11, 12, 13],
    [101, 102, 103],
    [1001, 1002, 1003]
];

""",
            ],
            [
                "tablename",
                ["ha", "hb", "hc"],
                value_matrix_iter,
                len(value_matrix_iter) - 1,
                """const tablename = [
    ["ha", "hb", "hc"],
    [1, 2, 3],
    [11, 12, 13],
    [1, 2, 3],
    [11, 12, 13]
];

""",
            ],
        ])
    def test_normal(self, capsys, table, header, value, iter_len, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.header_list = header
        writer.value_matrix = value
        writer.iteration_length = iter_len
        writer.write_table_iter()

        out, _err = capsys.readouterr()
        assert out == expected

    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [
            [data.table, data.header, data.value, data.expected]
            for data in exception_test_data_list
        ])
    def test_exception(self, table, header, value, expected):
        writer = table_writer_class()
        writer.table_name = table
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table_iter()
