# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import dataproperty
import logbook
from mbstrdecoder import MultiByteStrDecoder
import pytablereader
import simplesqlite


logger = logbook.Logger("pytablewriter")
logger.disable()


def set_logger(is_enable):
    if is_enable != logger.disabled:
        return

    if is_enable:
        logger.enable()
    else:
        logger.disable()

    dataproperty.set_logger(is_enable)
    pytablereader.set_logger(is_enable)
    simplesqlite.set_logger(is_enable)


def set_log_level(log_level):
    """
    Set logging level of this module. Using
    `logbook <http://logbook.readthedocs.io/en/stable/>`__ module for logging.

    :param int log_level:
        One of the log level of
        `logbook <http://logbook.readthedocs.io/en/stable/api/base.html>`__.
        Disabled logging if ``log_level`` is ``logbook.NOTSET``.
    :raises LookupError: If ``log_level`` is an invalid value.
    """

    # validate log level
    logbook.get_level_name(log_level)

    if log_level == logger.level:
        return

    if log_level == logbook.NOTSET:
        set_logger(is_enable=False)
    else:
        set_logger(is_enable=True)

    logger.level = log_level
    dataproperty.set_log_level(log_level)
    pytablereader.set_log_level(log_level)
    simplesqlite.set_log_level(log_level)


class WriterLogger(object):

    @property
    def logger(self):
        return self.__logger

    def __init__(self, writer):
        self.__writer = writer
        self.__logger = logger

        self.logger.debug(
            "created WriterLogger: format={}".format(writer.format_name))

    def logging_start_write(self, extra_message_list=None):
        log_entry_list = [
            self.__get_format_name_message(),
            self.__get_table_name_message(),
            "header={}".format(self.__writer.header_list),
        ]

        try:
            log_entry_list.append(
                "rows={}".format(len(self.__writer.value_matrix)))
        except (TypeError, AttributeError):
            pass

        log_entry_list.append(self.__get_typehint_message())

        if extra_message_list:
            log_entry_list.extend(extra_message_list)

        logger.debug("write table: {}".format(", ".join(log_entry_list)))

    def logging_complete_write(self, extra_message_list=None):
        log_entry_list = [
            self.__get_format_name_message(),
            self.__get_table_name_message(),
        ]

        logger.debug(
            "complete write table: {}".format(", ".join(log_entry_list)))

    def __get_format_name_message(self):
        return "format={:s}".format(self.__writer.format_name)

    def __get_table_name_message(self):
        if self.__writer.table_name:
            table_name = MultiByteStrDecoder(
                self.__writer.table_name).unicode_str
        else:
            table_name = None

        return "table-name='{}'".format(table_name)

    def __get_typehint_message(self):
        try:
            return "type-hint={}".format([
                type_hint(None).typename
                for type_hint in self.__writer.type_hint_list
            ])
        except (TypeError, AttributeError):
            return "type-hint=[]"
