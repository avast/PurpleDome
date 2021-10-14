#!/usr/bin/env python3

""" Generate human readable document describing the attack based on an attack log """

import argparse
from app.doc_generator import DocGenerator

DEFAULT_ATTACK_LOG = "removeme/loot/2021_09_08___07_41_35/attack.json"  # FIN 7 first run on environment


def create_parser():
    """ Creates the parser for the command line arguments"""
    parser = argparse.ArgumentParser("Controls an experiment on the configured systems")

    parser.add_argument("--attack_log", default=DEFAULT_ATTACK_LOG, help="The attack log the document is based on")
    parser.add_argument("--outfile", default="tools/human_readable_documentation/source/contents.rst", help="The default output file")

    return parser


if __name__ == "__main__":
    arguments = create_parser().parse_args()

    dg = DocGenerator()
    dg.generate(arguments.attack_log, arguments.outfile)
