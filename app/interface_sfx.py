#!/usr/bin/env python3

""" Helper functions to improve the command line experiments """

# Colors to be used when printing text to the terminal
# print(f"{CommandlineColors.WARNING}Warning {CommandlineColors.ENDC}")
# https://dev.to/ifenna__/adding-colors-to-bash-scripts-48g4


class CommandlineColors:
    """ A collection of command line colors """

    # pylint: disable=too-few-public-methods

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    BACKGROUND_BLUE ='\033[104m'
    WARNING = '\033[93m'
    ATTACK = '\033[93m'       # An attack is running
    MACHINE_CREATED = '\033[92m'
    MACHINE_STOPPED = '\033[96m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
