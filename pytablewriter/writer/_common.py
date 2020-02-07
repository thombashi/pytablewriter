from textwrap import dedent


import_error_msg_template = dedent(
    """\
    dependency packages for {0} not found.
    you can install the dependencies with 'pip install pytablewriter[{0}]'
    """
)
