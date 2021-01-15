# coding: utf8
"""
Setup script for otbenchmark
============================

This script allows to install otbenchmark within the Python environment.

Usage
-----
::

    python setup.py install

"""
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="otbenchmark",
    keywords=("OpenTURNS", "benchmark"),
    version="0.1",
    packages=find_packages(),
    install_requires=["numpy", "matplotlib", "scipy", "openturns"],
    description="Benchmark problems for OpenTURNS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Natural Language :: French",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering",
    ],
    license="LGPL",
    url="https://github.com/mbaudin47/otbenchmark",
    include_package_data=True,
    maintainer="Michaël Baudin",
    maintainer_email="michael.baudin@edf.fr",
    author="Michaël Baudin, Youssef Jebroun, Elias Fekhari and Vincent Chabridon",
    author_email="michael.baudin@edf.fr",
)
