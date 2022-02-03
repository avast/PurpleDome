#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
""" Generate human readable document describing the attack based on an attack log """

import argparse
import argcomplete
from app.doc_generator import DocGenerator


class CmdlineArgumentException(Exception):
    """ An error in the user supplied command line """


def create(arguments):
    """ Create a document """

    if arguments.attack_log is None:
        raise CmdlineArgumentException("Creating a new document requires an attack_log")

    doc_get = DocGenerator()
    doc_get.generate(arguments.attack_log, arguments.outfile)


def create_parser():
    """ Creates the parser for the command line arguments"""
    lparser = argparse.ArgumentParser("Manage attack documentation")
    subparsers = lparser.add_subparsers(help="sub-commands")
    parser_create = subparsers.add_parser("create", help="Create a new human readable document")
    parser_create.set_defaults(func=create)
    parser_create.add_argument("--attack_log", default=None, help="The attack log the document is based on")
    parser_create.add_argument("--outfile", default="tools/human_readable_documentation/source/contents.rst", help="The default output file")

    return lparser


if __name__ == "__main__":
    parser = create_parser()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    try:
        str(args.func(args))
    except CmdlineArgumentException as ex:
        parser.print_help()
        print(f"\nCommandline error: {ex}")
