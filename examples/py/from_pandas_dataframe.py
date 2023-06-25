#!/usr/bin/env python3

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import io
from textwrap import dedent

import pandas as pd

import pytablewriter


def main() -> None:
    df = pd.read_csv(
        io.StringIO(
            dedent(
                """\
                "i","f","c","if","ifc","bool","inf","nan","mix_num","time"
                1,1.10,"aa",1.0,"1",True,Infinity,NaN,1,"2017-01-01 00:00:00+09:00"
                22,2.20,"bbb",2.2,"2.2",False,Infinity,NaN,Infinity,"2017-01-02 03:04:05+09:00"
                333,3.33,"cccc",-3.0,"ccc",True,Infinity,NaN,NaN,"2017-01-01 00:00:00+09:00"
                """
            )
        ),
        sep=",",
    )

    writer = pytablewriter.MarkdownTableWriter(dataframe=df)
    writer.write_table()


if __name__ == "__main__":
    main()
