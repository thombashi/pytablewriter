#!/usr/bin/env python3

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import sys
from typing import Final

from path import Path
from readmemaker import ReadmeMaker


PROJECT_NAME: Final = "pytablewriter"
OUTPUT_DIR: Final = ".."


class Chapter:
    STYLE_FILTER: Final = "Style filter"


def make_internal_link(title: str, chapter: str) -> str:
    link = chapter.replace(" ", "-").lower()
    return f"`{title:s} <#{link:s}>`_"


def write_examples(maker: ReadmeMaker) -> None:
    maker.set_indent_level(0)
    maker.write_chapter("Examples")

    examples_root = Path("pages").joinpath("examples")

    maker.set_indent_level(1)
    maker.write_chapter("Write tables")
    maker.inc_indent_level()

    maker.write_chapter("Write a Markdown table")
    maker.write_file(examples_root.joinpath("table_format", "text", "markdown", "md_example.txt"))

    with maker.indent():
        maker.write_chapter("Write a Markdown table with margins")
        maker.write_file(
            examples_root.joinpath("table_format", "text", "markdown", "md_example_with_margin.txt")
        )

        maker.write_chapter("Write a GitHub Flavored Markdown (GFM) table")
        maker.write_file(
            examples_root.joinpath("table_format", "text", "markdown", "md_example_with_flavor.txt")
        )

        maker.write_chapter("Apply styles to GFM table with programmatically")
        maker.write_lines(
            [
                "Applying style filters to GFM allows for more flexible style settings for cells.",
                "See also the {}".format(make_internal_link("example", Chapter.STYLE_FILTER)),
            ]
        )

    with maker.indent():
        maker.write_chapter("Write a Markdown table to a stream or a file")
        maker.write_lines(
            [
                "`Refer an example <https://github.com/thombashi/pytablewriter/blob/master/examples/py/stream/configure_stream.py>`__"
            ]
        )

    maker.write_chapter("Write a table to an Excel sheet")
    maker.write_file(
        examples_root.joinpath("table_format", "binary", "spreadsheet", "excel_single_example.txt")
    )

    maker.write_chapter("Write a Unicode table")
    maker.write_file(examples_root.joinpath("table_format", "text", "unicode_example.txt"))

    maker.write_chapter(
        "Write a table with JavaScript format (as a nested list variable definition)"
    )
    maker.write_file(
        examples_root.joinpath("table_format", "text", "sourcecode", "javascript_example.txt")
    )

    maker.write_chapter("Write a Markdown table from ``pandas.DataFrame`` instance")
    maker.write_file(examples_root.joinpath("datasource", "from_pandas_dataframe_example.txt"))

    maker.write_chapter("Write a Markdown table from space-separated values")
    maker.write_file(examples_root.joinpath("datasource", "from_ssv_example.txt"))

    maker.set_indent_level(1)
    maker.write_chapter("Get rendered tabular text as str")
    maker.write_file(examples_root.joinpath("output", "dump", "dumps.txt"))

    maker.set_indent_level(1)
    maker.write_chapter("Configure table styles")
    maker.inc_indent_level()
    maker.write_chapter("Column styles")
    maker.write_file(examples_root.joinpath("style", "column_style_example.txt"))

    maker.write_chapter(Chapter.STYLE_FILTER)
    maker.write_file(
        examples_root.joinpath(
            "table_format", "text", "markdown", "md_example_with_style_filter.txt"
        )
    )

    maker.write_chapter("Theme")
    maker.write_file(examples_root.joinpath("style", "theme.txt"))

    maker.set_indent_level(1)
    maker.write_chapter("Make tables for specific applications")
    maker.inc_indent_level()

    maker.write_chapter("Render a table on Jupyter Notebook")
    maker.write_file(examples_root.joinpath("jupyter_notebook", "jupyter_notebook_example.txt"))

    maker.set_indent_level(1)
    maker.write_chapter("Multibyte character support")
    maker.inc_indent_level()

    maker.write_chapter("Write a table using multibyte character")
    maker.write_file(examples_root.joinpath("multibyte", "multibyte_table_example.txt"))

    maker.set_indent_level(1)
    maker.write_chapter("Multiprocessing")
    maker.write_file(examples_root.joinpath("customize", "multi_process.txt"))

    # maker.write_chapter("Create Elasticsearch index and put data")
    # maker.write_file(examples_root.joinpath("table_format", "elasticsearch_example.txt"))

    maker.set_indent_level(1)
    maker.write_chapter("For more information")
    maker.write_lines(
        [
            "More examples are available at ",
            f"https://{PROJECT_NAME:s}.rtfd.io/en/latest/pages/examples/index.html",
        ]
    )


def main():
    maker = ReadmeMaker(
        PROJECT_NAME,
        OUTPUT_DIR,
        is_make_toc=True,
        project_url=f"https://github.com/thombashi/{PROJECT_NAME}",
    )

    maker.write_chapter("Summary")
    maker.write_introduction_file("summary.txt")
    maker.write_introduction_file("badges.txt")
    maker.write_introduction_file("feature.txt")
    maker.write_introduction_file("installation.rst")

    write_examples(maker)

    maker.write_introduction_file("dependencies.rst")

    maker.set_indent_level(0)
    maker.write_chapter("Documentation")
    maker.write_lines([f"https://{PROJECT_NAME:s}.rtfd.io/"])

    maker.write_file(maker.doc_page_root_dir_path.joinpath("related.rst"))
    maker.write_file(maker.doc_page_root_dir_path.joinpath("sponsors.rst"))

    return 0


if __name__ == "__main__":
    sys.exit(main())
