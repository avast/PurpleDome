#!/usr/bin/env python3
""" Managing plugins """

import argparse
from app.pluginmanager import PluginManager


def list_plugins(arguments):
    p = PluginManager()
    p.print_list()


def create_parser():
    """ Creates the parser for the command line arguments"""

    main_parser = argparse.ArgumentParser("Manage plugins")
    subparsers = main_parser.add_subparsers(help="sub-commands")

    # Sub parser for machine creation
    parser_create = subparsers.add_parser("list", help="list plugins")
    parser_create.set_defaults(func=list_plugins)
    # parser_create.add_argument("--configfile", default="experiment.yaml", help="Config file to create from")

    # TODO: Get default config
    return main_parser


if __name__ == "__main__":

    parser = create_parser()

    args = parser.parse_args()

    args.func(args)
