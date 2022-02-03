#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
""" The main tool to run experiments """

import argparse
import argcomplete

from app.experimentcontrol import Experiment


# TODO: Name experiments. Name will be written to the log

def explain(args):  # pylint: disable=unused-argument
    """ Explain the tool"""

    print("Please specify a command to execute. For a list see <help>")


def run(args):
    """ Run experiments

    @param args: arguments from the argparse parser
    """

    if args.caldera_attack_file:
        with open(args.caldera_attack_file, "rt") as fh:
            for line in fh:
                line = line.strip()
                print(f"Running calder attack {line}")
                Experiment(args.configfile, args.verbose, [line])

    else:
        caldera_attack = None
        if args.caldera_attack:
            caldera_attack = [args.caldera_attack]
        Experiment(args.configfile, args.verbose, caldera_attack)


def create_parser():
    """ Creates the parser for the command line arguments"""
    lparser = argparse.ArgumentParser("Controls an experiment on the configured systems")
    subparsers = lparser.add_subparsers(help="sub-commands")

    lparser.set_defaults(func=explain)
    lparser.add_argument('--verbose', '-v', action='count', default=0, help="Verbosity level")

    # Sub parser for machine creation
    parser_run = subparsers.add_parser("run", help="run experiments")
    parser_run.set_defaults(func=run)
    parser_run.add_argument("--configfile", default="experiment.yaml", help="Config file to create the experiment from")
    parser_run.add_argument("--caldera_attack", default=None, help="The id of a specific caldera attack to run, will override experiment configuration for attacks")
    parser_run.add_argument("--caldera_attack_file", default=None, help="The file name containing a list of caldera attacks to run, will override experiment configuration for attacks")

    return lparser


if __name__ == "__main__":
    parser = create_parser()
    argcomplete.autocomplete(parser)
    arguments = parser.parse_args()
    arguments.func(arguments)
