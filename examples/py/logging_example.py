#!/usr/bin/env python3

import sys

from loguru import logger
from tblfaker import TableFaker

import pytablewriter as ptw
from pytablewriter import MarkdownTableWriter
from pytablewriter.style import Style


def initialize_logger(name: str, log_level: str) -> None:
    logger.remove()

    if log_level == "quiet":
        logger.disable(name)
        return

    if log_level == "DEBUG":
        log_format = (
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:"
            "<cyan>{function}</cyan>:"
            "<cyan>{line}</cyan> - <level>{message}</level>"
        )
    else:
        log_format = "<level>[{level}]</level> {message}"

    logger.add(sys.stderr, colorize=True, format=log_format, level=log_level)
    logger.enable(name)


def main() -> int:
    initialize_logger("logging", "DEBUG")
    ptw.set_logger(True)

    faker = TableFaker(seed=1)
    data = faker.generate(["name", "email", "address", "random_number"], rows=8)

    writer = MarkdownTableWriter(
        table_name="pytablewriter logging example",
        default_style=Style(thousand_separator=","),
        margin=1,
    )
    writer.from_tabledata(data, is_overwrite_table_name=False)
    writer.write_table()

    return 0


if __name__ == "__main__":
    sys.exit(main())
