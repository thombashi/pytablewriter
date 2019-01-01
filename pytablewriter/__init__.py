# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import

from typepy import (
    Bool,
    DateTime,
    Dictionary,
    Infinity,
    Integer,
    IpAddress,
    List,
    Nan,
    NoneType,
    NullString,
    RealNumber,
    String,
)

from .__version__ import __author__, __copyright__, __email__, __license__, __version__
from ._factory import TableWriterFactory
from ._function import dump_tabledata
from ._logger import set_log_level, set_logger
from ._table_format import FormatAttr, TableFormat
from .error import (
    EmptyHeaderError,
    EmptyTableDataError,
    EmptyTableNameError,
    EmptyValueError,
    NotSupportedError,
    WriterNotFoundError,
)
from .style import Align, Format
from .writer import (
    CsvTableWriter,
    ElasticsearchWriter,
    ExcelXlsTableWriter,
    ExcelXlsxTableWriter,
    HtmlTableWriter,
    JavaScriptTableWriter,
    JsonLinesTableWriter,
    JsonTableWriter,
    LatexMatrixWriter,
    LatexTableWriter,
    LtsvTableWriter,
    MarkdownTableWriter,
    MediaWikiTableWriter,
    NullTableWriter,
    NumpyTableWriter,
    PandasDataFrameWriter,
    PythonCodeTableWriter,
    RstCsvTableWriter,
    RstGridTableWriter,
    RstSimpleTableWriter,
    SpaceAlignedTableWriter,
    SqliteTableWriter,
    TomlTableWriter,
    TsvTableWriter,
)
from .writer._table_writer import LineBreakHandling
