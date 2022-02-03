#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
""" Demo program to set up and control the machines """

import argparse
import argcomplete

import yaml

from app.calderacontrol import CalderaControl
from app.machinecontrol import Machine
from app.attack_log import AttackLog


def create_machines(arguments):
    """ Create machines based on config

    @param arguments: The arguments from argparse
    """

    with open(arguments.configfile) as fh:
        config = yaml.safe_load(fh)

    attack_logger = AttackLog(arguments.verbose)
    target_ = Machine(config["targets"]["target1"], attack_logger)
    attacker_1 = Machine(config["attackers"]["attacker"], attack_logger)

    print("Got them")

    # TODO Automatically create all machines defined in config file

    # attacker_1.destroy()
    print("destroyed")
    attacker_1.create(reboot=False)
    print("Attacker up")
    attacker_1.up()
    print(attacker_1.install_caldera_server())
    attacker_1.start_caldera_server()
    print("Attacker done")

    target_.destroy()
    target_.set_caldera_server(attacker_1.get_ip())
    target_.install_caldera_service()
    target_.create()
    print("Target up")
    target_.up()
    target_.start_caldera_client()
    print("Target done")

    print("Caldera server running at: http://{}:8888/".format(attacker_1.get_ip()))
    # target_.install_caldera_client(attacker_1.getip(), "target1elf")


def download_caldera_client(arguments):
    """ Downloads the caldera client

    @param arguments: The arguments from argparse
    """

    attack_logger = AttackLog(arguments.verbose)
    caldera_control = CalderaControl(args.ip, attack_logger, None)
    caldera_control.fetch_client(platform=arguments.platform,
                                 file=arguments.file,
                                 target_dir=arguments.target_dir,
                                 extension=".go")


def create_parser():
    """ Creates the parser for the command line arguments"""

    main_parser = argparse.ArgumentParser("Controls machinery to test VM interaction")
    main_parser.add_argument('--verbose', '-v', action='count', default=0, help="Verbosity level")
    subparsers = main_parser.add_subparsers(help="sub-commands")

    # Sub parser for machine creation
    parser_create = subparsers.add_parser("create", help="Create VM machines")
    parser_create.set_defaults(func=create_machines)
    parser_create.add_argument("--configfile", default="experiment.yaml", help="Config file to create VMs from")

    parser_download_caldera_client = subparsers.add_parser("fetch_client", help="Download the caldera client")
    parser_download_caldera_client.set_defaults(func=download_caldera_client)
    parser_download_caldera_client.add_argument("--ip", default="192.168.178.189", help="IP of Caldera to connect to")
    parser_download_caldera_client.add_argument("--platform", default="windows", help="platform to download the client for")
    parser_download_caldera_client.add_argument("--file", default="sandcat.go", help="The agent to download")
    parser_download_caldera_client.add_argument("--target_dir", default=".", help="The target dir to download the file to")

    return main_parser


if __name__ == "__main__":

    parser = create_parser()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    args.func(args)
