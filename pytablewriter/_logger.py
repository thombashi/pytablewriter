# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import logbook


logger = logbook.Logger("pytablewriter")


class WriterLogger(object):

    def __init__(self, writer):
        self.__writer = writer

    def logging_write(self):
        log_message = "write table: type={:s}, table-name='{}', header={}".format(
            self.__writer.format_name, self.__writer.table_name,
            self.__writer.header_list)

        try:
            log_message += ", type-hint={}".format([
                type_hint(None).typename
                for type_hint in self.__writer.type_hint_list
            ])
        except (TypeError, AttributeError):
            pass

        logger.debug(log_message)
