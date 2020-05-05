Installation
============

Install from PyPI
------------------------------
::

    pip install pytablewriter

Some of the formats require additional dependency packages, you can install the dependency packages as follows:

- Elasticsearch
    - ``pip install pytablewriter[es6]`` or ``pip install pytablewriter[es5]``
- Excel
    - ``pip install pytablewriter[excel]``
- HTML
    - ``pip install pytablewriter[html]``
- SQLite
    - ``pip install pytablewriter[sqlite]``
- TOML
    - ``pip install pytablewriter[toml]``
- Install all of the optioanal dependencies
    - ``pip install pytablewriter[all]``

Install from PPA (for Ubuntu)
------------------------------
::

    sudo add-apt-repository ppa:thombashi/ppa
    sudo apt update
    sudo apt install python3-pytablewriter


Dependencies
============
Python 3.5+

- `DataProperty <https://github.com/thombashi/DataProperty>`__
- `mbstrdecoder <https://github.com/thombashi/mbstrdecoder>`__
- `msgfy <https://github.com/thombashi/msgfy>`__
- `pathvalidate <https://github.com/thombashi/pathvalidate>`__
- `tabledata <https://github.com/thombashi/tabledata>`__
- `tcolorpy <https://github.com/thombashi/tcolorpy>`__
- `typepy <https://github.com/thombashi/typepy>`__

Optional dependencies
---------------------
- `loguru <https://github.com/Delgan/loguru>`__
    - Used for logging if the package installed
- `pytablereader <https://github.com/thombashi/pytablereader>`__
- `simplejson <https://github.com/simplejson/simplejson>`__
- Elasticsearch:
    - `elasticsearch <https://github.com/elastic/elasticsearch-py>`__
- Excel
    - `xlwt <http://www.python-excel.org/>`__
    - `XlsxWriter <https://github.com/jmcnamara/XlsxWriter>`__
- HTML
    - `dominate <https://github.com/Knio/dominate/>`__
- SQLite
    - `SimpleSQLite <https://github.com/thombashi/SimpleSQLite>`__
- TOML
    - `toml <https://github.com/uiri/toml>`__


Test dependencies
-----------------
- `pytest <https://docs.pytest.org/en/latest/>`__
- `tox <https://testrun.org/tox/latest/>`__
