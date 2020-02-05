"""
Unit tests at Windows environments required to invoke from py module,
because of multiprocessing:
https://py.rtfd.io/en/latest/faq.html?highlight=cmdline#issues-with-py-test-multiprocess-and-setuptools
"""

import sys

import py


if __name__ == "__main__":
    sys.exit(py.test.cmdline.main())
