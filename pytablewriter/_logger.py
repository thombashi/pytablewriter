# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import logbook


logger = logbook.Logger("pytablewriter")
logger.disable()


def set_logger(log_level):
    """
    Set logging level of this module. The module using
    `logbook <http://logbook.readthedocs.io/en/stable/>`__ module for logging.

    :param int log_level:
        One of the log level of the
        `logbook <http://logbook.readthedocs.io/en/stable/api/base.html>`__.
        Disabled logging if the ``log_level`` is ``logbook.NOTSET``.
    """

    if log_level == logbook.NOTSET:
        logger.disable()
    else:
        logger.enable()
        logger.level = log_level


class WriterLogger(object):

    def __init__(self, writer):
        self.__writer = writer
        logger.debug(
            "created WriterLogger: format={}".format(writer.format_name))

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
