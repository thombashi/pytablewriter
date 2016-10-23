import sys
import os.path
import setuptools

REQUIREMENT_DIR = "requirements"

needs_pytest = set(['pytest', 'test', 'ptr']).intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

with open("README.rst") as fp:
    long_description = fp.read()

with open(os.path.join("docs", "pages", "introduction", "summary.txt")) as f:
    summary = f.read()

with open(os.path.join(REQUIREMENT_DIR, "requirements.txt")) as f:
    install_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "test_requirements.txt")) as f:
    tests_require = [line.strip() for line in f if line.strip()]

setuptools.setup(
    name="pytablewriter",
    version="0.11.0",
    author="Tsuyoshi Hombashi",
    author_email="gogogo.vm@gmail.com",
    url="https://github.com/thombashi/pytablewriter",
    license="MIT License",
    description=summary,
    include_package_data=True,
    install_requires=install_requires,
    keywords=[
        "table", "CSV", "Excel", "JavaScript", "JSON",
        "Markdown", "MediaWiki", "HTML", "Pandas", "reStructuredText",
    ],
    long_description=long_description,
    packages=setuptools.find_packages(exclude=['test*']),
    setup_requires=pytest_runner,
    tests_require=tests_require,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
