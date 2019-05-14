# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""

import re
from setuptools import setup

# Should equal quasardb api version
version = "3.3.1"


setup(
    name = "qdb-cloudwatch",
    packages = ["qdb_cloudwatch"],
    entry_points = {
        "console_scripts": ['qdb-cloudwatch = qdb_cloudwatch.exporter:main']
        },
    version = version,
    description = "Command line utility to export QuasarDB metrics.",

    install_requires=[
        "boto3 >= 1.9",
        "requests",
        "quasardb >= 3.3.1"],

    )
