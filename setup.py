"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""


import os.path
from typing import Dict

import setuptools


MODULE_NAME = "pytablewriter"
REPOSITORY_URL = f"https://github.com/thombashi/{MODULE_NAME:s}"
REQUIREMENT_DIR = "requirements"
ENCODING = "utf8"

pkg_info: Dict[str, str] = {}


def get_release_command_class() -> Dict[str, setuptools.Command]:
    try:
        from releasecmd import ReleaseCommand
    except ImportError:
        return {}

    return {"release": ReleaseCommand}


with open(os.path.join(MODULE_NAME, "__version__.py")) as f:
    exec(f.read(), pkg_info)

with open("README.rst", encoding=ENCODING) as f:
    long_description = f.read()

with open(os.path.join("docs", "pages", "introduction", "summary.txt"), encoding=ENCODING) as f:
    summary = f.read().strip()

with open(os.path.join(REQUIREMENT_DIR, "requirements.txt")) as f:
    install_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "test_requirements.txt")) as f:
    tests_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "docs_requirements.txt")) as f:
    docs_requires = [line.strip() for line in f if line.strip()]

setuptools_require = ["setuptools>=38.3.0"]

excel_requires = ["xlwt", "XlsxWriter>=0.9.6,<2"]
es7_requires = ["elasticsearch>=7.0.5,<8"]
from_requires = ["pytablereader>=0.30.0,<2"]
html_requires = ["dominate>=2.1.5,<3"]
logging_requires = ["loguru>=0.4.1,<1"]
sqlite_requires = ["SimpleSQLite>=1.1.3,<2"]
theme_requires = ["pytablewriter-altrow-theme>=0.0.2,<1"]
toml_requires = ["toml>=0.9.3,<1"]
yaml_requires = ["PyYAML>=3.11,<6"]
optional_requires = ["simplejson>=3.8.1,<4"]
all_requires = (
    excel_requires
    + es7_requires
    + from_requires
    + html_requires
    + logging_requires
    + sqlite_requires
    + theme_requires
    + toml_requires
    + yaml_requires
    + optional_requires
)
tests_requires = list(set(tests_requires + all_requires))

setuptools.setup(
    name=MODULE_NAME,
    version=pkg_info["__version__"],
    url=REPOSITORY_URL,
    author=pkg_info["__author__"],
    author_email=pkg_info["__email__"],
    description=summary,
    include_package_data=True,
    keywords=[
        "table",
        "CSV",
        "Excel",
        "JavaScript",
        "JSON",
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
    long_description=long_description,
    long_description_content_type="text/x-rst",
    packages=setuptools.find_packages(exclude=["test*"]),
    package_data={MODULE_NAME: ["py.typed"]},
    project_urls={
        "Documentation": f"https://{MODULE_NAME:s}.rtfd.io/",
        "Source": REPOSITORY_URL,
        "Tracker": f"{REPOSITORY_URL:s}/issues",
        "Changes": f"{REPOSITORY_URL:s}/releases",
    },
    python_requires=">=3.6",
    install_requires=setuptools_require + install_requires,
    setup_requires=setuptools_require,
    extras_require={
        "all": all_requires,
        "docs": docs_requires,
        "excel": excel_requires,
        "es7": es7_requires,
        "es": es7_requires,
        "html": html_requires,
        "from": from_requires,
        "logging": logging_requires,
        "sqlite": sqlite_requires,
        "test": tests_requires,
        "theme": theme_requires,
        "toml": toml_requires,
        "yaml": yaml_requires,
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Text Processing :: Markup :: LaTeX",
    ],
    cmdclass=get_release_command_class(),
)
