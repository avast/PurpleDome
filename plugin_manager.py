#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
""" Managing plugins """

import argparse
import sys
import argcomplete

from app.pluginmanager import PluginManager
from app.attack_log import AttackLog


class CmdlineArgumentException(Exception):
    """ An error in the user supplied command line """


def list_plugins(arguments):
    """ List plugins """

    attack_logger = AttackLog(arguments.verbose)
    plugin_manager = PluginManager(attack_logger)
    plugin_manager.print_list()
    return 0


def check_plugins(arguments):
    """ Check plugins for validity """

    attack_logger = AttackLog(arguments.verbose)
    plugin_manager = PluginManager(attack_logger)
    res = plugin_manager.print_check()
    if len(res) != 0:
        print("*************************************")
        print("Some issues in plugins were found: ")
        print("\n".join(res))
    return len(res)


def get_default_config(arguments):
    """ print default config of a specific plugin """

    attack_logger = AttackLog(arguments.verbose)
    plugin_manager = PluginManager(attack_logger)
    if arguments.subclass_name is None:
        raise CmdlineArgumentException("Getting configuration requires a subclass_name")
    if arguments.plugin_name is None:
        raise CmdlineArgumentException("Getting configuration requires a plugin_name")
    plugin_manager.print_default_config(arguments.subclass_name, arguments.plugin_name)


def create_parser():
    """ Creates the parser for the command line arguments"""

    main_parser = argparse.ArgumentParser("Manage plugins")
    main_parser.add_argument('--verbose', '-v', action='count', default=0, help="Verbosity level")
    subparsers = main_parser.add_subparsers(help="sub-commands")

    # Sub parser for plugin list
    parser_list = subparsers.add_parser("list", help="list plugins")
    parser_list.set_defaults(func=list_plugins)
    # parser_list.add_argument("--configfile", default="experiment.yaml", help="Config file to create from")

    # Sub parser for plugin check
    parser_list = subparsers.add_parser("check", help="Check plugin implementation")
    parser_list.set_defaults(func=check_plugins)

    parser_default_config = subparsers.add_parser("raw_config", help="Print raw default config of the given plugin")
    parser_default_config.set_defaults(func=get_default_config)
    parser_default_config.add_argument("subclass_name", help="Name of the subclass")
    parser_default_config.add_argument("plugin_name", help="Name of the plugin")

    # TODO: Get default config
    return main_parser


if __name__ == "__main__":

    parser = create_parser()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    try:
        exit_val = args.func(args)
        sys.exit(exit_val)
    except CmdlineArgumentException as ex:
        parser.print_help()
        print(f"\nCommandline error: {ex}")
