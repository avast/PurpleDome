#!/usr/bin/env python3

""" A command line tool to control a caldera server """

import argparse

#from app.calderacontrol import CalderaControl
from app.calderacontrol_4 import CalderaControl
from pprint import pprint

from app.attack_log import AttackLog


class CmdlineArgumentException(Exception):
    pass

# https://caldera.readthedocs.io/en/latest/The-REST-API.html

# TODO: Check if attack is finished

# TODO: Get results of a specific attack

# Arpgparse handling
def agents(calcontrol, arguments):  # pylint: disable=unused-argument
    """ Agents in caldera control

    @param calcontrol: Connection to the caldera server
    @param arguments: Parser command line arguments
    """

    if arguments.list:
        for agent in calcontrol.list_agents().__dict__["agents"]:
            print(agent)



def list_facts(calcontrol, arguments):  # pylint: disable=unused-argument
    """ Call list fact stores ("sources") in caldera control

    @param calcontrol: Connection to the caldera server
    @param arguments: Parser command line arguments
    """

    printme = "No found"

    if arguments.name:
        printme = calcontrol.list_facts_for_name(arguments.name)
    else:
        printme = calcontrol.list_sources()

    print(f"Stored facts: {printme}")


def add_facts(calcontrol, arguments):  # pylint: disable=unused-argument
    """ Generate new facts in caldera

    @param calcontrol: Connection to the caldera server
    @param arguments: Parser command line arguments
    """
    name = "Test"
    data = {"foo": "bar"}

    print(f'Created fact: {calcontrol.add_sources(name, data)}')


def delete_agents(calcontrol, arguments):  # pylint: disable=unused-argument
    """ Call list agents in caldera control

    @param calcontrol: Connection to the caldera server
    @param arguments: Parser command line arguments
    """
    print(calcontrol.list_paws_of_running_agents())

    if arguments.paw:
        print(calcontrol.kill_agent(paw=arguments.paw))
        print(calcontrol.delete_agent(paw=arguments.paw))

    else:
        print(calcontrol.kill_all_agents())
        print(calcontrol.delete_all_agents())


def list_abilities(calcontrol, arguments):
    """ Call list abilities in caldera control

    @param calcontrol: Connection to the caldera server
    @param arguments: Parser command line arguments
    """

    abilities = calcontrol.list_abilities().__dict__["abilities"]

    if arguments.list:
        abi_ids = [aid.ability_id for aid in abilities]
        print(abi_ids)

    for abi in abilities:
        for executor in abi.executors:
            for parser in executor.parsers:
                pprint(parser.relationships)

    #for aid in abilities:
    #    for ability in calcontrol.get_ability(aid):
    #        calcontrol.pretty_print_ability(ability)


def obfuscators(calcontrol, arguments):
    """ Manage obfuscators caldera control

    @param calcontrol: Connection to the caldera server
    @param arguments: Parser command line arguments
    """

    if arguments.list:
        obfs = calcontrol.list_obfuscators().__dict__["obfuscators"]
        # ob_ids = [aid.ability_id for aid in obfuscators]
        # print(ob_ids)

        for ob in obfs:
            print(ob)


def adversaries(calcontrol, arguments):
    """ Manage adversaries caldera control

    @param calcontrol: Connection to the caldera server
    @param arguments: Parser command line arguments
    """

    if arguments.list:
        advs = calcontrol.list_adversaries().__dict__["adversaries"]
        # ob_ids = [aid.ability_id for aid in obfuscators]
        # print(ob_ids)

        for ob in advs:
            print(ob)
    if arguments.add:
        if arguments.ability_id is None:
            raise CmdlineArgumentException("Creating an adversary requires an ability id")
        if arguments.name is None:
            raise CmdlineArgumentException("Creating an adversary requires an adversary name")
        res = calcontrol.add_adversary(arguments.name, arguments.ability_id)
    if arguments.delete:
        if arguments.adversary_id is None:
            raise CmdlineArgumentException("Deleting an adversary requires an adversary id")
        res = calcontrol.delete_adversary(arguments.adversary_id)


def sources(calcontrol, arguments):
    """ Manage sources caldera control

    @param calcontrol: Connection to the caldera server
    @param arguments: Parser command line arguments
    """

    if arguments.list:
        srcs = calcontrol.list_sources().__dict__["sources"]
        # ob_ids = [aid.ability_id for aid in obfuscators]
        # print(ob_ids)

        for ob in srcs:
            print(ob)


def operations(calcontrol, arguments):
    """ Manage operations caldera control

    @param calcontrol: Connection to the caldera server
    @param arguments: Parser command line arguments
    """

    if arguments.list:
        ops = calcontrol.list_operations().__dict__["operations"]
        # ob_ids = [aid.ability_id for aid in obfuscators]
        # print(ob_ids)

        for ob in ops:
            print(ob)

    if arguments.add:
        if arguments.adversary_id is None:
            raise CmdlineArgumentException("Adding an operation requires an adversary id")
        ops = calcontrol.add_operations(arguments.adversary_id)


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
    main_parser.add_argument('--verbose', '-v', action='count', default=0)

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
    parser_abilities.add_argument("--list", default=False, action="store_true",
                                  help="List all abilities")

    parser_agents = subparsers.add_parser("agents", help="agents")
    parser_agents.set_defaults(func=agents)
    parser_agents.add_argument("--list", default=False, action="store_true", help="List all agents")

    parser_delete_agents = subparsers.add_parser("delete_agents", help="agents")
    parser_delete_agents.add_argument("--paw", default=None, help="PAW to delete. if not set it will delete all agents")
    parser_delete_agents.set_defaults(func=delete_agents)

    parser_facts = subparsers.add_parser("facts", help="facts")
    parser_facts.set_defaults(func=list_facts)
    parser_facts.add_argument("--name", default=None, help="Name of a fact source to focus on")

    parser_facts = subparsers.add_parser("add_facts", help="facts")
    parser_facts.set_defaults(func=add_facts)

    # Sub parser for obfuscators
    parser_obfuscators = subparsers.add_parser("obfuscators", help="obfuscators")
    parser_obfuscators.set_defaults(func=obfuscators)
    parser_obfuscators.add_argument("--list", default=False, action="store_true",
                                  help="List all obfuscators")

    # Sub parser for adversaries
    parser_adversaries = subparsers.add_parser("adversaries", help="adversaries")
    parser_adversaries.set_defaults(func=adversaries)
    parser_adversaries.add_argument("--list", default=False, action="store_true",
                                    help="List all adversaries")
    parser_adversaries.add_argument("--add", default=False, action="store_true",
                                    help="Add a new adversary")
    parser_adversaries.add_argument("--ability_id", "--abid", default=None, help="Ability ID")
    parser_adversaries.add_argument("--ability_name", default=None, help="Adversary name")
    parser_adversaries.add_argument("--delete", default=False, action="store_true",
                                    help="Delete adversary")
    parser_adversaries.add_argument("--adversary_id", "--advid", default=None, help="Adversary ID")

    # Sub parser for operations
    parser_operations = subparsers.add_parser("operations", help="operations")
    parser_operations.set_defaults(func=operations)
    parser_operations.add_argument("--list", default=False, action="store_true",
                                    help="List all operations")
    parser_operations.add_argument("--add", default=False, action="store_true",
                                    help="Add a new operations")
    parser_operations.add_argument("--adversary_id", "--advid", default=None, help="Adversary ID")

    # Sub parser for sources
    parser_sources = subparsers.add_parser("sources", help="sources")
    parser_sources.set_defaults(func=sources)
    parser_sources.add_argument("--list", default=False, action="store_true",
                                    help="List all sources")

    # For all parsers
    main_parser.add_argument("--caldera_url", help="caldera url, including port", default="http://localhost:8888/")
    main_parser.add_argument("--apikey", help="caldera api key", default="ADMIN123")

    return main_parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    print(args.caldera_url)

    attack_logger = AttackLog(args.verbose)
    caldera_control = CalderaControl(args.caldera_url, attack_logger, config=None, apikey=args.apikey)
    print("Caldera Control ready")
    try:
        str(args.func(caldera_control, args))
    except CmdlineArgumentException as ex:
        parser.print_help()
        print(f"\nCommandline error: {ex}")
