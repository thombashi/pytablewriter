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

Installation: conda
------------------------------
::

    conda install -c conda-forge pytablewriter

Installation: apt
------------------------------
::

    sudo add-apt-repository ppa:thombashi/ppa
    sudo apt update
    sudo apt install python3-pytablewriter
