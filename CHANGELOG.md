<a id="v1.2.0"></a>
# [v1.2.0](https://github.com/thombashi/pytablewriter/releases/tag/v1.2.0) - 2023-10-08

- Add `enable_style_filter` method and `disable_style_filter` method to writer classes
- Add `check_style_filter_kwargs` method to the `Theme` class
- Add `pytablewriter-altcol-theme` to theme extras
- Add `margin` support to the `CssTableWriter` class
- Add support for Python 3.12
- Modify the style filter to be applicable to table headers: [#37](https://github.com/thombashi/pytablewriter/issues/37) (Thanks to [@shawalli](https://github.com/shawalli))
- Change the `add_col_separator_style_filter` method that raises `NotImplementedError` to debug-log output
- Improve discovery of pytablewriter plugins
- Bump minimum required version of `typepy` to 1.3.2
- Fix `margin`, `stream`, and `style_filter_kwargs` to be propagated correctly in `from_writer` method
    - Fix the output of `HtmlTableWriter.write_table` method when the method called with `write_css=True`
- Fix an issue where the CSS output would be incorrect if the `HtmlTableWriter.write_table` method was called with `write_css=True` when `table_name` was not specified
- Fix style applying for headers of `CssTableWriter` writer class
- Fix type annotations


**Full Changelog**: https://github.com/thombashi/pytablewriter/compare/v1.1.0...v1.2.0

[Changes][v1.2.0]


<a id="v1.1.0"></a>
# [v1.1.0](https://github.com/thombashi/pytablewriter/releases/tag/v1.1.0) - 2023-09-24

- Add color support for GFM to `MarkdownTableWriter` class
- Add `FontStyle.TYPEWRITER`
- Add styles supported by Latex writers
  - `Style.fg_color`
  - `Style.decoration_line`: `DecorationLine.STRIKE`, `DecorationLine.LINE_THROUGH`
  - `Style.decoration_line`: `DecorationLine.UNDERLINE`
- Add warnings for when invalid style attributes are passed to the Style class
- Modify the output format of Latex table writers
- Improve type annotations
- Fix Excel worksheet name generation
- Bump minimum required version of `DataProperty` to 1.0.1


**Full Changelog**: https://github.com/thombashi/pytablewriter/compare/v1.0.0...v1.1.0

[Changes][v1.1.0]


<a id="v1.0.0"></a>
# [v1.0.0](https://github.com/thombashi/pytablewriter/releases/tag/v1.0.0) - 2023-06-25

- Add support for Python 3.11
- Drop support for Python 3.6
- Fix a regular expression range of LatexWriter: [#57](https://github.com/thombashi/pytablewriter/issues/57)
- Add support for Elasticsearch 8
- Drop support for Elasticsearch 7
- Reduce import time for non-pandas use 
- Update `pathvalidate` dependency to allow v3
- Bump minimum version requirement of `SimpleSQLite`
- Improve type annotations
- Add `zip_safe=False`
- Change the `Cell` class to an immutable data class
- Update docs
- Replace deprecated `setup.py` calls
- Add `pandas` extras
- Add `__all__` to `__init__.py`
- Remove deprecated functions and properties
    - `dump_tabledata`
    - `set_log_level`
    - `AbstractTableWriter.header_list`
    - `AbstractTableWriter.type_hint_list`
    - `AbstractTableWriter.styles`
    - `AbstractTableWriter.style_list`
    - `AbstractTableWriter.value_preprocessor.setter`

**Full Changelog**: https://github.com/thombashi/pytablewriter/compare/v0.64.2...v1.0.0

[Changes][v1.0.0]


<a id="v0.64.2"></a>
# [v0.64.2](https://github.com/thombashi/pytablewriter/releases/tag/v0.64.2) - 2022-03-21

- Fix to `thousand_separator` of `default_style` not properly applied: [#55](https://github.com/thombashi/pytablewriter/issues/55) (Thanks to [@riklopfer](https://github.com/riklopfer))
- Add support for `PyYAML` v7
- Avoid installation error with `setuptools>=58`
- Modify type annotations:
  - `default_style` property
  - `StyleFilterFunc.__call__` method
  - `ColSeparatorStyleFilterFunc.__call__` method

**Full Changelog**: https://github.com/thombashi/pytablewriter/compare/v0.64.1...v0.64.2


[Changes][v0.64.2]


<a id="v0.64.1"></a>
# [v0.64.1](https://github.com/thombashi/pytablewriter/releases/tag/v0.64.1) - 2021-10-17

- Fix write failed when the inputs include `dict` values: [#52](https://github.com/thombashi/pytablewriter/issues/52) (Thanks to [@rutsam](https://github.com/rutsam))
- Improve write performance

**Full Changelog**: https://github.com/thombashi/pytablewriter/compare/v0.64.0...v0.64.1


[Changes][v0.64.1]


<a id="v0.64.0"></a>
# [v0.64.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.64.0) - 2021-10-02

- Modify to accept `deuote` keyword argument at writer class constructors: [#51](https://github.com/thombashi/pytablewriter/issues/51) (Thanks to [@andormarkus](https://github.com/andormarkus))
- Make it possible to specify type hints by strings


[Changes][v0.64.0]


<a id="v0.63.0"></a>
# [v0.63.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.63.0) - 2021-09-20

- Add `max_precision` argument to writer class constructors: [#44](https://github.com/thombashi/pytablewriter/issues/44)
- Improve output precision of real numbers: [#44](https://github.com/thombashi/pytablewriter/issues/44)
- Remove trailing whitespace when table does not have a name [#46](https://github.com/thombashi/pytablewriter/issues/46) (Thanks to [@movermeyer](https://github.com/movermeyer))
- Fix AsciiDoc table header output: [#47](https://github.com/thombashi/pytablewriter/issues/47) (Thanks to [@jvdvegt](https://github.com/jvdvegt))
- Fix to dequote in cells properly: [#49](https://github.com/thombashi/pytablewriter/issues/49) (Thanks to [@hugovk](https://github.com/hugovk))
- Modify to accept type hints by strings as well
- Add `CodeQL` analysis
- Add type annotations
- Allow `XlsxWriter` v3
- Add `setup-ci` target to Makefile


[Changes][v0.63.0]


<a id="v0.62.0"></a>
# [v0.62.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.62.0) - 2021-07-18

- Add support for `CommonMark` as a flavor for `MarkdownTableWriter` class
- Add support for `kramdown`/`Jeklly` as a flavor for `MarkdownTableWriter` class
- Add support styles(`fg_color`, `bg_color`, `font_weight`, `font_style`) for `AsciiDocTableWriter` class
- Add `table_style` for `MediaWikiTableWriter`: [#43](https://github.com/thombashi/pytablewriter/issues/43)
- Add `overwrite_type_hints` argument to `from_dataframe` method
- Add types to `pytablewirter.typehint`
- Add support for string with thousand separators as integer: [#44](https://github.com/thombashi/pytablewriter/issues/44)
- Add support for string with thousand separators as integer
- Made it possible to set `flavor` as a keyword argument of `MarkdownTableWriter` constructor
- Fix to `flavor` keyword argument properly applied when executing `write_table` method at the second time
- Change to just output warning instead of raising exception when `set_theme` method failed
- Improve error messages when a theme not found
- Improve output precision of numbers: [#44](https://github.com/thombashi/pytablewriter/issues/44)
  - This may increase output decimal places of real numbers compared to the previous versions
- Remove an unused class


[Changes][v0.62.0]


<a id="v0.61.0"></a>
# [v0.61.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.61.0) - 2021-06-16

- Add an alias for `Style.color` as `Style.fg_color`
- Make it possible to set `theme` via writer class constructors
- Make it possible to initialize writer from `dataframe` via writer class constructors
- Fix comparison of `Style.__eq__` method
- Fix CSS output of `HtmlTableWriter.write_table` method when `write_css=True`
- Vendoring `msgfy` package


[Changes][v0.61.0]


<a id="v0.60.0"></a>
# [v0.60.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.60.0) - 2021-05-12

- Add support for AsciiDoc format
- Add format name `ssv` for `SpaceAlignedTableWriter` class
- Make it possible to set `write_callback` via writer class constructors
- Fix format attributes of `UNICODE`/`BOLD_UNICODE` enums
- Remove `es5`/`es6` from `extras_require`


[Changes][v0.60.0]


<a id="v0.59.0"></a>
# [v0.59.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.59.0) - 2021-05-04

- Add support for Python 3.10
- Drop support for Python 3.5
- Markdown alignment cells respect `margin` [#36](https://github.com/thombashi/pytablewriter/issues/36) (Thanks to [@shawalli](https://github.com/shawalli))
- Add validation to margin setter
- Make it possible to set more writer settings via writer class constructors
- Forced to set margin to zero for CSV/sourcecode writer classes
- Fix `_repr_html_` method to properly apply writer settings
- Fix to `margin` value setting changes are properly applied after written a table
- Modify type annotations
- Update requirements


[Changes][v0.59.0]


<a id="v0.58.0"></a>
# [v0.58.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.58.0) - 2020-08-30

- Add `PandasDataFramePickleWriter` class
- Add support for keyword arguments initialization to `TableWriterFactory` instantiation
- Fix initialization by keyword arguments of writer class constructor
- Remove deprecated properties


[Changes][v0.58.0]


<a id="v0.57.0"></a>
# [v0.57.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.57.0) - 2020-08-22

- Add `table_format` property to writer classes
- Add `clear_theme` method to writer classes
- Add `TableFormat.from_file_extension` class method
- Make it possible to initialize writer instance with constructor
- Fix plugin discovery to avoid errors when some of the functions not implemented
- Fix the case that style filters are not properly applied


[Changes][v0.57.0]


<a id="v0.56.1"></a>
# [v0.56.1](https://github.com/thombashi/pytablewriter/releases/tag/v0.56.1) - 2020-08-16

- Add ``theme`` extras


[Changes][v0.56.1]


<a id="v0.56.0"></a>
# [v0.56.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.56.0) - 2020-08-16

- Add `set_theme`/`list_themes` functions to writer classes
- Add `es` extras
- Implement `__repr__` method for text writer classes
- Modify pytest stream detection
- Modify not to raise an error when input data is empty
- Fix to properly propagate `max_workers` value to a dependency package
- Update requirements


[Changes][v0.56.0]


<a id="v0.55.0"></a>
# [v0.55.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.55.0) - 2020-07-26

- Add `enable_ansi_escape` attribute to writer classes: [#30](https://github.com/thombashi/pytablewriter/issues/30) (Thanks to [@calebstewart](https://github.com/calebstewart))
- Add `update` method to Style class
- Modify to disable ANSI escapes during `dump` method execution
- Modify type annotations for `dump` method
- Fix to propagate `enable_ansi_escape`/`colorize_terminal` at `_repr_html_` method
- Fix `colorize_terminal` to clear preprocess data when the value changed
- Update requirements


[Changes][v0.55.0]


<a id="v0.54.0"></a>
# [v0.54.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.54.0) - 2020-05-16

- Add `kwargs` to `dump` method of writer classes
- Add `indent` keyword argument support for `write_table`/`dump`/`dumps` methods
- Add `sort_keys` keyword argument support for `write_table`/`dump`/`dumps` method of JSON writer classes
- Changes to accept list of dict as value_matrix for JSON table writer classes
- Change the default indent level of `JsonTableWriter` class
- Fix output of `JsonLinesTableWriter` for `None` values
- Modify output format of `JsonTableWriter.write_table` method
- Remove `EmptyHeaderError`
- Update requirements


[Changes][v0.54.0]


<a id="v0.53.0"></a>
# [v0.53.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.53.0) - 2020-05-10

- Add GitHub Flavored Markdown support
- Add DecorationLine support as a style
- Add `is_header_row` method to `Cell` class
- Modify type annotations


[Changes][v0.53.0]


<a id="v0.52.0"></a>
# [v0.52.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.52.0) - 2020-05-05

- Add `YamlTableWriter` writer class
- Add `Cell` class
- Add `style_filter_kwargs` attribute to writer classes
- Add `pytablewriter.typehint` module
- Add color support with style
- Make it possible to apply style filter to column separators
- Make it possible to apply part of the style filter to headers
- Make it configurable header row crosspoint characters for text format writer classes
- Make "sort_keys" not True by default [#15](https://github.com/thombashi/pytablewriter/issues/15) (Thanks to [@Zackhardtoname](https://github.com/Zackhardtoname))
- Change to convert `None` values for Style class constructor arguments to default values.
- Improve an error message: [#26](https://github.com/thombashi/pytablewriter/issues/26) (Thanks to [@hugovk](https://github.com/hugovk))
- Change signatures of `StyleFilterFunc`
- Change `max_workers` attribute default value to 1
- Allow non ascii characters for JSON formats
- Fix changing chars for text format tables not properly applied due to initialization order
- Fix `TomlTableWriter` not properly rendered when including `Decimal` values
- Fix `from_tabledata` method not properly propagate `table_name` when the value is None
- Fix `__repr__` method of `Style` class
- Fix style filter to properly apply align
- Update requirements
- Minor bug fixes


[Changes][v0.52.0]


<a id="v0.51.0"></a>
# [v0.51.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.51.0) - 2020-04-12

- Add `BoldUnicodeTableWriter` class
- Add `BorderlessTableWriter` class
- Add underscore support for thousand separators
- Add `TableFormat.from_name` class method
- Add `from_writer` method to writers
- Add vertical align to style (only for `HtmlTableWriter`): [#13](https://github.com/thombashi/pytablewriter/issues/13) (Thanks to [@jimkohl](https://github.com/jimkohl))
- Add `write_css` argument add an interface to write CSS with `HtmlTableWriter`: [#16](https://github.com/thombashi/pytablewriter/issues/16) (Thanks to [@domino-blake](https://github.com/domino-blake))
- Add `AbstractTableWriter` class to public paths
- Add margin property to `AbstractTableWriter` class to avoid lint errors
- Make it possible to apply styles to headers
- Fix to properly apply align for `HtmlTableWriter`
- Make style filter applicable to `HtmlTableWriter`
- Add `CssTableWriter` class
- Fix to include `py.typed` to the package
- Modify type annotations
- Increase priority of the `xlsx` format within `TableFormat`
- Change the default `table_name` value to an empty string
- Update requirements
- Minor bug fixes


[Changes][v0.51.0]


<a id="v0.50.0"></a>
# [v0.50.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.50.0) - 2020-02-24

- Add `add_style_filter` method to writers
- Add type annotations and `py.typed` to the package
- Minor bug fixes


[Changes][v0.50.0]


<a id="v0.49.0"></a>
# [v0.49.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.49.0) - 2020-02-17

- Add `max_workers` property to writers
- Add validation for `default_style` setter
- Change `_font_size_map` to cache


[Changes][v0.49.0]


<a id="v0.48.0"></a>
# [v0.48.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.48.0) - 2020-02-16

- Drop Python 2 support: [#24](https://github.com/thombashi/pytablewriter/issues/24) (Thanks to [@hugovk](https://github.com/hugovk))
- Add support for Python 3.9
- Add support for platforms that lacks support `sem_open` such as Android Termux
- Add `default_style` to writers
- Add `update_preprocessor` method to writers
- Fix backward compatibility with getting `pandas.DataFrame`: [#25](https://github.com/thombashi/pytablewriter/issues/25) (Thanks to [@hugovk](https://github.com/hugovk) )
- Replace the logging library from `Logbook` to `loguru`
- Remove deprecated methods/properties
- Remove `dev` extras_require
- Rename a property from `styles` to `column_styles`

[Changes][v0.48.0]


<a id="v0.47.0"></a>
# [v0.47.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.47.0) - 2020-02-05

- Add support for escape formula injection: [#20](https://github.com/thombashi/pytablewriter/issues/20) (Thanks to [@randomstuff](https://github.com/randomstuff))
  - for CSV/Excel writers
- Replace line breaks to `<br>` tag for HTML table writer: [#22](https://github.com/thombashi/pytablewriter/issues/22) (Thanks to [@kesyog](https://github.com/kesyog))
- Modify to replace line breaks separately


[Changes][v0.47.0]


<a id="v0.46.3"></a>
# [v0.46.3](https://github.com/thombashi/pytablewriter/releases/tag/v0.46.3) - 2020-01-13

- Add support for PyPy
- Add `es7` extras
- Integrate `release` and `build` extras to `dev` extras
- Update requirements


[Changes][v0.46.3]


<a id="v0.46.0"></a>
# [v0.46.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.46.0) - 2019-05-05

- Drop support for `Python 3.4`
- Add deb package to PPA
- Loosen some of the external dependencies version restriction
- Bug fixes

[Changes][v0.46.0]


<a id="v0.45.1"></a>
# [v0.45.1](https://github.com/thombashi/pytablewriter/releases/tag/v0.45.1) - 2019-04-20

- Fix improper type hints behavior for SQLite table writer: [#12](https://github.com/thombashi/pytablewriter/issues/12) (Thanks to [@smcat8](https://github.com/smcat8))

[Changes][v0.45.1]


<a id="v0.45.0"></a>
# [v0.45.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.45.0) - 2019-03-16

- Add `UnicodeTableWriter` class
- Bug fixes
- Do not install on Python 3.3: [#11](https://github.com/thombashi/pytablewriter/issues/11) (Thanks to [@hugovk](https://github.com/hugovk))

[Changes][v0.45.0]


<a id="v0.44.0"></a>
# [v0.44.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.44.0) - 2019-02-18

- Add `pandas.DataFrame` pickle support for `from_dataframe` method
- Add `from_series` method
- Bug fixes


[Changes][v0.44.0]


<a id="v0.43.1"></a>
# [v0.43.1](https://github.com/thombashi/pytablewriter/releases/tag/v0.43.1) - 2019-02-11

- Improve processing performance
- Suppress excessive DeprecationWarning

[Changes][v0.43.1]


<a id="v0.43.0"></a>
# [v0.43.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.43.0) - 2019-02-11

- Improve processing performance
- Add `add_index_column` argument to `from_dataframe`
- Add `register_trans_func` method
- Rename properties:
    - from `type_hint_list` to `type_hints`
    - from `header_list` to `headers`
    - from `style_list` to `styles`
- Remove `value_map` property


[Changes][v0.43.0]


<a id="v0.42.0"></a>
# [v0.42.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.42.0) - 2019-01-27

- Add `trans_func` property
- Change to forbid to assign a `stream` to binary writers
- Change to be more informative when optional packages not installed
- Bug fixes

[Changes][v0.42.0]


<a id="v0.41.2"></a>
# [v0.41.2](https://github.com/thombashi/pytablewriter/releases/tag/v0.41.2) - 2019-01-14

- Fix missing `extras_require` for `html` (Thanks to [@hugovk](https://github.com/hugovk))

[Changes][v0.41.2]


<a id="v0.41.1"></a>
# [v0.41.1](https://github.com/thombashi/pytablewriter/releases/tag/v0.41.1) - 2019-01-14

- Fix the case that changing styles by using `set_style` not properly applied
- Fix `__repr__`/`__eq__` method for `Style` class
- Avoid closing ipykernel OutStream
- Bug fixes

[Changes][v0.41.1]


<a id="v0.41.0"></a>
# [v0.41.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.41.0) - 2019-01-13

- Add `dump` method to writers
- Add support for italic style
- Add `is_opened` method to binary writers
- Fix to apply styles for `_repr_html_` method
- Avoid overwriting the stream when executing `dumps` method
- Loosen external package dependencies
    - Change HTML writer to an extra require
- Bug fixes

[Changes][v0.41.0]


<a id="v0.40.1"></a>
# [v0.40.1](https://github.com/thombashi/pytablewriter/releases/tag/v0.40.1) - 2019-01-09

- Fix Excel writers failed to write

[Changes][v0.40.1]


<a id="v0.40.0"></a>
# [v0.40.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.40.0) - 2019-01-07

- Add `set_style` method to writers
- Add `value_map` attribute to writers
- Improve precision of column ASCII char width calculation
- Suppress applying styles when the value is null
- Bug fixes


[Changes][v0.40.0]


<a id="v0.39.0"></a>
# [v0.39.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.39.0) - 2019-01-06

- Add support for `Style` to ReStructuredText writers
- Bug fixes

[Changes][v0.39.0]


<a id="v0.38.0"></a>
# [v0.38.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.38.0) - 2019-01-02

- Change to accept string values for the `line_break_handling` attribute of writers
- Change `is_write_null_line_after_table` default value of writers from `True` to `False`
- Change `dump_tabledata` function to pass arguments to writer


[Changes][v0.38.0]


<a id="v0.37.0"></a>
# [v0.37.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.37.0) - 2019-01-02

- Add `align`/`thousand_separator`/`font_weight` to Style
- Add `line_break_handling` attribute to writers
- Bug fixes


[Changes][v0.37.0]


<a id="v0.36.1"></a>
# [v0.36.1](https://github.com/thombashi/pytablewriter/releases/tag/v0.36.1) - 2018-11-25

- Add `all` to `extras_require` that enable install all of the extra dependency packages at once
- Fix to avoid executing writers constructor when importing `pytablewriter`

[Changes][v0.36.1]


<a id="v0.36.0"></a>
# [v0.36.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.36.0) - 2018-10-13

- Add support for ANSI escape sequences to text writers: [#6](https://github.com/thombashi/pytablewriter/issues/6) (Thanks to [@hugovk](https://github.com/hugovk))


[Changes][v0.36.0]


<a id="v0.35.0"></a>
# [v0.35.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.35.0) - 2018-10-10

- Loosen external package dependencies

[Changes][v0.35.0]


<a id="v0.34.0"></a>
# [v0.34.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.34.0) - 2018-10-07

- Add `style_list` attribute to writers as an interface to set styles of columns: [#4](https://github.com/thombashi/pytablewriter/issues/4) (thanks to [@jpiter](https://github.com/jpiter))
- Loosen external package dependencies
- Bug fixes

[Changes][v0.34.0]


<a id="v0.33.0"></a>
# [v0.33.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.33.0) - 2018-09-30

- Add `format_list` attribute to set float formatting in a table: [#4](https://github.com/thombashi/pytablewriter/issues/4) (Thanks to [@hugovk](https://github.com/hugovk))
- Improve processing performance
- Enable float formatting in default with `SpaceAlignedTableWriter`
- Bug fixes

[Changes][v0.33.0]


<a id="v0.32.0"></a>
# [v0.32.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.32.0) - 2018-09-17

- Add `dumps` method that returns rendered tabular text: [#3](https://github.com/thombashi/pytablewriter/issues/3) (Thanks to [@nettrino](https://github.com/nettrino))


[Changes][v0.32.0]


<a id="v0.31.0"></a>
# [v0.31.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.31.0) - 2018-07-22

- Add an interface to set alignment for each column of the output table: [#2](https://github.com/thombashi/pytablewriter/issues/2) (Thanks to [@jpoa](https://github.com/jpoa))


[Changes][v0.31.0]


<a id="v0.30.1"></a>
# [v0.30.1](https://github.com/thombashi/pytablewriter/releases/tag/v0.30.1) - 2018-07-15

- Add support for Python 3.7
- Bug fixes

[Changes][v0.30.1]


<a id="v0.30.0"></a>
# [v0.30.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.30.0) - 2018-06-25

- Add support for LDJSON/JSON Lines/NDJSON
- Bug fixes

[Changes][v0.30.0]


<a id="v0.29.0"></a>
# [v0.29.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.29.0) - 2018-06-10

- Add interface to escape HTML tags in cells in a table
- Add `from_tablib` method
- Bug fixes


[Changes][v0.29.0]


<a id="v0.28.1"></a>
# [v0.28.1](https://github.com/thombashi/pytablewriter/releases/tag/v0.28.1) - 2018-05-05

- Fix the case that margins not properly worked
- Loosen external package dependencies


[Changes][v0.28.1]


<a id="v0.28.0"></a>
# [v0.28.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.28.0) - 2018-04-22

- Add an interface to set margin for both sides of each cell for text format writer classes
- Bug fixes

[Changes][v0.28.0]


<a id="v0.27.2"></a>
# [v0.27.2](https://github.com/thombashi/pytablewriter/releases/tag/v0.27.2) - 2018-01-01

- The type detected from the `str` values has been changed from `string` type (deprecated since Elasticsearch 5.x) to `text`/`keyword` type


[Changes][v0.27.2]


<a id="v0.27.1"></a>
# [v0.27.1](https://github.com/thombashi/pytablewriter/releases/tag/v0.27.1) - 2017-11-20

- Fix the improper write output, which occurred when executing `from_tabledata` and `write_table` multiple times consecutively.

[Changes][v0.27.1]


<a id="v0.27.0"></a>
# [v0.27.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.27.0) - 2017-11-19

- Performance improvement

[Changes][v0.27.0]


<a id="v0.26.1"></a>
# [v0.26.1](https://github.com/thombashi/pytablewriter/releases/tag/v0.26.1) - 2017-11-19

- Fix package dependency

[Changes][v0.26.1]


<a id="v0.26.0"></a>
# [v0.26.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.26.0) - 2017-11-12

- Performance improvement
- Loosen package dependency
- Bug fixes

[Changes][v0.26.0]


<a id="v0.25.0"></a>
# [v0.25.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.25.0) - 2017-11-04

- Improve performance for multi-core environments
- Change Latex output to insert padding to align columns
- Fix improper column width calculation for the case that includes mixed value types in a column
- Drop support for Python 3.3


[Changes][v0.25.0]


<a id="v0.24.1"></a>
# [v0.24.1](https://github.com/thombashi/pytablewriter/releases/tag/v0.24.1) - 2017-10-29

- Modify Latex output to optimize for Jupyter Notebook
- Suppress excessive quote output for Excel sheets


[Changes][v0.24.1]


<a id="v0.24.0"></a>
# [v0.24.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.24.0) - 2017-08-20

- Add support for Jupyter Notebook

[Changes][v0.24.0]


<a id="v0.23.1"></a>
# [v0.23.1](https://github.com/thombashi/pytablewriter/releases/tag/v0.23.1) - 2017-07-31

- Add escape processing for vertical bar characters in Markdown table items to get consistent rendering result

[Changes][v0.23.1]


<a id="v0.23.0"></a>
# [v0.23.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.23.0) - 2017-07-23

- Add a table writer class for space aligned values
- Add default headers for Markdown/SQLite table writers that used when headers are null
- Change to preserve spaces in table items
- Change to remove line breaks from headers for text table formats
- Make headers are not mandatory for Pandas writer
- Modify Markdown output format to get more consistent rendering result
- Improve output consistency for SQLite


[Changes][v0.23.0]


<a id="v0.22.0"></a>
# [v0.22.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.22.0) - 2017-07-15

- Add support for LaTeX table/matrix
- Improve real number output precision.for CSV/JSON/LTSV/TOML/TSV


[Changes][v0.22.0]


<a id="v0.21.0"></a>
# [v0.21.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.21.0) - 2017-07-02

- Add `NumPy` writer class
- Add `search_table_format` method to `TableFormat` class
- Add attributes to pandas writer class: `import_pandas_as`/`import_numpy_as` to specify import name
- Modify to sanitize `Elasticsearch` index name
- Bug fixes


[Changes][v0.21.0]


<a id="v0.20.2"></a>
# [v0.20.2](https://github.com/thombashi/pytablewriter/releases/tag/v0.20.2) - 2017-06-29

- Fix the case that incorrect write result when matrix which has uniform size for each row

[Changes][v0.20.2]


<a id="v0.20.0"></a>
# [v0.20.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.20.0) - 2017-06-25

- Add support for Elasticsearch
- Simplify pandas dataframe output
- Change to accept non string values as headers
- Modify log messages
- Bug fixes

[Changes][v0.20.0]


<a id="v0.19.1"></a>
# [v0.19.1](https://github.com/thombashi/pytablewriter/releases/tag/v0.19.1) - 2017-05-03

- Change to write a blank line after writing a text format table


[Changes][v0.19.1]


<a id="v0.19.0"></a>
# [v0.19.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.19.0) - 2017-05-02

- Add SQLite writer
- Improve processing performance
- Bug fixes


[Changes][v0.19.0]


<a id="v0.17.0"></a>
# [v0.17.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.17.0) - 2017-01-08

- Add type hint interface to writer classes
- Improve data type detection
- Add `get_variable_name` method to source code writers to provide an interface that retrieves variable names to be written
- Add an interface to change variable declaration type to `JavaScriptTableWriter` class
  - Change default variable declaration type from `var` to `const`


[Changes][v0.17.0]


<a id="v0.16.0"></a>
# [v0.16.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.16.0) - 2016-12-30

- Add `TOML` format support
- Add `tabledata` property
- Change to all of the source code table writers are required table name
- Improve multibyte character support
- Bug fixes


[Changes][v0.16.0]


<a id="v0.15.0"></a>
# [v0.15.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.15.0) - 2016-12-23

- Add `TSV`/`LTSV` support
- Add `dump_tabledata` function
- Bug fixes


[Changes][v0.15.0]


<a id="v0.14.0"></a>
# [v0.14.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.14.0) - 2016-12-10

- Add `from_csv` method
- Improve multi-byte character support
- Bug fixes


[Changes][v0.14.0]


<a id="v0.13.0"></a>
# [v0.13.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.13.0) - 2016-11-27

- Add pandas DataFrame as a data source
- Improve multi-byte character support


[Changes][v0.13.0]


<a id="v0.12.6"></a>
# [v0.12.6](https://github.com/thombashi/pytablewriter/releases/tag/v0.12.6) - 2016-11-20

- Support multi-byte string formatting
- Bug fixes


[Changes][v0.12.6]


<a id="v0.12.0"></a>
# [v0.12.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.12.0) - 2016-10-30

- Add writer factory
- Bug fixes


[Changes][v0.12.0]


<a id="v0.10.2"></a>
# [v0.10.2](https://github.com/thombashi/pytablewriter/releases/tag/v0.10.2) - 2016-08-10

- Bug fixes


[Changes][v0.10.2]


<a id="v0.10.1"></a>
# [v0.10.1](https://github.com/thombashi/pytablewriter/releases/tag/v0.10.1) - 2016-08-07

- Fix iterative table write


[Changes][v0.10.1]


<a id="v0.10.0"></a>
# [v0.10.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.10.0) - 2016-08-07

- Modify to support the iterative table write with PandasDataFrameWriter class
- Add a switch that write datetime instance formatting to PythonCodeTableWriter/PandasDataFrameWriter
- Bug fixes


[Changes][v0.10.0]


<a id="v0.9.0"></a>
# [v0.9.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.9.0) - 2016-07-31

- Modify error handling of the write_table_iter method


[Changes][v0.9.0]


<a id="v0.8.2"></a>
# [v0.8.2](https://github.com/thombashi/pytablewriter/releases/tag/v0.8.2) - 2016-07-28

- Improve memory efficiency for Python 2


[Changes][v0.8.2]


<a id="v0.8.0"></a>
# [v0.8.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.8.0) - 2016-07-23

- Add MediaWiki format support
- Add writing table with iteration
- Add flag to switch writing format of datetime values as date-time instance or string
- Modify to write will be succeeded when the table header is null
- Bug fixes


[Changes][v0.8.0]


<a id="v0.7.0"></a>
# [v0.7.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.7.0) - 2016-07-17

- Add support for iteration write
- Fix for the case that excel sheet name includes invalid character(s)
- Minor bug fixes


[Changes][v0.7.0]


<a id="v0.6.0"></a>
# [v0.6.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.6.0) - 2016-07-16

- Add support for `.xls` file format: l: Thanks to [@yegorich](https://github.com/yegorich)


[Changes][v0.6.0]


<a id="v0.5.0"></a>
# [v0.5.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.5.0) - 2016-07-10

- Split is_quote_str property to is_quote_header property and is_quote_table property
- Modify default datetime format string
- Fix: For float value formatting apply condition
- Fix: An exception is not correctly handled


[Changes][v0.5.0]


<a id="v0.4.0"></a>
# [v0.4.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.4.0) - 2016-07-09

- Modification for support Decimal: Thanks to [@yegorich](https://github.com/yegorich)
- Minor bug fixes


[Changes][v0.4.0]


<a id="v0.3.0"></a>
# [v0.3.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.3.0) - 2016-07-04

- Add is_float_formatting property
- Fix conversion error when writing data that a version string (such as "3.3.5"): Thanks to [@yegorich](https://github.com/yegorich)


[Changes][v0.3.0]


<a id="v0.2.1"></a>
# [v0.2.1](https://github.com/thombashi/pytablewriter/releases/tag/v0.2.1) - 2016-07-03



[Changes][v0.2.1]


<a id="v0.2.0"></a>
# [v0.2.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.2.0) - 2016-07-03

- Add support for:
  - bool type
  - Infinity value
  - Not a Number


[Changes][v0.2.0]


<a id="v0.1.6"></a>
# [v0.1.6](https://github.com/thombashi/pytablewriter/releases/tag/v0.1.6) - 2016-06-19

- Make pytest-runner a conditional requirement


[Changes][v0.1.6]


<a id="v0.1.4"></a>
# [v0.1.4](https://github.com/thombashi/pytablewriter/releases/tag/v0.1.4) - 2016-05-30

- Fix: PythonCodeTableWriter was written `None` as string (`"None"`). [`cfdf591daf`](https://github.com/thombashi/pytablewriter/commit/cfdf591dafaff0576426a3bda215ed298313563d)
- Fix: PandasDataFrameWriter is not properly write a table. [`9b82a9715a`](https://github.com/thombashi/pytablewriter/commit/9b82a9715a7566a0db7b404558c2ecb7ca8bbff7)
- Change: write null string when a value in a table is None. [`cfdf591daf`](https://github.com/thombashi/pytablewriter/commit/cfdf591dafaff0576426a3bda215ed298313563d)


[Changes][v0.1.4]


<a id="v0.1.3"></a>
# [v0.1.3](https://github.com/thombashi/pytablewriter/releases/tag/v0.1.3) - 2016-05-29

- Fix: converting `None` value to `null` with JavaScriptTableWriter and JsonTableWriter classes


[Changes][v0.1.3]


<a id="v0.1.2"></a>
# [v0.1.2](https://github.com/thombashi/pytablewriter/releases/tag/v0.1.2) - 2016-05-29

- Fix variable name output: [`9a4f264354`](https://github.com/thombashi/pytablewriter/commit/9a4f264354de508d2e91648755a8903362533575)


[Changes][v0.1.2]


<a id="v0.1.0"></a>
# [v0.1.0](https://github.com/thombashi/pytablewriter/releases/tag/v0.1.0) - 2016-05-23



[Changes][v0.1.0]


[v1.2.0]: https://github.com/thombashi/pytablewriter/compare/v1.1.0...v1.2.0
[v1.1.0]: https://github.com/thombashi/pytablewriter/compare/v1.0.0...v1.1.0
[v1.0.0]: https://github.com/thombashi/pytablewriter/compare/v0.64.2...v1.0.0
[v0.64.2]: https://github.com/thombashi/pytablewriter/compare/v0.64.1...v0.64.2
[v0.64.1]: https://github.com/thombashi/pytablewriter/compare/v0.64.0...v0.64.1
[v0.64.0]: https://github.com/thombashi/pytablewriter/compare/v0.63.0...v0.64.0
[v0.63.0]: https://github.com/thombashi/pytablewriter/compare/v0.62.0...v0.63.0
[v0.62.0]: https://github.com/thombashi/pytablewriter/compare/v0.61.0...v0.62.0
[v0.61.0]: https://github.com/thombashi/pytablewriter/compare/v0.60.0...v0.61.0
[v0.60.0]: https://github.com/thombashi/pytablewriter/compare/v0.59.0...v0.60.0
[v0.59.0]: https://github.com/thombashi/pytablewriter/compare/v0.58.0...v0.59.0
[v0.58.0]: https://github.com/thombashi/pytablewriter/compare/v0.57.0...v0.58.0
[v0.57.0]: https://github.com/thombashi/pytablewriter/compare/v0.56.1...v0.57.0
[v0.56.1]: https://github.com/thombashi/pytablewriter/compare/v0.56.0...v0.56.1
[v0.56.0]: https://github.com/thombashi/pytablewriter/compare/v0.55.0...v0.56.0
[v0.55.0]: https://github.com/thombashi/pytablewriter/compare/v0.54.0...v0.55.0
[v0.54.0]: https://github.com/thombashi/pytablewriter/compare/v0.53.0...v0.54.0
[v0.53.0]: https://github.com/thombashi/pytablewriter/compare/v0.52.0...v0.53.0
[v0.52.0]: https://github.com/thombashi/pytablewriter/compare/v0.51.0...v0.52.0
[v0.51.0]: https://github.com/thombashi/pytablewriter/compare/v0.50.0...v0.51.0
[v0.50.0]: https://github.com/thombashi/pytablewriter/compare/v0.49.0...v0.50.0
[v0.49.0]: https://github.com/thombashi/pytablewriter/compare/v0.48.0...v0.49.0
[v0.48.0]: https://github.com/thombashi/pytablewriter/compare/v0.47.0...v0.48.0
[v0.47.0]: https://github.com/thombashi/pytablewriter/compare/v0.46.3...v0.47.0
[v0.46.3]: https://github.com/thombashi/pytablewriter/compare/v0.46.0...v0.46.3
[v0.46.0]: https://github.com/thombashi/pytablewriter/compare/v0.45.1...v0.46.0
[v0.45.1]: https://github.com/thombashi/pytablewriter/compare/v0.45.0...v0.45.1
[v0.45.0]: https://github.com/thombashi/pytablewriter/compare/v0.44.0...v0.45.0
[v0.44.0]: https://github.com/thombashi/pytablewriter/compare/v0.43.1...v0.44.0
[v0.43.1]: https://github.com/thombashi/pytablewriter/compare/v0.43.0...v0.43.1
[v0.43.0]: https://github.com/thombashi/pytablewriter/compare/v0.42.0...v0.43.0
[v0.42.0]: https://github.com/thombashi/pytablewriter/compare/v0.41.2...v0.42.0
[v0.41.2]: https://github.com/thombashi/pytablewriter/compare/v0.41.1...v0.41.2
[v0.41.1]: https://github.com/thombashi/pytablewriter/compare/v0.41.0...v0.41.1
[v0.41.0]: https://github.com/thombashi/pytablewriter/compare/v0.40.1...v0.41.0
[v0.40.1]: https://github.com/thombashi/pytablewriter/compare/v0.40.0...v0.40.1
[v0.40.0]: https://github.com/thombashi/pytablewriter/compare/v0.39.0...v0.40.0
[v0.39.0]: https://github.com/thombashi/pytablewriter/compare/v0.38.0...v0.39.0
[v0.38.0]: https://github.com/thombashi/pytablewriter/compare/v0.37.0...v0.38.0
[v0.37.0]: https://github.com/thombashi/pytablewriter/compare/v0.36.1...v0.37.0
[v0.36.1]: https://github.com/thombashi/pytablewriter/compare/v0.36.0...v0.36.1
[v0.36.0]: https://github.com/thombashi/pytablewriter/compare/v0.35.0...v0.36.0
[v0.35.0]: https://github.com/thombashi/pytablewriter/compare/v0.34.0...v0.35.0
[v0.34.0]: https://github.com/thombashi/pytablewriter/compare/v0.33.0...v0.34.0
[v0.33.0]: https://github.com/thombashi/pytablewriter/compare/v0.32.0...v0.33.0
[v0.32.0]: https://github.com/thombashi/pytablewriter/compare/v0.31.0...v0.32.0
[v0.31.0]: https://github.com/thombashi/pytablewriter/compare/v0.30.1...v0.31.0
[v0.30.1]: https://github.com/thombashi/pytablewriter/compare/v0.30.0...v0.30.1
[v0.30.0]: https://github.com/thombashi/pytablewriter/compare/v0.29.0...v0.30.0
[v0.29.0]: https://github.com/thombashi/pytablewriter/compare/v0.28.1...v0.29.0
[v0.28.1]: https://github.com/thombashi/pytablewriter/compare/v0.28.0...v0.28.1
[v0.28.0]: https://github.com/thombashi/pytablewriter/compare/v0.27.2...v0.28.0
[v0.27.2]: https://github.com/thombashi/pytablewriter/compare/v0.27.1...v0.27.2
[v0.27.1]: https://github.com/thombashi/pytablewriter/compare/v0.27.0...v0.27.1
[v0.27.0]: https://github.com/thombashi/pytablewriter/compare/v0.26.1...v0.27.0
[v0.26.1]: https://github.com/thombashi/pytablewriter/compare/v0.26.0...v0.26.1
[v0.26.0]: https://github.com/thombashi/pytablewriter/compare/v0.25.0...v0.26.0
[v0.25.0]: https://github.com/thombashi/pytablewriter/compare/v0.24.1...v0.25.0
[v0.24.1]: https://github.com/thombashi/pytablewriter/compare/v0.24.0...v0.24.1
[v0.24.0]: https://github.com/thombashi/pytablewriter/compare/v0.23.1...v0.24.0
[v0.23.1]: https://github.com/thombashi/pytablewriter/compare/v0.23.0...v0.23.1
[v0.23.0]: https://github.com/thombashi/pytablewriter/compare/v0.22.0...v0.23.0
[v0.22.0]: https://github.com/thombashi/pytablewriter/compare/v0.21.0...v0.22.0
[v0.21.0]: https://github.com/thombashi/pytablewriter/compare/v0.20.2...v0.21.0
[v0.20.2]: https://github.com/thombashi/pytablewriter/compare/v0.20.0...v0.20.2
[v0.20.0]: https://github.com/thombashi/pytablewriter/compare/v0.19.1...v0.20.0
[v0.19.1]: https://github.com/thombashi/pytablewriter/compare/v0.19.0...v0.19.1
[v0.19.0]: https://github.com/thombashi/pytablewriter/compare/v0.17.0...v0.19.0
[v0.17.0]: https://github.com/thombashi/pytablewriter/compare/v0.16.0...v0.17.0
[v0.16.0]: https://github.com/thombashi/pytablewriter/compare/v0.15.0...v0.16.0
[v0.15.0]: https://github.com/thombashi/pytablewriter/compare/v0.14.0...v0.15.0
[v0.14.0]: https://github.com/thombashi/pytablewriter/compare/v0.13.0...v0.14.0
[v0.13.0]: https://github.com/thombashi/pytablewriter/compare/v0.12.6...v0.13.0
[v0.12.6]: https://github.com/thombashi/pytablewriter/compare/v0.12.0...v0.12.6
[v0.12.0]: https://github.com/thombashi/pytablewriter/compare/v0.10.2...v0.12.0
[v0.10.2]: https://github.com/thombashi/pytablewriter/compare/v0.10.1...v0.10.2
[v0.10.1]: https://github.com/thombashi/pytablewriter/compare/v0.10.0...v0.10.1
[v0.10.0]: https://github.com/thombashi/pytablewriter/compare/v0.9.0...v0.10.0
[v0.9.0]: https://github.com/thombashi/pytablewriter/compare/v0.8.2...v0.9.0
[v0.8.2]: https://github.com/thombashi/pytablewriter/compare/v0.8.0...v0.8.2
[v0.8.0]: https://github.com/thombashi/pytablewriter/compare/v0.7.0...v0.8.0
[v0.7.0]: https://github.com/thombashi/pytablewriter/compare/v0.6.0...v0.7.0
[v0.6.0]: https://github.com/thombashi/pytablewriter/compare/v0.5.0...v0.6.0
[v0.5.0]: https://github.com/thombashi/pytablewriter/compare/v0.4.0...v0.5.0
[v0.4.0]: https://github.com/thombashi/pytablewriter/compare/v0.3.0...v0.4.0
[v0.3.0]: https://github.com/thombashi/pytablewriter/compare/v0.2.1...v0.3.0
[v0.2.1]: https://github.com/thombashi/pytablewriter/compare/v0.2.0...v0.2.1
[v0.2.0]: https://github.com/thombashi/pytablewriter/compare/v0.1.6...v0.2.0
[v0.1.6]: https://github.com/thombashi/pytablewriter/compare/v0.1.4...v0.1.6
[v0.1.4]: https://github.com/thombashi/pytablewriter/compare/v0.1.3...v0.1.4
[v0.1.3]: https://github.com/thombashi/pytablewriter/compare/v0.1.2...v0.1.3
[v0.1.2]: https://github.com/thombashi/pytablewriter/compare/v0.1.0...v0.1.2
[v0.1.0]: https://github.com/thombashi/pytablewriter/tree/v0.1.0

<!-- Generated by https://github.com/rhysd/changelog-from-release v3.8.1 -->
