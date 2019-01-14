# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import io
import os.path
import sys

import setuptools


MODULE_NAME = "pytablewriter"
REPOSITORY_URL = "https://github.com/thombashi/{:s}".format(MODULE_NAME)
REQUIREMENT_DIR = "requirements"
ENCODING = "utf8"

pkg_info = {}


def need_pytest():
    return set(["pytest", "test", "ptr"]).intersection(sys.argv)


def get_release_command_class():
    try:
        from releasecmd import ReleaseCommand
    except ImportError:
        return {}

    return {"release": ReleaseCommand}


with open(os.path.join(MODULE_NAME, "__version__.py")) as f:
    exec(f.read(), pkg_info)

with io.open("README.rst", encoding=ENCODING) as f:
    long_description = f.read()

with io.open(os.path.join("docs", "pages", "introduction", "summary.txt"), encoding=ENCODING) as f:
    summary = f.read().strip()

with open(os.path.join(REQUIREMENT_DIR, "requirements.txt")) as f:
    install_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "test_requirements.txt")) as f:
    tests_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "docs_requirements.txt")) as f:
    docs_requires = [line.strip() for line in f if line.strip()]

setuptools_require = ["setuptools>=38.3.0"]
pytest_runner_require = ["pytest-runner"] if need_pytest() else []

excel_requires = ["xlwt", "XlsxWriter>=1.1.2,<2.0.0"]
es6_requires = ["elasticsearch>=6.2.0,<7.0.0"]
from_requires = ["pytablereader>=0.23.0,<1.0.0"]
html_requires = ["dominate>=2.3.5,<3.0.0"]
logging_requires = ["Logbook>=1.1.0,<2.0.0"]
sqlite_requires = ["SimpleSQLite>=0.34.0,<1.0.0"]
toml_requires = ["toml>=0.9.4,<1.0.0"]
optional_requires = ["simplejson>=3.16,<4.0"]
all_requires = (
    excel_requires
    + es6_requires
    + from_requires
    + html_requires
    + logging_requires
    + sqlite_requires
    + toml_requires
    + optional_requires
)
tests_requires = frozenset(tests_requires + all_requires)

setuptools.setup(
    name=MODULE_NAME,
    version=pkg_info["__version__"],
    url=REPOSITORY_URL,

    author=pkg_info["__author__"],
    author_email=pkg_info["__email__"],
    description=summary,
    include_package_data=True,
    keywords=[
        "table", "CSV", "Excel", "JavaScript", "JSON", "LTSV", "Markdown", "MediaWiki", "HTML",
        "pandas", "reStructuredText", "SQLite", "TSV", "TOML",
    ],
    license=pkg_info["__license__"],
    long_description=long_description,
    packages=setuptools.find_packages(exclude=["test*"]),
    project_urls={
        "Documentation": "https://{:s}.rtfd.io/".format(MODULE_NAME),
        "Source": REPOSITORY_URL,
        "Tracker": "{:s}/issues".format(REPOSITORY_URL),
    },

    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*',
    install_requires=setuptools_require + install_requires,
    setup_requires=setuptools_require + pytest_runner_require,
    tests_require=tests_requires,
    extras_require={
        "all": all_requires,
        "build": ["wheel"],
        "docs": docs_requires,
        "excel": excel_requires,
        "es5": ["elasticsearch>=5.5.2,<6.0.0"],
        "es6": es6_requires,
        "html": html_requires,
        "from": from_requires,
        "logging": logging_requires,
        "release": ["releasecmd>=0.0.12,<0.1.0"],
        "sqlite": sqlite_requires,
        "test": tests_requires,
        "toml": toml_requires,
    },

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
    ],
    cmdclass=get_release_command_class())
