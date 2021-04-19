#!/usr/bin/env python3
""" Demo program to set up and control the machines """

import argparse

import yaml

from app.calderacontrol import CalderaControl
from app.machinecontrol import Machine


def create_machines(arguments):
    """

    @param arguments: The arguments from argparse
    """
    # TODO: Add argparse and make it flexible

    with open(arguments.configfile) as fh:
        config = yaml.safe_load(fh)

    target_ = Machine(config["targets"]["target1"])
    attacker_1 = Machine(config["attackers"]["attacker"])

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
    target_.set_caldera_server(attacker_1.getip())
    target_.install_caldera_service()
    target_.create()
    print("Target up")
    target_.up()
    target_.start_caldera_client()
    print("Target done")

    print("Caldera server running at: http://{}:8888/".format(attacker_1.getip()))
    # target_.install_caldera_client(attacker_1.getip(), "target1elf")


def download_caldera_client(arguments):
    """ Downloads the caldera client

    @param arguments: The arguments from argparse
    """

    caldera_control = CalderaControl(args.ip, None)
    caldera_control.fetch_client(platform=arguments.platform,
                                 file=arguments.file,
                                 target_dir=arguments.target_dir,
                                 extension=".go")


def create_parser():
    """ Creates the parser for the command line arguments"""

    main_parser = argparse.ArgumentParser("Controls a Caldera server to attack other systems")
    subparsers = main_parser.add_subparsers(help="sub-commands")

    # Sub parser for machine creation
    parser_create = subparsers.add_parser("create", help="create systems")
    parser_create.set_defaults(func=create_machines)
    parser_create.add_argument("--configfile", default="experiment.yaml", help="Config file to create from")

    parser_download_caldera_client = subparsers.add_parser("fetch_client", help="download the caldera client")
    parser_download_caldera_client.set_defaults(func=download_caldera_client)
    parser_download_caldera_client.add_argument("--ip", default="192.168.178.189", help="Ip of Caldera to connect to")
    parser_download_caldera_client.add_argument("--platform", default="windows", help="platform to download the client for")
    parser_download_caldera_client.add_argument("--file", default="sandcat.go", help="The agent to download")
    parser_download_caldera_client.add_argument("--target_dir", default=".", help="The target dir to download the file to")

    return main_parser


if __name__ == "__main__":

    parser = create_parser()

    args = parser.parse_args()

    args.func(args)
