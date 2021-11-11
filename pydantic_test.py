#!/usr/bin/env python3

import argparse
import yaml
from app.config_verifier import MainConfig


def load(filename):
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
    r = load(arguments.filename)
    print(r)
    print(r.caldera.apikey)
    # print(r.blarg)
    print(dir(r.__dict__))
