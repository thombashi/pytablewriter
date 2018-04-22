#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import argparse
import datetime
import json
import sys

import pytablewriter as ptw
from elasticsearch import Elasticsearch


def parse_option():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--host", default="localhost",
        help="default=%(default)s")
    parser.add_argument(
        "--port", type=int, default=9200,
        help="default=%(default)s")

    return parser.parse_args()


def main():
    options = parse_option()

    es = Elasticsearch(hosts="{:s}:{:d}".format(options.host, options.port))

    writer = ptw.ElasticsearchWriter()
    writer.stream = es
    writer.index_name = "es writer example"
    writer.header_list = [
        "str", "byte", "short", "int", "long", "float", "date", "bool", "ip",
    ]
    writer.value_matrix = [
        [
            "abc", 100, 10000, 2000000000, 200000000000, 0.1,
            datetime.datetime(2017, 1, 2, 3, 4, 5), True, "127.0.0.1",
        ],
        [
            "def", -10, -1000, -200000000, -20000000000, 100.1,
            datetime.datetime(2017, 6, 5, 4, 5, 2), False, "::1",
        ],
    ]

    # delete existing index ---
    es.indices.delete(index=writer.index_name, ignore=404)

    # create an index and put data ---
    writer.write_table()

    # display the result ---
    es.indices.refresh(index=writer.index_name)

    print("----- mappings -----")
    response = es.indices.get_mapping(
        index=writer.index_name, doc_type="table")
    print("{}\n".format(json.dumps(response, indent=4)))

    print("----- documents -----")
    response = es.search(
        index=writer.index_name,
        doc_type="table",
        body={
            "query": {"match_all": {}}
        }
    )
    for hit in response["hits"]["hits"]:
        print(json.dumps(hit["_source"], indent=4))

    return 0


if __name__ == "__main__":
    sys.exit(main())
