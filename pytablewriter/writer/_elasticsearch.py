# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import copy

import dataproperty
from typepy import Typecode

from .._const import TableFormat
from .._logger import logger
from ._table_writer import AbstractTableWriter


class ElasticsearchWriter(AbstractTableWriter):
    """
    [Experimental] A table writer class for Elasticsearch.
    """

    @property
    def format_name(self):
        return TableFormat.ELASTICSEARCH

    @property
    def support_split_write(self):
        return True

    def __init__(self):
        super(ElasticsearchWriter, self).__init__()

        self.stream = None
        self.is_padding = False
        self.is_float_formatting = False
        self._is_required_table_name = True
        self._quote_flag_mapping = copy.deepcopy(
            dataproperty.NULL_QUOTE_FLAG_MAPPING)

        self.document_type = "table"

    def write_null_line(self):
        pass

    def write_table(self):
        """
        Make a index and put data to a Elastisearch cluster.
        """

        self._logger.logging_start_write()
        self._write_table()

    def __get_es_datatype(self, column_dp):
        if column_dp.typecode in (Typecode.STRING, Typecode.NULL_STRING):
            return {"type": "string"}

        if column_dp.typecode == Typecode.DATETIME:
            return {"type": "date", "format": "date_optional_time"}

        if column_dp.typecode in [Typecode.REAL_NUMBER, Typecode.INFINITY, Typecode.NAN]:
            return {"type": "double"}

        if column_dp.typecode == Typecode.BOOL:
            return {"type": "boolean"}

        if column_dp.typecode == Typecode.IP_ADDRESS:
            return {"type": "ip"}

        if column_dp.typecode == Typecode.INTEGER:
            if column_dp.bit_length <= 8:
                return {"type": "byte"}
            elif column_dp.bit_length <= 16:
                return {"type": "short"}
            elif column_dp.bit_length <= 32:
                return {"type": "integer"}
            elif column_dp.bit_length <= 64:
                return {"type": "long"}

            raise ValueError(
                "too large integer bits: "
                "expected<=64bits, actual={:d}bits".format(
                    column_dp.bit_length))

        raise ValueError("unknown typecode: {}".format(column_dp.typecode))

    def _get_mappings(self):
        properties = {}

        for header, column_dp in zip(self.header_list, self._column_dp_list):
            properties[header] = self.__get_es_datatype(column_dp)

        return {
            "mappings": {
                self.document_type: {
                    "properties": properties
                }
            }
        }

    def _get_body(self):
        for value_dp_list in self._value_dp_matrix:
            value_list = [
                value_dp.data if value_dp.typecode not in (
                    Typecode.DATETIME, Typecode.IP_ADDRESS) else value_dp.to_str()
                for value_dp in value_dp_list
            ]

            yield dict(zip(self.header_list, value_list))

    def _write_table(self):
        import elasticsearch as es

        if not isinstance(self.stream, es.Elasticsearch):
            raise ValueError(
                "stream must be a elasticsearch.Elasticsearch instance")

        self._verify_property()
        self._verify_value_matrix()
        self._preprocess()

        index_name = self.table_name
        mappings = self._get_mappings()

        try:
            result = self.stream.indices.create(
                index=index_name, body=mappings)
            logger.debug(result)
        except es.TransportError as e:
            if e.error == "index_already_exists_exception":
                # ignore already existing index
                logger.debug(e)
            else:
                raise

        for body in self._get_body():
            try:
                self.stream.index(
                    index=index_name, body=body, doc_type=self.document_type)
            except es.exceptions.RequestError as e:
                logger.error("message={}, body={}".format(e, body))

    def _write_value_row_separator(self):
        pass
