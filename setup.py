#!/usr/bin/python3
from setuptools import setup
import io
import os

# Package meta-data
NAME = "twint_fork"
DESCRIPTION = "An advanced Twitter scraping & OSINT tool."
URL = "https://github.com/yihong0618/twint"
EMAIL = "codyzacharias@pm.me, zouzou0208@gmail.com"
AUTHOR = "Cody Zacharias, yihong0618"
REQUIRES_PYTHON = ">=3.7.0"
VERSION = None

# Packages required
REQUIRED = [
    "aiohttp",
    "aiodns",
    "beautifulsoup4",
    "cchardet",
    "dataclasses",
    "elasticsearch",
    "pysocks",
    "pandas",
    "aiohttp_socks",
    "schedule",
    "geopy",
    "fake-useragent",
    "googletransx",
]

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

setup(
    name=NAME,
    version="2.5.0",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=["twint", "twint.storage"],
    entry_points={
        "console_scripts": [
            "twint = twint.cli:run_as_command",
        ],
    },
    install_requires=REQUIRED,
    dependency_links=["git+https://github.com/x0rzkov/py-googletrans#egg=googletrans"],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
