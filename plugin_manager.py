#!/usr/bin/env python3
""" Managing plugins """

import argparse
import sys

from app.pluginmanager import PluginManager
from app.attack_log import AttackLog


def list_plugins(arguments):
    """ List plugins """

    attack_logger = AttackLog(arguments.verbose)
    p = PluginManager(attack_logger)
    p.print_list()
    return 0


def check_plugins(arguments):
    """ Check plugins for validity """

    attack_logger = AttackLog(arguments.verbose)
    p = PluginManager(attack_logger)
    res = p.print_check()
    if len(res):
        print("*************************************")
        print("Some issues in plugins were found: ")
        print("\n".join(res))
    return len(res)


def get_default_config(arguments):
    """ print default config of a specific plugin """

    attack_logger = AttackLog(arguments.verbose)
    p = PluginManager(attack_logger)
    p.print_default_config(arguments.subclass_name, arguments.plugin_name)


def create_parser():
    """ Creates the parser for the command line arguments"""

    main_parser = argparse.ArgumentParser("Manage plugins")
    main_parser.add_argument('--verbose', '-v', action='count', default=0)
    subparsers = main_parser.add_subparsers(help="sub-commands")

    # Sub parser for plugin list
    parser_list = subparsers.add_parser("list", help="list plugins")
    parser_list.set_defaults(func=list_plugins)
    # parser_list.add_argument("--configfile", default="experiment.yaml", help="Config file to create from")

    # Sub parser for plugin check
    parser_list = subparsers.add_parser("check", help="check plugin implementation")
    parser_list.set_defaults(func=check_plugins)

    parser_default_config = subparsers.add_parser("raw_config", help="print raw default config of the given plugin")
    parser_default_config.set_defaults(func=get_default_config)
    parser_default_config.add_argument("subclass_name", help="name of the subclass")
    parser_default_config.add_argument("plugin_name", help="name of the plugin")

    # TODO: Get default config
    return main_parser


if __name__ == "__main__":

    parser = create_parser()

    args = parser.parse_args()

    exval = args.func(args)
    sys.exit(exval)
