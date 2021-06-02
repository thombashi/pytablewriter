"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import random
import string


alphanum_chars = [x for x in string.digits + string.ascii_letters]


INVALID_PATH_CHARS = ["\0"]
INVALID_FILENAME_CHARS = ["/"]
INVALID_WIN_PATH_CHARS = [":", "*", "?", '"', "<", ">", "|"] + INVALID_PATH_CHARS
INVALID_WIN_FILENAME_CHARS = INVALID_WIN_PATH_CHARS + INVALID_FILENAME_CHARS + ["\\"]

VALID_FILENAME_CHARS = [
    "!",
    "#",
    "$",
    "&",
    "'",
    "_",
    "=",
    "~",
    "^",
    "@",
    "`",
    "[",
    "]",
    "+",
    "-",
    ";",
    "{",
    "}",
    ",",
    ".",
    "(",
    ")",
    "%",
]
VALID_PATH_CHARS = VALID_FILENAME_CHARS + ["/"]

INVALID_JS_VAR_CHARS = INVALID_WIN_FILENAME_CHARS + [
    "!",
    "#",
    "&",
    "'",
    "=",
    "~",
    "^",
    "@",
    "`",
    "[",
    "]",
    "+",
    "-",
    ";",
    "{",
    "}",
    ",",
    ".",
    "(",
    ")",
    "%",
    " ",
    "\t",
    "\n",
    "\r",
    "\f",
    "\v",
]
INVALID_PYTHON_VAR_CHARS = INVALID_JS_VAR_CHARS + ["$"]


def make_random_str(length, chars=alphanum_chars):
    return "".join(random.choice(chars) for _i in range(length))
