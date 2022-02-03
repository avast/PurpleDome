#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
""" A command line tool to control a caldera server """

import argparse
from pprint import pprint
import argcomplete

# from app.calderacontrol import CalderaControl
# from app.calderacontrol import CalderaControl
from app.calderaapi_4 import CalderaAPI


from app.attack_log import AttackLog


class CmdlineArgumentException(Exception):
    """ An error in the user supplied command line """

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
        print(calcontrol.list_agents())
        print([i["paw"] for i in calcontrol.list_agents()])
    if arguments.delete:
        print(calcontrol.delete_agent(arguments.paw))
    if arguments.kill:
        print(calcontrol.kill_agent(arguments.paw))


def facts(calcontrol, arguments):
    """ Deal with fact stores ("sources") in caldera control

    @param calcontrol: Connection to the caldera server
    @param arguments: Parser command line arguments
    """

    if arguments.list:
        if arguments.name is None:
            raise CmdlineArgumentException("Listing facts by name requires a name")

        print_me = calcontrol.list_facts_for_name(arguments.name)
        print(f"Stored facts: {print_me}")


def abilities(calcontrol, arguments):
    """ Call list abilities in caldera control

    @param calcontrol: Connection to the caldera server
    @param arguments: Parser command line arguments
    """

    if arguments.list:
        ability_list = calcontrol.list_abilities()
        abi_ids = [aid.ability_id for aid in ability_list]
        print(abi_ids)

        for abi in ability_list:
            for executor in abi.executors:
                for a_parser in executor.parsers:
                    pprint(a_parser.relationships)


def obfuscators(calcontrol, arguments):
    """ Manage obfuscators caldera control

    @param calcontrol: Connection to the caldera server
    @param arguments: Parser command line arguments
    """

    if arguments.list:
        obfs = calcontrol.list_obfuscators()
        # ob_ids = [aid.ability_id for aid in obfuscators]
        # print(ob_ids)

        for obfuscator in obfs:
            print(obfuscator)


def objectives(calcontrol, arguments):
    """ Manage objectives caldera control

    @param calcontrol: Connection to the caldera server
    @param arguments: Parser command line arguments
    """

    if arguments.list:
        for objective in calcontrol.list_objectives():
            print(objective)


def adversaries(calcontrol, arguments):
    """ Manage adversaries caldera control

    @param calcontrol: Connection to the caldera server
    @param arguments: Parser command line arguments
    """

    if arguments.list:
        for adversary in calcontrol.list_adversaries():
            print(adversary)
    if arguments.add:
        if arguments.ability_id is None:
            raise CmdlineArgumentException("Creating an adversary requires an ability id")
        if arguments.name is None:
            raise CmdlineArgumentException("Creating an adversary requires an adversary name")
        calcontrol.add_adversary(arguments.name, arguments.ability_id)
    if arguments.delete:
        if arguments.adversary_id is None:
            raise CmdlineArgumentException("Deleting an adversary requires an adversary id")
        calcontrol.delete_adversary(arguments.adversary_id)


def sources(calcontrol, arguments):
    """ Manage sources caldera control

    @param calcontrol: Connection to the caldera server
    @param arguments: Parser command line arguments
    """

    if arguments.list:
        for a_source in calcontrol.list_sources():
            print(a_source)


def planners(calcontrol, arguments):
    """ Manage planners caldera control

    @param calcontrol: Connection to the caldera server
    @param arguments: Parser command line arguments
    """

    if arguments.list:
        for a_planner in calcontrol.list_planners():
            print(a_planner)


def operations(calcontrol, arguments):
    """ Manage operations caldera control

    @param calcontrol: Connection to the caldera server
    @param arguments: Parser command line arguments
    """

    if arguments.list:
        for an_operation in calcontrol.list_operations():
            print(an_operation)

    if arguments.add:
        if arguments.adversary_id is None:
            raise CmdlineArgumentException("Adding an operation requires an adversary id")
        if arguments.name is None:
            raise CmdlineArgumentException("Adding an operation requires a name for it")

        ops = calcontrol.add_operation(name=arguments.name,
                                       adversary_id=arguments.adversary_id,
                                       source_id=arguments.source_id,
                                       planner_id=arguments.planner_id,
                                       group=arguments.group,
                                       state=arguments.state,
                                       obfuscator=arguments.obfuscator,
                                       jitter=arguments.jitter)
        print(ops)

    if arguments.delete:
        if arguments.id is None:
            raise CmdlineArgumentException("Deleting an operation requires its id")
        ops = calcontrol.delete_operation(arguments.id)
        print(ops)

    if arguments.view_report:
        if arguments.id is None:
            raise CmdlineArgumentException("Viewing an operation report requires an operation id")
        report = calcontrol.view_operation_report(arguments.id)
        print(report)


def attack(calcontrol, arguments):
    """ Starting an attack

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

    main_parser = argparse.ArgumentParser("Controls a Caldera server. Use this to test your Caldera setup or the Caldera API.")
    main_parser.add_argument('--verbose', '-v', action='count', default=0)

    subparsers = main_parser.add_subparsers(help="sub-commands")

    # Sub parser for attacks
    parser_attack = subparsers.add_parser("attack", help="Attack system")
    parser_attack.set_defaults(func=attack)
    parser_attack.add_argument("--paw", default="kickme", help="Paw to attack and get specific results for")
    parser_attack.add_argument("--group", default="red", help="Target group to attack")
    parser_attack.add_argument("--ability_id", default="bd527b63-9f9e-46e0-9816-b8434d2b8989",
                               help="The ability to use for the attack")

    # Sub parser to list abilities
    parser_abilities = subparsers.add_parser("abilities", help="Control Caldera abilities ( aka exploits)")
    # parser_abilities.add_argument("--abilityid", default=None, help="Id of the ability to list")
    parser_abilities.set_defaults(func=abilities)
    # parser_abilities.add_argument("--ability_ids", default=[], nargs="+",
    #                               help="The abilities to look up. One or more ids")
    parser_abilities.add_argument("--list", default=False, action="store_true",
                                  help="List all abilities")

    parser_agents = subparsers.add_parser("agents", help="Control Caldera agents ( aka implants)")
    parser_agents.set_defaults(func=agents)
    parser_agents.add_argument("--list", default=False, action="store_true", help="List all agents")
    parser_agents.add_argument("--delete", default=False, action="store_true", help="Delete agent from database")
    parser_agents.add_argument("--kill", default=False, action="store_true", help="Kill agent on target system")
    parser_agents.add_argument("--paw", default=None, help="PAW to delete or kill. If this is not set it will delete all agents")

    parser_facts = subparsers.add_parser("facts", help="facts")
    parser_facts.set_defaults(func=facts)
    parser_facts.add_argument("--list", default=False, action="store_true", help="List facts")
    parser_facts.add_argument("--name", default=None, help="Name of a fact source to focus on")

    # parser_facts = subparsers.add_parser("add_facts", help="facts")
    # parser_facts.set_defaults(func=add_facts)

    # Sub parser for obfuscators
    parser_obfuscators = subparsers.add_parser("obfuscators", help="Obfuscator interface. Hide the attack")
    parser_obfuscators.set_defaults(func=obfuscators)
    parser_obfuscators.add_argument("--list", default=False, action="store_true",
                                    help="List all obfuscators")

    # Sub parser for objectives
    parser_objectives = subparsers.add_parser("objectives", help="Objectives interface")
    parser_objectives.set_defaults(func=objectives)
    parser_objectives.add_argument("--list", default=False, action="store_true",
                                   help="List all objectives")

    # Sub parser for adversaries
    parser_adversaries = subparsers.add_parser("adversaries", help="Adversary interface. Adversaries are attacker archetypes")
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
    parser_operations = subparsers.add_parser("operations", help="Attack operation interface")
    parser_operations.set_defaults(func=operations)
    parser_operations.add_argument("--list", default=False, action="store_true",
                                   help="List all operations")
    parser_operations.add_argument("--add", default=False, action="store_true",
                                   help="Add a new operations")
    parser_operations.add_argument("--delete", default=False, action="store_true",
                                   help="Delete an operation")
    parser_operations.add_argument("--view_report", default=False, action="store_true",
                                   help="View the report of a finished operation")
    parser_operations.add_argument("--name", default=None, help="Name of the operation")
    parser_operations.add_argument("--adversary_id", "--advid", default=None, help="Adversary ID")
    parser_operations.add_argument("--source_id", "--sourceid", default="basic", help="Source ID")
    parser_operations.add_argument("--planner_id", "--planid", default="atomic", help="Planner ID")
    parser_operations.add_argument("--group", default="", help="Caldera group to run the operation on (we are targeting groups, not PAWs)")
    parser_operations.add_argument("--state", default="running", help="State to start the operation in")
    parser_operations.add_argument("--obfuscator", default="plain-text", help="Obfuscator to use for this attack")
    parser_operations.add_argument("--jitter", default="4/8", help="Jitter to use")
    parser_operations.add_argument("--id", default=None, help="ID of operation to delete")

    # Sub parser for sources
    parser_sources = subparsers.add_parser("sources", help="Data source management")
    parser_sources.set_defaults(func=sources)
    parser_sources.add_argument("--list", default=False, action="store_true",
                                help="List all sources")

    # Sub parser for planners
    parser_sources = subparsers.add_parser("planners", help="Planner management. They define the pattern of attack steps")
    parser_sources.set_defaults(func=planners)
    parser_sources.add_argument("--list", default=False, action="store_true",
                                help="List all planners")

    # For all parsers
    main_parser.add_argument("--caldera_url", help="The Caldera url, including port and protocol (http://)", default="http://localhost:8888/")
    main_parser.add_argument("--apikey", help="Caldera api key", default="ADMIN123")

    return main_parser


if __name__ == "__main__":
    parser = create_parser()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    print(args.caldera_url)

    attack_logger = AttackLog(args.verbose)
    caldera_control = CalderaAPI(args.caldera_url, attack_logger, config=None, apikey=args.apikey)
    print("Caldera Control ready")
    try:
        str(args.func(caldera_control, args))
    except CmdlineArgumentException as ex:
        parser.print_help()
        print(f"\nCommandline error: {ex}")
