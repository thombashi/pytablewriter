"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import collections

import pytest

import pytablewriter as ptw

from ..._common import print_test_result
from ...data import (
    float_header_list,
    float_value_matrix,
    mix_header_list,
    mix_value_matrix,
    value_matrix,
    vut_style_tabledata,
    vut_styles,
)
from ._common import regexp_ansi_escape


Data = collections.namedtuple("Data", "header value expected")

normal_test_data_list = [
    Data(
        header=mix_header_list,
        value=mix_value_matrix,
        expected=r"""\begin{array}{r | r | l | r | l | l | l | l | l | l} \hline
    \verb|i| & \verb| f  | & \verb| c  | & \verb| if | & \verb|ifc| & \verb|bool | & \verb| inf  | & \verb|nan| & \verb|mix_num| & \verb|          time           | \\ \hline
    \hline
    1 & 1.10 & aa   &  1.0 &   1 & True  & \infty & NaN &       1 & 2017-01-01T00:00:00       \\ \hline
    2 & 2.20 & bbb  &  2.2 & 2.2 & False & \infty & NaN & \infty  & \verb|2017-01-02 03:04:05+09:00| \\ \hline
    3 & 3.33 & cccc & -3.0 & ccc & True  & \infty & NaN & NaN     & 2017-01-01T00:00:00       \\ \hline
\end{array}
""",
    ),
    Data(
        header=None,
        value=value_matrix,
        expected=r"""\begin{array}{r | r | l | r | l} \hline
    1 & 123.1 & a   & 1.0 &    1 \\ \hline
    2 &   2.2 & bb  & 2.2 &  2.2 \\ \hline
    3 &   3.3 & ccc & 3.0 & cccc \\ \hline
\end{array}
""",
    ),
    Data(
        header=float_header_list,
        value=float_value_matrix,
        expected=r"""\begin{array}{r | r | r} \hline
    \verb| a  | & \verb|     b     | & \verb|  c  | \\ \hline
    \hline
    0.01 &      0.0012 & 0.000 \\ \hline
    1.00 &     99.9000 & 0.010 \\ \hline
    1.20 & 999999.1230 & 0.001 \\ \hline
\end{array}
""",
    ),
    Data(
        header=[],
        value=[],
        expected="",
    ),
]


table_writer_class = ptw.LatexTableWriter


class Test_LatexTableWriter_write_new_line:
    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()

        assert out == "\n"


class Test_LatexTableWriter_write_table:
    @pytest.mark.parametrize(
        ["header", "value", "expected"],
        [[data.header, data.value, data.expected] for data in normal_test_data_list],
    )
    def test_normal(self, capsys, header, value, expected):
        writer = table_writer_class()
        writer.headers = header
        writer.value_matrix = value
        writer.write_table()

        out, err = capsys.readouterr()
        print_test_result(expected=expected, actual=out, error=err)

        assert out == expected
        assert writer.dumps() == expected
        assert str(writer) == expected

    def test_normal_styles(self):
        writer = table_writer_class()
        writer.from_tabledata(vut_style_tabledata)
        writer.column_styles = vut_styles

        expected = r"""\begin{array}{r | r | r | r | r | r | l | r | r | r} \hline
    \verb|none| & \verb|empty| & \verb|  tiny   | & \verb|  small   | & \verb|     medium     | & \verb|   large   | & \verb|null w/ bold| & \verb|   L bold    | & \verb|  S italic   | & \verb| L bold italic  | \\ \hline
    \hline
     111 &   111 & \tiny 111 & \small 111 &  \normalsize 111 &  \large 111 &              & \large \bf 111 & \small \it 111 & \large \bf \it 111 \\ \hline
    1234 &  1234 & \tiny 1234 & \small 1234 & \normalsize 1,234 & \large 1 234 &              & \large \bf 1234 & \small \it 1234 & \large \bf \it 1234 \\ \hline
\end{array}
"""

        out = writer.dumps()
        print_test_result(expected=expected, actual=out)

        assert regexp_ansi_escape.search(out)
        assert regexp_ansi_escape.sub("", out) == expected
