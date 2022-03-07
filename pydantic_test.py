#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
""" A command line tool to verify PurpleDome configuration files """

import argparse
from pprint import pprint
import sys
import argcomplete

import yaml
from app.config_verifier import MainConfig


def load(filename):
    """ Loads the config file and feeds it into the built in verifier """
    with open(filename, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
        return MainConfig(**data)


def create_parser():
    """ Creates the parser for the command line arguments"""
    lparser = argparse.ArgumentParser("Parse a config file and verifies it")

    lparser.add_argument('--filename', default="experiment_ng.yaml", help="Config file to verify")

    return lparser


if __name__ == "__main__":
    parser = create_parser()
    argcomplete.autocomplete(parser)
    arguments = parser.parse_args()
    try:
        r = load(arguments.filename)
    except TypeError as e:
        print("Config file has error(s):")
        print(e)
        sys.exit(1)
    print("Loaded successfully: ")
    pprint(r)

    sys.exit(0)
