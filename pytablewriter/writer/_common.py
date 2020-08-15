from textwrap import dedent


import_error_msg_template = dedent(
    """\
    dependency packages for {0} not found.
    you can install the dependencies with 'pip install pytablewriter[{0}]'
    """
)


class Theme:
    class Key:
        STYLE_FILTER = "style_filter"
        COL_SEPARATOR_STYLE_FILTER = "col_separator_style_filter"

    KNOWN_PLUGINS = ("altrow",)
