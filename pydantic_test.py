#!/usr/bin/env python3

""" A command line tool to verify PurpleDome configuration files """

import argparse
from pprint import pprint
import sys
import yaml
from app.config_verifier import MainConfig


def load(filename):
    """ Loads the config file and feeds it into the built in verifier """
    with open(filename) as fh:
        data = yaml.safe_load(fh)
        return MainConfig(**data)


def create_parser():
    """ Creates the parser for the command line arguments"""
    parser = argparse.ArgumentParser("Parse a config file and verifies it")

    parser.add_argument('--filename', default="experiment_ng.yaml")

    return parser


if __name__ == "__main__":
    arguments = create_parser().parse_args()
    try:
        r = load(arguments.filename)
    except TypeError as e:
        print("Config file has error(s):")
        print(e)
        sys.exit(1)
    print("Loaded successfully: ")
    pprint(r)

    sys.exit(0)
