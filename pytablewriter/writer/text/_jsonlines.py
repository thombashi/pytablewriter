from ._json import JsonTableWriter


try:
    import simplejson as json
except ImportError:
    import json  # type: ignore


class JsonLinesTableWriter(JsonTableWriter):
    """
    A table writer class for JSON lines format.

        :Example:
            :ref:`example-jsonl-writer`
    """

    FORMAT_NAME = "json_lines"

    @property
    def format_name(self) -> str:
        return self.FORMAT_NAME

    @property
    def support_split_write(self) -> bool:
        return True

    def write_table(self, **kwargs) -> None:
        """
        |write_table| with
        `Line-delimited JSON(LDJSON) <https://en.wikipedia.org/wiki/JSON_streaming#Line-delimited_JSON>`__
        /NDJSON/JSON Lines format.

        :raises pytablewriter.EmptyHeaderError: If the |headers| is empty.
        :Example:
            :ref:`example-jsonl-writer`
        """

        with self._logger:
            self._verify_property()
            self._preprocess()

            for values in self._table_value_matrix:
                self._write_line(json.dumps(values, ensure_ascii=False))
