# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import logbook
import pytablereader
import simplesqlite


logger = logbook.Logger("pytablewriter")
logger.disable()


def set_logger(is_enable):
    pytablereader.set_logger(is_enable)
    simplesqlite.set_logger(is_enable)

    if is_enable:
        logger.enable()
    else:
        logger.disable()


def set_log_level(log_level):
    """
    Set logging level of this module. Using
    `logbook <http://logbook.readthedocs.io/en/stable/>`__ module for logging.

    :param int log_level:
        One of the log level of
        `logbook <http://logbook.readthedocs.io/en/stable/api/base.html>`__.
        Disabled logging if ``log_level`` is ``logbook.NOTSET``.
    """

    pytablereader.set_log_level(log_level)
    simplesqlite.set_log_level(log_level)

    if log_level == logbook.NOTSET:
        set_logger(is_enable=False)
    else:
        set_logger(is_enable=True)
        logger.level = log_level


class WriterLogger(object):

    def __init__(self, writer):
        self.__writer = writer
        logger.debug(
            "created WriterLogger: format={}".format(writer.format_name))

    def logging_write(self):
        log_entry_list = [
            "type={:s}".format(self.__writer.format_name),
            "table-name='{}'".format(self.__writer.table_name),
            "header={}".format(self.__writer.header_list),
        ]

        try:
            log_entry_list.append(
                "rows={}".format(len(self.__writer.value_matrix)))
        except (TypeError, AttributeError):
            pass

        try:
            log_entry_list.append("type-hint={}".format([
                type_hint(None).typename
                for type_hint in self.__writer.type_hint_list
            ]))
        except (TypeError, AttributeError):
            pass

        logger.debug("write table: " + ", ".join(log_entry_list))
