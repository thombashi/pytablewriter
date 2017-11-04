# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import copy

import dataproperty
from typepy import Typecode

from six.moves import zip

from ._table_writer import AbstractTableWriter


class ElasticsearchWriter(AbstractTableWriter):
    """
    A table writer class for Elasticsearch.

    .. py:attribute:: index_name

        Alias attribute for |table_name|.

    .. py:attribute:: document_type

        Specify document type for indices. Defaults to ``"table"``.

    .. py:method:: write_table()

        Create an index and put documents for each row to Elasticsearch.

        You need to pass an
        `elasticsearch.Elasticsearch <http://elasticsearch-py.readthedocs.io/en/master/api.html#elasticsearch>`__
        instance to |stream| before calling this method.
        |table_name|/:py:attr:`~pytablewriter.ElasticsearchWriter.index_name`
        used as the creating index name,
        invalid characters in the name are replaced with underscore (``'_'``).
        Document data types for documents are automatically detected
        from the data.

        :raises ValueError:
            If the |stream| has not elasticsearch.Elasticsearch instance.
        :Example:
            :ref:`example-elasticsearch-table-writer`
    """

    @property
    def format_name(self):
        return "elasticsearch"

    @property
    def support_split_write(self):
        return True

    @property
    def table_name(self):
        return super(ElasticsearchWriter, self).table_name

    @table_name.setter
    def table_name(self, value):
        from pathvalidate import (
            ElasticsearchIndexNameSanitizer,
            NullNameError,
        )

        try:
            self._table_name = ElasticsearchIndexNameSanitizer(
                value).sanitize(replacement_text="_")
        except NullNameError:
            self._table_name = None

    @property
    def index_name(self):
        return self.table_name

    @index_name.setter
    def index_name(self, value):
        self.table_name = value

    def __init__(self):
        super(ElasticsearchWriter, self).__init__()

        self.stream = None
        self.is_padding = False
        self.is_formatting_float = False
        self._is_require_table_name = True
        self._quoting_flags = copy.deepcopy(dataproperty.NOT_QUOTING_FLAGS)
        self._dp_extractor.type_value_mapping = copy.deepcopy(
            dataproperty.DefaultValue.TYPE_VALUE_MAPPING)

        self.document_type = "table"

    def write_null_line(self):
        pass

    @staticmethod
    def __get_es_datatype(column_dp):
        if column_dp.typecode in (Typecode.STRING, Typecode.NULL_STRING):
            return {"type": "string"}

        if column_dp.typecode == Typecode.DATETIME:
            return {"type": "date", "format": "date_optional_time"}

        if column_dp.typecode == Typecode.REAL_NUMBER:
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

        if column_dp.typecode == Typecode.NONE:
            return {"type": "string"}

        if column_dp.typecode in (Typecode.INFINITY, Typecode.NAN):
            return {"type": "keyword"}

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
        str_datatype = (
            Typecode.DATETIME, Typecode.IP_ADDRESS,
            Typecode.INFINITY, Typecode.NAN,
        )

        for value_dp_list in self._value_dp_matrix:
            value_list = [
                value_dp.data if value_dp.typecode not in str_datatype else value_dp.to_str()
                for value_dp in value_dp_list
            ]

            yield dict(zip(self.header_list, value_list))

    def _write_table(self):
        import elasticsearch as es

        if not isinstance(self.stream, es.Elasticsearch):
            raise ValueError(
                "stream must be an elasticsearch.Elasticsearch instance")

        self._verify_value_matrix()
        self._preprocess()

        mappings = self._get_mappings()

        try:
            result = self.stream.indices.create(
                index=self.index_name, body=mappings)
            self._logger.logger.debug(result)
        except es.TransportError as e:
            if e.error == "index_already_exists_exception":
                # ignore already existing index
                self._logger.logger.debug(
                    "{:s}: {}".format(e.__class__.__name__, e))
            else:
                raise

        for body in self._get_body():
            try:
                self.stream.index(
                    index=self.index_name, body=body,
                    doc_type=self.document_type)
            except es.exceptions.RequestError as e:
                self._logger.logger.error(
                    "message={}, body={}".format(e, body))

    def _write_value_row_separator(self):
        pass
