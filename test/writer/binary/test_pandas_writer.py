"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import collections
import os
import sys
from decimal import Decimal

import pytest
from tabledata import TableData

import pytablewriter as ptw

from ..._common import print_test_result
from ...data import headers, value_matrix


try:
    import pandas as pd

    SKIP_DATAFRAME_TEST = False
except ImportError:
    SKIP_DATAFRAME_TEST = True


inf = Decimal("Infinity")
nan = None

Data = collections.namedtuple("Data", "table header value expected")

normal_test_data_list = [
    Data(
        table="tablename",
        header=headers,
        value=value_matrix,
        expected=TableData(
            "tablename",
            ["a", "b", "c", "dd", "e"],
            [[1, 123.1, "a", 1, 1], [2, 2.2, "bb", 2.2, 2.2], [3, 3.3, "ccc", 3, "cccc"]],
        ),
    ),
    Data(
        table="empty header",
        header=[],
        value=value_matrix,
        expected=TableData(
            "empty_header",
            ["A", "B", "C", "D", "E"],
            [[1, 123.1, "a", 1, 1], [2, 2.2, "bb", 2.2, 2.2], [3, 3.3, "ccc", 3, "cccc"]],
        ),
    ),
]

empty_test_data_list = [
    Data(table="dummy", header=[], value=[], expected=None),
    Data(table="dummy", header=headers, value=[], expected=None),
]


@pytest.mark.skipif(SKIP_DATAFRAME_TEST, reason="required package not found")
class Test_PandasDataFramePickleWriter_write_table:
    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [[data.table, data.header, data.value, data.expected] for data in normal_test_data_list],
    )
    def test_normal(self, tmpdir, table, header, value, expected):
        test_filepath = tmpdir.join("test1.pkl")

        writer = ptw.PandasDataFramePickleWriter(
            table_name=table,
            headers=header,
            value_matrix=value,
        )
        writer.open(str(test_filepath))
        writer.write_table()

        print(expected, file=sys.stderr)

        actual = ptw.PandasDataFramePickleWriter()
        actual.from_dataframe(pd.read_pickle(test_filepath))
        actual.table_name = expected.table_name

        print_test_result(
            expected=ptw.dumps_tabledata(expected), actual=ptw.dumps_tabledata(actual.tabledata)
        )

        assert ptw.dumps_tabledata(actual.tabledata) == ptw.dumps_tabledata(expected)

    @pytest.mark.parametrize(
        ["table", "header", "value", "expected"],
        [[data.table, data.header, data.value, data.expected] for data in empty_test_data_list],
    )
    def test_smoke_empty(self, tmpdir, table, header, value, expected):
        test_filepath = str(tmpdir.join("empty.pkl"))
        writer = ptw.PandasDataFramePickleWriter(
            table_name=table, headers=header, value_matrix=value
        )
        writer.open(test_filepath)
        writer.write_table()
        assert not os.path.isfile(test_filepath)

    def test_exception(self):
        writer = ptw.PandasDataFramePickleWriter(
            table_name="tablename",
            headers=["ha", "hb", "hc"],
            value_matrix=[[1.0, 2.0, 3.0], [11.0, 12.0, 13.0], [1.0, 2.0, 3.0]],
        )

        writer.write_table()


@pytest.mark.skipif(SKIP_DATAFRAME_TEST, reason="required package not found")
class Test_PandasDataFramePickleWriter_dump:
    def test_normal_single_table(self, tmpdir):
        test_filepath = str(tmpdir.join("test.pkl"))
        data = TableData(
            "tablename", ["ha", "hb", "hc"], [[1.0, 2.0, 3.0], [11.0, 12.0, 13.0], [1.0, 2.0, 3.0]]
        )

        writer = ptw.PandasDataFramePickleWriter()
        writer.from_tabledata(data)
        writer.dump(test_filepath)

        actual = ptw.PandasDataFramePickleWriter()
        actual.from_dataframe(pd.read_pickle(test_filepath))
        actual.table_name = data.table_name

        assert actual.tabledata == data

    def test_normal_multi_table(self, tmpdir):
        test_filepath = str(tmpdir.join("test.pkl"))
        data = TableData("first", ["ha1", "hb1", "hc1"], [[1.0, 2.0, 3.0], [11.0, 12.0, 13.0]])
        writer = ptw.PandasDataFramePickleWriter()

        writer.from_tabledata(data)
        writer.dump(test_filepath, close_after_write=False)

        actual = ptw.PandasDataFramePickleWriter()
        actual.from_dataframe(pd.read_pickle(test_filepath))
        actual.table_name = data.table_name

        assert actual.tabledata == data


class Test_PandasDataFramePickleWriter_dumps:
    def test_exception(self, tmpdir):
        writer = ptw.PandasDataFramePickleWriter()

        with pytest.raises(NotImplementedError):
            writer.dumps()
