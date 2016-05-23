#!/usr/bin/env python
# encoding: utf-8

import os
import re
import sys


PROJECT_NAME = "pytablewriter"
VERSION = "0.5.0"
OUTPUT_DIR = ".."
README_WORK_DIR = "."
DOC_PAGE_DIR = os.path.join(README_WORK_DIR, "pages")


def get_usage_file_path(filename):
    return os.path.join(DOC_PAGE_DIR, "examples", filename)


def replace_for_pypi(line):
    line = line.replace(".. code-block::", ".. code::")
    line = line.replace(".. code:: none", ".. code::")

    return line


def write_line_list(f, line_list):
    f.write("\n".join([
        replace_for_pypi(line)
        for line in line_list
        if re.search(":caption:", line) is None
    ]))
    f.write("\n" * 2)


def write_usage_file(f, filename):
    with open(get_usage_file_path(filename)) as f_usage_file:
        write_line_list(
            f, [line.rstrip()for line in f_usage_file.readlines()])


def write_examples(f):
    write_line_list(f, [
        "Examples",
        "========",
    ])

    write_line_list(f, [
        "Write a Markdown table",
        "----------------------------",
    ])
    write_usage_file(f, "markdown_example.txt")

    write_line_list(f, [
        "Write a JavaScript table (variable definition of nested list )",
        "----------------------------------------------------------------",
    ])
    write_usage_file(f, "javascript_example.txt")

    write_line_list(f, [
        "Write an Excel table",
        "----------------------------",
    ])
    write_usage_file(f, "exel_single_example.txt")

    write_line_list(f, [
        "For more information",
        "--------------------",
        "More examples are available at ",
        "http://%s.readthedocs.org/en/latest/pages/examples/index.html" % (
            PROJECT_NAME),
        "",
    ])


def main():
    with open(os.path.join(OUTPUT_DIR, "README.rst"), "w") as f:
        write_line_list(f, [
            PROJECT_NAME,
            "=" * len(PROJECT_NAME),
            "",
        ] + [
            line.rstrip() for line in
            open(os.path.join(
                DOC_PAGE_DIR, "introduction", "badges.txt")).readlines()
        ])

        write_line_list(f, [
            "Summary",
            "-------",
            "",
        ] + [
            line.rstrip() for line in
            open(os.path.join(
                DOC_PAGE_DIR, "introduction", "summary.txt")).readlines()
        ])

        write_examples(f)

        write_line_list(f, [
            line.rstrip() for line in
            open(os.path.join(DOC_PAGE_DIR, "installation.rst")).readlines()
        ])

        write_line_list(f, [
            "Documentation",
            "=============",
            "",
            "http://%s.readthedocs.org/en/latest/" % (PROJECT_NAME)
        ])


if __name__ == '__main__':
    sys.exit(main())
