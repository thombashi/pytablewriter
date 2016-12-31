# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import toml

from ._text_writer import TextTableWriter


class TomlTableWriter(TextTableWriter):
    """
    A table writer class for
    `TOML <https://github.com/toml-lang/toml>`__ data format.

    :Examples:

        :ref:`example-toml-table-writer`
    """

    @property
    def support_split_write(self):
        return True

    def __init__(self):
        super(TomlTableWriter, self).__init__()

        self._is_required_table_name = True

    def write_table(self):
        """
        |write_table| with
        `TOML <https://github.com/toml-lang/toml>`__ format.

        :raises pytablewriter.EmptyTableNameError:
            If the |header_list| is empty.
        :raises pytablewriter.EmptyHeaderError:
            If the |header_list| is empty.
        """

        self._verify_property()

        self.stream.write(toml.dumps(self.tabledata.asdict()))

    def _verify_header(self):
        self._validate_empty_header()
