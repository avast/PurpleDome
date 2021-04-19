#!/usr/bin/env python3

""" A command line tool to control a caldera server """

import argparse

from app.calderacontrol import CalderaControl


# https://caldera.readthedocs.io/en/latest/The-REST-API.html


# Arpgparse handling
def list_agents(calcontrol, arguments):  # pylint: disable=unused-argument
    """ Call list agents in caldera control

    @param calcontrol: Connection to the caldera server
    @param arguments: Parser command line arguments
    """
    # TODO: calcontrol.list_agents(arguments)
    pass  # pylint: disable=unnecessary-pass


def list_abilities(calcontrol, arguments):
    """ Call list abilities in caldera control

    @param calcontrol: Connection to the caldera server
    @param arguments: Parser command line arguments
    """

    abilities = arguments.ability_ids

    if arguments.all:
        abilities = [aid["ability_id"] for aid in calcontrol.list_abilities()]

    for aid in abilities:
        for ability in calcontrol.get_ability(aid):
            calcontrol.pretty_print_ability(ability)


def attack(calcontrol, arguments):
    """ Calling attack

    @param calcontrol: Connection to the caldera server
    @param arguments: Parser command line arguments
    """
    print("Running attack")
    print(arguments.paw)
    print(arguments.group)
    print(arguments.ability_id)
    calcontrol.attack(paw=arguments.paw, group=arguments.group, ability_id=arguments.ability_id)


def create_parser():
    """ Creates the parser for the command line arguments"""

    main_parser = argparse.ArgumentParser("Controls a Caldera server to attack other systems")
    subparsers = main_parser.add_subparsers(help="sub-commands")

    # Sub parser for attacks
    parser_attack = subparsers.add_parser("attack", help="attack system")
    parser_attack.set_defaults(func=attack)
    parser_attack.add_argument("--paw", default="kickme", help="paw to attack and get specific results for")
    parser_attack.add_argument("--group", default="red", help="target group to attack")
    parser_attack.add_argument("--ability_id", default="bd527b63-9f9e-46e0-9816-b8434d2b8989",
                               help="The ability to use for the attack")

    # Sub parser to list abilities
    parser_abilities = subparsers.add_parser("abilities", help="abilities")
    # parser_abilities.add_argument("--abilityid", default=None, help="Id of the ability to list")
    parser_abilities.set_defaults(func=list_abilities)
    parser_abilities.add_argument("--ability_ids", default=[], nargs="+",
                                  help="The abilities to look up. One or more ids")
    parser_abilities.add_argument("--all", default=False, action="store_true",
                                  help="List all abilities")

    # TODO: Add sub parser to list agents
    parser_agents = subparsers.add_parser("agents", help="agents")
    parser_agents.set_defaults(func=list_agents)

    # For all parsers
    main_parser.add_argument("--caldera_url", help="caldera url, including port", default="http://192.168.178.97:8888/")
    main_parser.add_argument("--apikey", help="caldera api key", default="ADMIN123")

    return main_parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    print(args.caldera_url)

    caldera_control = CalderaControl(args.caldera_url, config=None, apikey=args.apikey)
    print("Caldera Control ready")

    str(args.func(caldera_control, args))
