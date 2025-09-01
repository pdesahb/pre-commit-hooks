#!/usr/bin/env python3
from __future__ import annotations

from setuptools import find_packages
from setuptools import setup

setup(
    name="pre-commit-hooks",
    description="Some out-of-the-box hooks for pre-commit.",
    url="https://github.com/pre-commit/pre-commit-hooks",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    packages=find_packages(exclude=("tests*", "testing*")),
    install_requires=[
        "identify>=2.0.0",
        "PyYAML>=5.1",
        "toml>=0.0.18",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "check-commit-size = pre_commit_hooks.check_commit_size:main",
        ],
    },
)
