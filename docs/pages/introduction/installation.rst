Installation
============

Installation: pip
------------------------------
::

    pip install pytablewriter

Some of the formats require additional dependency packages, you can install these packages as follows:

- Elasticsearch
    - ``pip install pytablewriter[es]``
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
- Python 3.5+
- `Python package dependencies (automatically installed) <https://github.com/thombashi/pytablewriter/network/dependencies>`__


Optional dependencies
---------------------
- ``logging`` extras
    - `loguru <https://github.com/Delgan/loguru>`__: Used for logging if the package installed
- ``from`` extras
    - `pytablereader <https://github.com/thombashi/pytablereader>`__
- ``es`` extra
    - `elasticsearch <https://github.com/elastic/elasticsearch-py>`__
- ``excel`` extras
    - `xlwt <http://www.python-excel.org/>`__
    - `XlsxWriter <https://github.com/jmcnamara/XlsxWriter>`__
- ``html`` extras
    - `dominate <https://github.com/Knio/dominate/>`__
- ``sqlite`` extras
    - `SimpleSQLite <https://github.com/thombashi/SimpleSQLite>`__
- ``theme`` extras
    - `pytablewriter-altrow-theme <https://github.com/thombashi/pytablewriter-altrow-theme>`__
- ``toml`` extras
    - `toml <https://github.com/uiri/toml>`__


