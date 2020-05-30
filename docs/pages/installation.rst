Installation
============

Installation: pip
------------------------------
::

    pip install pytablewriter

Some of the formats require additional dependency packages, you can install these packages as follows:

- Elasticsearch
    - ``pip install pytablewriter[es7]`` or ``pip install pytablewriter[es6]``
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

Installation: apt
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


