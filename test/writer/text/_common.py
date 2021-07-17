import re


regexp_ansi_escape = re.compile(
    r"(?:\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])"
)


def strip_ansi_escape(value):
    return regexp_ansi_escape.sub("", value)
