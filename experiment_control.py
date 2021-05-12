#!/usr/bin/env python3
""" The main tool to run experiments """

import argparse

from app.experimentcontrol import Experiment


# TODO: Add verbose settings: -v to -vvv
# TODO: Name experiments. Name will be written to the log

def explain(args):  # pylint: disable=unused-argument
    """ Explain the tool"""

    print("Please specify a command to execute. For a list see <help>")


def run(args):
    """ Run experiments

    @param args: arguments from the argparse parser
    """
    Experiment(args.configfile, args.verbose)


def create_parser():
    """ Creates the parser for the command line arguments"""
    parser = argparse.ArgumentParser("Controls an experiment on the configured systems")
    subparsers = parser.add_subparsers(help="sub-commands")

    parser.set_defaults(func=explain)
    parser.add_argument('--verbose', '-v', action='count', default=0)

    # Sub parser for machine creation
    parser_run = subparsers.add_parser("run", help="run experiments")
    parser_run.set_defaults(func=run)
    parser_run.add_argument("--configfile", default="experiment.yaml", help="Config file to create from")

    return parser


if __name__ == "__main__":
    arguments = create_parser().parse_args()
    arguments.func(arguments)
