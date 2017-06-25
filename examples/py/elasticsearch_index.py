# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import datetime

import logbook

from elasticsearch import Elasticsearch
import pytablewriter as ptw


logbook.StderrHandler(
    level=logbook.DEBUG,
    format_string="[{record.level_name}] {record.channel}: {record.message}"
).push_application()


writer = ptw.ElasticsearchWriter()

writer.stream = Elasticsearch(hosts="localhost:9200")
writer.table_name = "es_mappings"
writer.header_list = [
    "str", "byte", "short", "int", "long", "float", "date", "bool", "ip",
]
writer.value_matrix = [
    [
        "abc", 100, 10000, 2000000000, 200000000000, 0.1,
        datetime.datetime(2017, 1, 3, 4, 5, 6), True, "127.0.0.1",
    ],
    [
        "def", -10, -1000, -200000000, -20000000000, 100.1,
        datetime.datetime(2017, 1, 3, 4, 5, 6), False, "::1",
    ],
]

writer.write_table()
