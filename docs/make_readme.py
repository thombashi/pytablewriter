#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

import sys

import readmemaker


PROJECT_NAME = "pytablewriter"
OUTPUT_DIR = ".."


def write_examples(maker):
    maker.set_indent_level(0)
    maker.write_chapter("Examples")

    maker.inc_indent_level()
    maker.write_chapter("Write a Markdown table")
    maker.write_example_file("markdown_example.txt")

    maker.write_chapter("Write a reStructuredText table (grid tables)")
    maker.write_example_file("rst_grid_table_example.txt")

    maker.write_chapter(
        "Write a JavaScript table (variable definition of nested list)")
    maker.write_example_file("javascript_example.txt")

    maker.write_chapter("Write an Excel table")
    maker.write_example_file("exel_single_example.txt")

    maker.write_chapter("For more information")
    maker.write_line_list([
        "More examples are available at ",
        "http://%s.readthedocs.org/en/latest/pages/examples/index.html" % (
            PROJECT_NAME),
    ])


def main():
    maker = readmemaker.ReadmeMaker(PROJECT_NAME, OUTPUT_DIR)

    maker.write_introduction_file("badges.txt")

    maker.inc_indent_level()
    maker.write_chapter("Summary")
    maker.write_introduction_file("summary.txt")
    maker.write_introduction_file("feature.txt")

    write_examples(maker)

    maker.write_file(
        maker.doc_page_root_dir_path.joinpath("installation.rst"))

    maker.set_indent_level(0)
    maker.write_chapter("Documentation")
    maker.write_line_list([
        "http://%s.readthedocs.org/en/latest/" % (PROJECT_NAME),
    ])


if __name__ == '__main__':
    sys.exit(main())
