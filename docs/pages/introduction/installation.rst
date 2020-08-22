Installation
============

Installation: pip
------------------------------
::

    pip install pytablewriter

Some of the formats require additional dependency packages, you can install these packages as follows:

.. csv-table:: Installation of optional dependencies
    :header: Installation example, Remark

    ``pip install pytablewriter[es]``, Elasticsearch
    ``pip install pytablewriter[excel]``, Excel
    ``pip install pytablewriter[html]``, HTML
    ``pip install pytablewriter[sqlite]``, SQLite
    ``pip install pytablewriter[toml]``, TOML
    ``pip install pytablewriter[theme]``, Theme plugins
    ``pip install pytablewriter[all]``, Install all of the optioanal dependencies

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
