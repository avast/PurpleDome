#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
""" Generate human readable document describing the attack based on an attack log """

import argparse
import argcomplete
from app.doc_generator import DocGenerator

DEFAULT_ATTACK_LOG = "removeme/loot/2021_09_08___07_41_35/attack.json"  # FIN 7 first run on environment


def create_parser():
    """ Creates the parser for the command line arguments"""
    lparser = argparse.ArgumentParser("Controls an experiment on the configured systems")

    lparser.add_argument("--attack_log", default=DEFAULT_ATTACK_LOG, help="The attack log the document is based on")
    lparser.add_argument("--outfile", default="tools/human_readable_documentation/source/contents.rst", help="The default output file")

    return lparser


if __name__ == "__main__":
    parser = create_parser()
    argcomplete.autocomplete(parser)
    arguments = parser.parse_args()

    dg = DocGenerator()
    dg.generate(arguments.attack_log, arguments.outfile)
