#!/usr/bin/env python3

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from textwrap import dedent

import pytablewriter


filename = "sample.csv"


def main() -> None:
    with open(filename, "w", encoding="utf8") as f:
        f.write(
            dedent(
                """\
            "i","f","c","if","ifc","bool","inf","nan","mix_num","time"
            1,1.10,"aa",1.0,"1",True,Infinity,NaN,1,"2017-01-01 00:00:00+09:00"
            2,2.20,"bbb",2.2,"2.2",False,Infinity,NaN,Infinity,"2017-01-02 03:04:05+09:00"
            3,3.33,"cccc",-3.0,"ccc",True,Infinity,NaN,NaN,"2017-01-01 00:00:00+09:00"
            """
            )
        )

    writer = pytablewriter.MarkdownTableWriter()
    writer.from_csv(filename)
    writer.write_table()


if __name__ == "__main__":
    main()
