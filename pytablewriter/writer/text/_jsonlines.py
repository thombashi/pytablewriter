# encoding: utf-8

from __future__ import absolute_import, unicode_literals

from ._json import JsonTableWriter


try:
    import simplejson as json
except ImportError:
    import json


class JsonLinesTableWriter(JsonTableWriter):
    """
    A table writer class for JSON lines format.

        :Example:
            :ref:`example-jsonl-writer`
    """

    FORMAT_NAME = "json_lines"

    @property
    def format_name(self):
        return self.FORMAT_NAME

    @property
    def support_split_write(self):
        return True

    def write_table(self):
        """
        |write_table| with
        `Line-delimited JSON(LDJSON) <https://en.wikipedia.org/wiki/JSON_streaming#Line-delimited_JSON>`__
        /NDJSON/JSON Lines format.

        :raises pytablewriter.EmptyHeaderError: If the |header_list| is empty.
        :Example:
            :ref:`example-jsonl-writer`
        """

        with self._logger:
            self._verify_property()
            self._preprocess()

            for value_list in self._table_value_matrix:
                self._write_line(json.dumps(value_list))
