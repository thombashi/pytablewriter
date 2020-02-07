from ._csv import CsvTableWriter


class TsvTableWriter(CsvTableWriter):
    """
    A table writer class for tab separated values (TSV) format.

        :Example:
            :ref:`example-tsv-table-writer`
    """

    FORMAT_NAME = "tsv"

    @property
    def format_name(self):
        return self.FORMAT_NAME

    def __init__(self):
        super().__init__()

        self.column_delimiter = "\t"
