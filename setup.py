#!/usr/bin/env python3
""" Setup configuration. Required by Tox. """

import setuptools


# https://packaging.python.org/tutorials/packaging-projects/
# https://setuptools.readthedocs.io/en/latest/

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="purpledome-thorsten-sick",  # Replace with your own username
    version="0.0.1",
    author="Thorsten Sick",
    author_email="thorsten.sick@avast.com",
    description="An attack environment to simulated malware attacks on targets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/avast/PurpleDome",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
