import collections
import itertools
from io import StringIO
from textwrap import dedent

import pytest
import yaml
from tabledata import TableData

import pytablewriter as ptw

from ..._common import print_test_result
from ...data import float_tabledata, mix_tabledata, value_matrix


Data = collections.namedtuple("Data", "tabledata expected")

normal_test_data_list = [
    Data(
        tabledata=mix_tabledata,
        expected=dedent(
            """\
            mix data:
            - bool: true
              c: aa
              f: 1.1
              i: 1
              if: 1
              ifc: 1
              inf: .inf
              mix_num: 1
              nan: .nan
              time: '2017-01-01T00:00:00'
            - bool: false
              c: bbb
              f: 2.2
              i: 2
              if: 2.2
              ifc: 2.2
              inf: .inf
              mix_num: .inf
              nan: .nan
              time: '2017-01-02 03:04:05+09:00'
            - bool: true
              c: cccc
              f: 3.33
              i: 3
              if: -3
              ifc: ccc
              inf: .inf
              mix_num: .nan
              nan: .nan
              time: '2017-01-01T00:00:00'
            """
        ),
    ),
    Data(
        tabledata=TableData(
            table_name=None,
            headers=[],
            rows=value_matrix,
        ),
        expected=dedent(
            """\
            - - 1
              - 123.1
              - a
              - 1
              - 1
            - - 2
              - 2.2
              - bb
              - 2.2
              - 2.2
            - - 3
              - 3.3
              - ccc
              - 3
              - cccc
            """
        ),
    ),
    Data(
        tabledata=float_tabledata,
        expected=dedent(
            """\
            float data:
            - a: 0.01
              b: 0.00125
              c: 0
            - a: 1
              b: 99.9
              c: 0.01
            - a: 1.2
              b: 999999.123
              c: 0.001
            """
        ),
    ),
]

exception_test_data_list = [
    Data(
        tabledata=TableData(table_name=None, headers=headers, rows=rows),
        expected=ptw.EmptyTableDataError,
    )
    for headers, rows in itertools.product([None, [], ""], [None, [], ""])
]

table_writer_class = ptw.YamlTableWriter


class Test_YamlTableWriter_write_new_line:
    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()

        assert out == "\n"


class Test_YamlTableWriter_write_table:
    @pytest.mark.parametrize(
        ["value", "expected"],
        [[data.tabledata, data.expected] for data in normal_test_data_list],
    )
    def test_normal(self, capsys, value, expected):
        writer = table_writer_class()
        writer.from_tabledata(value)
        writer.write_table()

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)
        assert out == expected
        assert yaml.safe_load(StringIO(out))

        # margin setting must be ignored
        writer.margin = 1
        dumps_out = writer.dumps()
        print_test_result(expected=out, actual=dumps_out)
        assert dumps_out == out

    @pytest.mark.parametrize(
        ["value", "expected"],
        [[data.tabledata, data.expected] for data in exception_test_data_list],
    )
    def test_exception(self, value, expected):
        writer = table_writer_class()
        writer.from_tabledata(value)

        with pytest.raises(expected):
            writer.write_table()
