# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import collections
import itertools

import pytest

import pytablewriter as ptw

from .data import (
    float_header_list,
    float_value_matrix,
    mix_header_list,
    mix_value_matrix,
    value_matrix,
)


Data = collections.namedtuple("Data", "header value expected")

normal_test_data_list = [
    Data(header=mix_header_list,
         value=mix_value_matrix,
         expected=r"""\begin{array}{r | r | l | r | l | l | l | l | l | l} \hline
    \verb|i| & \verb| f  | & \verb| c  | & \verb| if | & \verb|ifc| & \verb|bool | & \verb| inf  | & \verb|nan| & \verb|mix_num| & \verb|          time           | \\ \hline
    \hline
    1 & 1.10 & aa   &  1.0 &   1 & True  & \infty & NaN &       1 & 2017-01-01 00:00:00       \\ \hline
    2 & 2.20 & bbb  &  2.2 & 2.2 & False & \infty & NaN & \infty  & \verb|2017-01-02 03:04:05+09:00| \\ \hline
    3 & 3.33 & cccc & -3.0 & ccc & True  & \infty & NaN & NaN     & 2017-01-01 00:00:00       \\ \hline
\end{array}

"""),
    Data(header=None,
         value=value_matrix,
         expected=r"""\begin{array}{r | r | l | r | l} \hline
    1 & 123.1 & a   & 1.0 &    1 \\ \hline
    2 &   2.2 & bb  & 2.2 &  2.2 \\ \hline
    3 &   3.3 & ccc & 3.0 & cccc \\ \hline
\end{array}

"""),
    Data(header=float_header_list,
         value=float_value_matrix,
         expected=r"""\begin{array}{r | r | r} \hline
    \verb| a  | & \verb|     b     | & \verb|  c  | \\ \hline
    \hline
    0.01 &      0.0012 & 0.000 \\ \hline
    1.00 &     99.9000 & 0.010 \\ \hline
    1.20 & 999999.1230 & 0.001 \\ \hline
\end{array}

"""),
]

exception_test_data_list = [
    Data(
        header=header,
        value=value,
        expected=ptw.EmptyTableDataError)
    for header, value in itertools.product([None, [], ""], [None, [], ""])
]

table_writer_class = ptw.LatexTableWriter


class Test_LatexTableWriter_write_new_line(object):

    def test_normal(self, capsys):
        writer = table_writer_class()
        writer.write_null_line()

        out, _err = capsys.readouterr()

        assert out == "\n"


class Test_LatexTableWriter_write_table(object):

    @pytest.mark.parametrize(["header", "value", "expected"], [
        [data.header, data.value, data.expected]
        for data in normal_test_data_list
    ])
    def test_normal(self, capsys, header, value, expected):
        writer = table_writer_class()
        writer.header_list = header
        writer.value_matrix = value
        writer.write_table()

        out, _err = capsys.readouterr()

        print("[expected]\n{}".format(expected))
        print("[actual]\n{}".format(out))

        assert out == expected

    @pytest.mark.parametrize(["header", "value", "expected"], [
        [data.header, data.value, data.expected]
        for data in exception_test_data_list
    ])
    def test_exception(self, header, value, expected):
        writer = table_writer_class()
        writer.header_list = header
        writer.value_matrix = value

        with pytest.raises(expected):
            writer.write_table()
