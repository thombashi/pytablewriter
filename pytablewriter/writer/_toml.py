# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import toml

from ._text_writer import TextTableWriter


class TomlTableWriter(TextTableWriter):
    """
    A table writer class for
    `TOML <https://github.com/toml-lang/toml>`__ data format.
    """

    @property
    def format_name(self):
        return "toml"

    @property
    def support_split_write(self):
        return True

    def __init__(self):
        super(TomlTableWriter, self).__init__()

        self.is_formatting_float = False

        self._is_require_table_name = True
        self._is_require_header = True

    def write_table(self):
        """
        |write_table| with
        `TOML <https://github.com/toml-lang/toml>`__ format.

        :raises pytablewriter.EmptyTableNameError:
            If the |header_list| is empty.
        :raises pytablewriter.EmptyHeaderError:
            If the |header_list| is empty.
        :Example:
            :ref:`example-toml-table-writer`
        """

        self._logger.logging_start_write()
        self._verify_property()
        self.stream.write(toml.dumps(self.tabledata.as_dict()))
        self._logger.logging_complete_write()
