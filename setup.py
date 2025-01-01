"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

import os.path
import re
from typing import Final

import setuptools


MODULE_NAME: Final = "pytablewriter"
REPOSITORY_URL: Final = f"https://github.com/thombashi/{MODULE_NAME:s}"
REQUIREMENT_DIR: Final = "requirements"
ENCODING: Final = "utf8"

pkg_info: dict[str, str] = {}


def get_release_command_class() -> dict[str, type[setuptools.Command]]:
    try:
        from releasecmd import ReleaseCommand
    except ImportError:
        return {}

    return {"release": ReleaseCommand}


def make_long_description() -> str:
    # ref: https://github.com/pypa/readme_renderer/issues/304
    re_exclude = re.compile(r"\s*:scale:\s*\d+")

    with open("README.rst", encoding=ENCODING) as f:
        return "".join([line for line in f if not re_exclude.search(line)])


with open(os.path.join(MODULE_NAME, "__version__.py")) as f:
    exec(f.read(), pkg_info)

with open(os.path.join("docs", "pages", "introduction", "summary.txt"), encoding=ENCODING) as f:
    summary = f.read().strip()

with open(os.path.join(REQUIREMENT_DIR, "requirements.txt")) as f:
    install_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "test_requirements.txt")) as f:
    tests_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "docs_requirements.txt")) as f:
    docs_requires = [line.strip() for line in f if line.strip()]

setuptools_require = ["setuptools>=38.3.0"]

excel_requires = ["xlwt", "XlsxWriter>=0.9.6,<4"]
es8_requires = ["elasticsearch>=8.0.1,<9"]
from_requires = ["pytablereader>=0.31.3,<2"]
html_requires = ["dominate>=2.1.5,<3"]
logging_requires = ["loguru>=0.4.1,<1"]
sqlite_requires = ["SimpleSQLite>=1.3.2,<2"]
theme_requires = [
    "pytablewriter-altrow-theme>=0.2.0,<1",
    "pytablewriter-altcol-theme>=0.1.0,<1",
]
toml_requires = ["toml>=0.9.3,<1"]
yaml_requires = ["PyYAML>=3.11,<7"]
optional_requires = ["simplejson>=3.8.1,<4"]
pandas_requires = ["pandas>=0.25.3,<3"]
all_requires = (
    excel_requires
    + es8_requires
    + from_requires
    + html_requires
    + logging_requires
    + sqlite_requires
    + theme_requires
    + toml_requires
    + yaml_requires
    + optional_requires
    + pandas_requires
)
tests_requires = list(set(tests_requires + all_requires))

setuptools.setup(
    name=MODULE_NAME,
    url=REPOSITORY_URL,
    author=pkg_info["__author__"],
    author_email=pkg_info["__email__"],
    description=summary,
    include_package_data=True,
    keywords=[
        "AsciiDoc",
        "table",
        "CSV",
        "Excel",
        "JavaScript",
        "JSON",
        "LaTeX",
        "LTSV",
        "Markdown",
        "MediaWiki",
        "HTML",
        "pandas",
        "reStructuredText",
        "SQLite",
        "TSV",
        "TOML",
    ],
    license=pkg_info["__license__"],
    long_description=make_long_description(),
    long_description_content_type="text/x-rst",
    packages=setuptools.find_packages(exclude=["test*"]),
    package_data={MODULE_NAME: ["py.typed"]},
    project_urls={
        "Changelog": f"{REPOSITORY_URL:s}/blob/master/CHANGELOG.md",
        "Documentation": f"https://{MODULE_NAME:s}.rtfd.io/",
        "Funding": "https://github.com/sponsors/thombashi",
        "Source": REPOSITORY_URL,
        "Tracker": f"{REPOSITORY_URL:s}/issues",
    },
    python_requires=">=3.9",
    install_requires=setuptools_require + install_requires,
    setup_requires=setuptools_require,
    extras_require={
        "all": all_requires,
        "docs": docs_requires + all_requires,
        "es": es8_requires,
        "es8": es8_requires,
        "excel": excel_requires,
        "from": from_requires,
        "html": html_requires,
        "logging": logging_requires,
        "pandas": pandas_requires,
        "sqlite": sqlite_requires,
        "test": tests_requires,
        "theme": theme_requires,
        "toml": toml_requires,
        "yaml": yaml_requires,
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Text Processing :: Markup :: LaTeX",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Text Processing :: Markup :: reStructuredText",
        "Typing :: Typed",
    ],
    cmdclass=get_release_command_class(),
    zip_safe=False,
)
