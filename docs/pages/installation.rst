Installation
============
::

    pip install pytablewriter

Some of the formats require additional packages, you can download the packages as follows:

- Elasticsearch
    - ``pip install pytablewriter[es6]`` or ``pip install pytablewriter[es5]``
- Excel
    - ``pip install pytablewriter[excel]``
- SQLite
    - ``pip install pytablewriter[sqlite]``
- TOML
    - ``pip install pytablewriter[toml]``


Dependencies
============
Python 2.7+ or 3.4+

- `DataPropery <https://github.com/thombashi/DataProperty>`__
- `dominate <https://github.com/Knio/dominate/>`__
- `logbook <https://logbook.readthedocs.io/en/stable/>`__
- `mbstrdecoder <https://github.com/thombashi/mbstrdecoder>`__
- `msgfy <https://github.com/thombashi/msgfy>`__
- `pathvalidate <https://github.com/thombashi/pathvalidate>`__
- `six <https://pypi.org/project/six/>`__
- `tabledata <https://github.com/thombashi/tabledata>`__
- `typepy <https://github.com/thombashi/typepy>`__

Optional Dependencies
----------------------------------
- `pytablereader <https://github.com/thombashi/pytablereader>`__
- `simplejson <https://github.com/simplejson/simplejson>`__
- Elasticsearch:
    - `elasticsearch <https://github.com/elastic/elasticsearch-py>`__
- Excel
    - `xlwt <http://www.python-excel.org/>`__
    - `XlsxWriter <https://github.com/jmcnamara/XlsxWriter>`__
- SQLite
    - `SimpleSQLite <https://github.com/thombashi/SimpleSQLite>`__
- TOML
    - `toml <https://github.com/uiri/toml>`__


Test dependencies
-----------------
- `pytest <https://docs.pytest.org/en/latest/>`__
- `pytest-runner <https://github.com/pytest-dev/pytest-runner>`__
- `tox <https://testrun.org/tox/latest/>`__
