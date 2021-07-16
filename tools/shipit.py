#!/usr/bin/env python3

# A python tool to compress the relevant project files.

import glob
import zipfile
import os

filename = "shipit.zip"

globs = ["TODO.md",
         ".gitignore",
         "*.py",
         "CONTRIBUTING.txt",
         "experiment.yaml",
         "cloud_experiment.yaml",
         "Makefile",
         "*.sh",
         "README.md",
         "requirements.txt",
         "tox.ini",
         "app/*.py",
         "tools/*.py",
         "tests/*.py",
         "systems/Vagrantfile",
         "systems/*/*.sh",
         "systems/*/*.bat",
         "systems/azure_attacker"
         "doc/source",
         "doc/source/conf.py",
         "doc/source/asciinema/*",
         "doc/source/index.rst",
         "doc/Makefile",
         "doc/purpledome.pdf",
         "doc/documentation.zip",
         "doc/source/*/*.rst",
         "doc/source/_static/*.png",
         "doc/source/_templates/*",
         "tests/data/*.yaml",
         "plugins/base/*.py",
         "plugins/default/*/*/*.py",
         "plugins/default/*/*/*.txt",
         "plugins/default/*/*/*.md",
         "plugins/default/*/**/*.exe",
         "plugins/default/*/**/*.ps1",
         "plugins/default/*/*/*.yaml",
         "plugins/default/*/*/*.dll",
         "plugins/default/*/*/*.dll_*",
         "plugins/default/*/*/*.reg",
         "plugins/avast_internal_plugins/*/*/*.py",
         "plugins/avast_internal_plugins/*/*/*.bat",
         "plugins/avast_internal_plugins/*/*/*.txt",
         "plugins/avast_internal_plugins/*/*/*.md",
         "plugins/avast_internal_plugins/*/*/*.yaml",
         "plugins/avast_internal_plugins/*/*/*.exe",
         "plugins/avast_internal_plugins/*/*/*.dll",
         "plugins/avast_internal_plugins/*/*/*.dll_*",
         "plugins/avast_internal_plugins/*/*/*.reg",
         "plugins/avast_internal_plugins/*/*/idpx",
         "plugins/avast_internal_plugins/*/*/hosts",
         "plugins/README.md",
         "pylint.rc",
         "shipit_log.txt",
         "all_caldera_attacks_unique.txt",
         "caldera_subset.txt"]

try:
    os.remove(filename)
except FileNotFoundError:
    pass

with zipfile.ZipFile(filename, "w") as zfh:
    for gs in globs:
        for g in glob.iglob(gs, recursive=True):
            print(g)
            zfh.write(g)
