#!/usr/bin/env python
import os
from pathlib import Path

from setuptools import setup

with open("serving/core/__init__.py") as file:
    for line in file.readlines():
        if "version" in line:
            version = line.split("=")[1].strip().replace('"', "")
            break

assert (
    os.path.exists(os.path.join("serving", "__init__.py")) is False
), "serving is a namespace not a module"

extra_requires = {"plugins": ["importlib_resources"]}
extra_requires["all"] = sorted(set(sum(extra_requires.values(), [])))

if __name__ == "__main__":
    setup(
        name="serving",
        version=version,
        extras_require=extra_requires,
        description="Pytorch serving POC",
        long_description=(Path(__file__).parent / "README.rst").read_text(),
        author="Delaunay",
        author_email="setepenre@outlook.com",
        license="BSD 3-Clause License",
        url="https://serving.readthedocs.io",
        classifiers=[
            "License :: OSI Approved :: BSD License",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Operating System :: OS Independent",
        ],
        packages=[
            "serving.core",
            "serving.plugins.example",
        ],
        setup_requires=["setuptools"],
        install_requires=["importlib_resources"],
        namespace_packages=[
            "serving",
            "serving.plugins",
        ],
        package_data={
            "serving.data": [
                "serving/data",
            ],
        },
    )
