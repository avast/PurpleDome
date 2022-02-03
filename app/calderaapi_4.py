#!/usr/bin/env python3

""" Remote control a caldera 4 server. Starting compatible to the old control 2.8 calderacontrol. Maybe it will stop being compatible if refactoring is an option """

import json

from pprint import pformat
from typing import Optional, Union
import requests
import simplejson
from pydantic.dataclasses import dataclass
from pydantic import conlist  # pylint: disable=no-name-in-module

# from app.exceptions import CalderaError
# from app.interface_sfx import CommandlineColors


# TODO: Ability deserves an own class.
# TODO: Support all Caldera agents: "Sandcat (GoLang)","Elasticat (Blue Python/ Elasticsearch)","Manx (Reverse Shell TCP)","Ragdoll (Python/HTML)"

@dataclass
class Variation:
    description: str
    command: str


@dataclass
class ParserConfig:
    source: str
    edge: str
    target: str
    custom_parser_vals: dict  # undocumented ! Needs improvement ! TODO


@dataclass
class Parser:
    module: str
    relationships: list[ParserConfig]  # undocumented ! Needs improvement ! TODO
    parserconfigs: Optional[list[ParserConfig]] = None


@dataclass
class Requirement:
    module: str
    relationship_match: list[dict]


@dataclass
class AdditionalInfo:
    additionalProp1: Optional[str] = None  # pylint: disable=invalid-name
    additionalProp2: Optional[str] = None  # pylint: disable=invalid-name
    additionalProp3: Optional[str] = None  # pylint: disable=invalid-name


@dataclass
class Executor:
    build_target: Optional[str]  # Why can this be None ?
    language: Optional[str]  # Why can this be None ?
    payloads: list[str]
    variations: list[Variation]
    additional_info: Optional[AdditionalInfo]
    parsers: list[Parser]
    cleanup: list[str]
    name: str
    timeout: int
    code: Optional[str]  # Why can this be None ?
    uploads: list[str]
    platform: str
    command: Optional[str]

    def get(self, akey, default=None):
        """ Get a specific element out of the internal data representation, behaves like the well know 'get' """
        if akey in self.__dict__:
            return self.__dict__[akey]

        return default


@dataclass
class Ability:
    """ An ability is an exploit, a TTP, an attack step ...more or less... """
    description: str
    plugin: str
    technique_name: str
    requirements: list[Requirement]
    additional_info: AdditionalInfo
    singleton: bool
    buckets: list[str]
    access: dict
    executors: list[Executor]
    name: str
    technique_id: str
    tactic: str
    repeatable: str
    ability_id: str
    privilege: Optional[str] = None

    def get(self, akey, default=None):
        """ Get a specific element out of the internal data representation, behaves like the well know 'get' """
        if akey in self.__dict__:
            return self.__dict__[akey]

        return default


@dataclass
class AbilityList:
    """ A list of exploits """
    abilities: conlist(Ability, min_items=1)

    def get_data(self):
        return self.abilities


@dataclass
class Obfuscator:
    """ An obfuscator hides the attack by encryption/encoding """
    description: str
    name: str
    module: Optional[str] = None  # Documentation error !!!


@dataclass
class ObfuscatorList:
    """ A list of obfuscators """
    obfuscators: conlist(Obfuscator, min_items=1)

    def get_data(self):
        return self.obfuscators


@dataclass
class Adversary:
    """ An adversary is a defined attacker """
    has_repeatable_abilities: bool
    adversary_id: str
    description: str
    name: str
    atomic_ordering: list[str]
    objective: str
    tags: list[str]
    plugin: Optional[str] = None

    def get(self, akey, default=None):
        """ Get a specific element out of the internal data representation, behaves like the well know 'get' """
        if akey in self.__dict__:
            return self.__dict__[akey]

        return default


@dataclass
class AdversaryList:
    """ A list of adversary """
    adversaries: conlist(Adversary, min_items=1)

    def get_data(self):
        return self.adversaries


@dataclass
class Fact:
    unique: str
    name: str
    score: int
    limit_count: int
    relationships: list[str]
    source: str
    trait: str
    links: list[str]
    created: str
    origin_type: Optional[str] = None
    value: Optional[str] = None
    technique_id: Optional[str] = None
    collected_by: Optional[str] = None

    def get(self, akey, default=None):
        """ Get a specific element out of the internal data representation, behaves like the well know 'get' """
        if akey in self.__dict__:
            return self.__dict__[akey]

        return default


@dataclass
class Relationship:
    target: Fact
    unique: str
    score: int
    edge: str
    origin: str
    source: Fact


@dataclass
class Visibility:
    score: int
    adjustments: list[int]


@dataclass
class Link:
    pin: int
    ability: Ability
    paw: str
    status: int
    finish: str
    decide: str
    output: str
    visibility: Visibility
    pid: str
    host: str
    executor: Executor
    unique: str
    score: int
    used: list[Fact]
    facts: list[Fact]
    agent_reported_time: str
    id: str  # pylint: disable=invalid-name
    collect: str
    command: str
    cleanup: int
    relationships: list[Relationship]
    jitter: int
    deadman: bool


@dataclass
class Agent:
    """ A representation of an agent on the target (agent = implant) """
    paw: str
    location: str
    platform: str
    last_seen: str   # Error in document
    host_ip_addrs: list[str]
    group: str
    architecture: str
    pid: int
    server: str
    trusted: bool
    username: str
    host: str
    ppid: int
    created: str
    links: list[Link]
    sleep_max: int
    exe_name: str
    display_name: str
    sleep_min: int
    contact: str
    deadman_enabled: bool
    proxy_receivers: AdditionalInfo
    origin_link_id: str
    executors: list[str]
    watchdog: int
    proxy_chain: list[list[str]]
    available_contacts: list[str]
    upstream_dest: str
    pending_contact: str
    privilege: Optional[str] = None  # Error, not documented

    def get(self, akey, default=None):
        """ Get a specific element out of the internal data representation, behaves like the well know 'get' """
        if akey in self.__dict__:
            return self.__dict__[akey]

        return default


@dataclass
class AgentList:
    """ A list of agents """
    agents: list[Agent]

    def get_data(self):
        return self.agents


@dataclass
class Rule:
    match: str
    trait: str
    action: Optional[str] = None


@dataclass
class Adjustment:
    offset: int
    trait: str
    value: str
    ability_id: str


@dataclass
class Source:
    name: str
    plugin: str
    facts: list[Fact]
    rules: list[Rule]
    relationships: list[Relationship]
    id: str  # pylint: disable=invalid-name
    adjustments: Optional[list[Adjustment]] = None

    def get(self, akey, default=None):
        """ Get a specific element out of the internal data representation, behaves like the well know 'get' """
        if akey in self.__dict__:
            return self.__dict__[akey]

        return default


@dataclass
class SourceList:
    sources: list[Source]

    def get_data(self):
        return self.sources


@dataclass
class Planner:
    """ A logic defining the order in which attack steps are executed """
    name: str
    plugin: str
    id: str  # pylint: disable=invalid-name
    stopping_conditions: list[Fact]
    params: dict
    description: str
    allow_repeatable_abilities: bool
    module: Optional[str] = None
    ignore_enforcement_module: Optional[list[str]] = None
    ignore_enforcement_modules: Optional[list[str]] = None   # Maybe error in Caldera 4 ?


@dataclass
class PlannerList:
    planners: list[Planner]

    def get_data(self):
        return self.planners


@dataclass
class Goal:
    target: str
    count: int
    achieved: bool
    operator: str
    value: str


@dataclass
class Objective:
    percentage: int
    name: str
    goals: list[Goal]
    description: str
    id: str  # pylint: disable=invalid-name

    def get(self, akey, default=None):
        """ Get a specific element out of the internal data representation, behaves like the well know 'get' """
        if akey in self.__dict__:
            return self.__dict__[akey]

        return default


@dataclass
class Operation:
    """ An attack operation collecting all the relevant items (obfuscator, adversary, planner) """
    obfuscator: str
    state: str
    jitter: str
    autonomous: int
    name: str
    source: Source
    adversary: Adversary
    objective: Union[Objective, str]   # Maybe Error in caldera 4: Creating a Operation returns a objective ID, not an objective object
    host_group: list[Agent]
    start: str
    group: str
    use_learning_parsers: bool
    planner: Planner
    visibility: int
    id: str  # pylint: disable=invalid-name
    auto_close: bool
    chain: Optional[list] = None

    def get(self, akey, default=None):
        """ Get a specific element out of the internal data representation, behaves like the well know 'get' """
        if akey in self.__dict__:
            return self.__dict__[akey]

        return default


@dataclass
class OperationList:
    operations: conlist(Operation)

    def get_data(self):
        return self.operations


@dataclass
class ObjectiveList:
    objectives: conlist(Objective)

    def get_data(self):
        return self.objectives


class CalderaAPI():
    """ Remote control Caldera through REST api """

    def __init__(self, server: str, attack_logger, config=None, apikey=None):
        """

        @param server: Caldera server url/ip
        @param attack_logger: The attack logger to use
        @param config: The configuration
        """
        self.url = server if server.endswith("/") else server + "/"
        self.attack_logger = attack_logger

        self.config = config

        if self.config:
            self.apikey = self.config.caldera_apikey()
        else:
            self.apikey = apikey

    def __contact_server__(self, payload, rest_path: str = "api/v2/abilities", method: str = "get"):
        """

        @param payload: payload as dict to send to the server
        @param rest_path: specific path for this rest api
        @param method: http method to use
        """
        url = self.url + rest_path
        header = {"KEY": "ADMIN123",
                  "accept": "application/json",
                  "Content-Type": "application/json"}
        if method.lower() == "post":
            j = json.dumps(payload)
            request = requests.post(url, headers=header, data=j)
        elif method.lower() == "put":
            request = requests.put(url, headers=header, data=json.dumps(payload))
        elif method.lower() == "get":
            request = requests.get(url, headers=header, data=json.dumps(payload))
        elif method.lower() == "head":
            request = requests.head(url, headers=header, data=json.dumps(payload))
        elif method.lower() == "delete":
            request = requests.delete(url, headers=header, data=json.dumps(payload))
        elif method.lower() == "patch":
            request = requests.patch(url, headers=header, data=json.dumps(payload))
        else:
            raise ValueError
        try:
            if request.status_code == 200:
                res = request.json()
            # Comment: Sometimes we get a 204: succcess, but not content in response
            elif request.status_code == 204:
                res = {"result": "ok",
                       "http_status_code": 204}
            else:
                print(f"Status code: {request.status_code} {request.json()}")
                res = request.json()

        except simplejson.errors.JSONDecodeError as exception:  # type: ignore
            print("!!! Error !!!!")
            print(payload)
            print(request.text)
            print("!!! Error !!!!")
            raise exception

        return res

    def list_abilities(self):
        """ Return all ablilities """

        payload = None
        data = {"abilities": self.__contact_server__(payload, method="get", rest_path="api/v2/abilities")}
        abilities = AbilityList(**data)
        return abilities.get_data()

    def list_obfuscators(self):
        """ Return all obfuscators """

        payload = None
        data = {"obfuscators": self.__contact_server__(payload, method="get", rest_path="api/v2/obfuscators")}
        obfuscators = ObfuscatorList(**data)
        return obfuscators.get_data()

    def list_adversaries(self):
        """ Return all adversaries """

        payload = None
        data = {"adversaries": self.__contact_server__(payload, method="get", rest_path="api/v2/adversaries")}
        adversaries = AdversaryList(**data)
        return adversaries.get_data()

    def list_sources(self):
        """ Return all sources """

        payload = None
        data = {"sources": self.__contact_server__(payload, method="get", rest_path="api/v2/sources")}
        sources = SourceList(**data)
        return sources.get_data()

    def list_planners(self):
        """ Return all planners """

        payload = None
        data = {"planners": self.__contact_server__(payload, method="get", rest_path="api/v2/planners")}
        planners = PlannerList(**data)
        return planners.get_data()

    def list_operations(self):
        """ Return all operations """

        payload = None
        data = {"operations": self.__contact_server__(payload, method="get", rest_path="api/v2/operations")}
        operations = OperationList(**data)
        return operations.get_data()

    def set_operation_state(self, operation_id: str, state: str = "running"):
        """ Executes an operation on a server

        @param operation_id: The operation to modify
        @param state: The state to set this operation into
        """

        # TODO: Change state of an operation: curl -X POST -H "KEY:ADMIN123" http://localhost:8888/api/rest -d '{"index":"operation", "op_id":123, "state":"finished"}'
        # curl -X POST -H "KEY:ADMIN123" http://localhost:8888/api/rest -d '{"index":"operation", "op_id":123, "state":"finished"}'

        if state not in ["running", "finished", "paused", "run_one_link", "cleanup"]:
            raise ValueError

        payload = {"state": state}
        return self.__contact_server__(payload, method="patch", rest_path=f"api/v2/operations/{operation_id}")

    def list_agents(self):
        """ Return all agents """

        payload = None
        data = {"agents": self.__contact_server__(payload, method="get", rest_path="api/v2/agents")}
        agents = AgentList(**data)
        return agents.get_data()

    def list_objectives(self):
        """ Return all objectivs """

        payload = None
        data = {"objectives": self.__contact_server__(payload, method="get", rest_path="api/v2/objectives")}
        objectives = ObjectiveList(**data)
        return objectives.get_data()

    def add_adversary(self, name: str, ability: str, description: str = "created automatically"):
        """ Adds a new adversary

        :param name: Name of the adversary
        :param ability: Ability ID to add
        :param description: Human readable description
        :return:
        """
        payload = {
            #  "adversary_id": "string",
            "atomic_ordering": [
                ability
            ],
            "name": name,
            #  "plugin": "string",
            "objective": '495a9828-cab1-44dd-a0ca-66e58177d8cc',  # default objective
            #  "tags": [
            #     "string"
            #  ],
            "description": description
        }
        data = {"agents": self.__contact_server__(payload, method="post", rest_path="api/v2/adversaries")}
        # agents = AgentList(**data)
        return data

    def delete_adversary(self, adversary_id: str):
        """ Deletes an adversary

        :param adversary_id: The id of this adversary
        :return:
        """
        payload = None
        data = {"agents": self.__contact_server__(payload, method="delete", rest_path=f"api/v2/adversaries/{adversary_id}")}
        return data

    def delete_agent(self, agent_paw: str):
        """ Deletes an agent

        :param agent_paw: the paw to delete
        :return:
        """
        payload = None
        data = {"agents": self.__contact_server__(payload, method="delete", rest_path=f"api/v2/agents/{agent_paw}")}
        return data

    def kill_agent(self, agent_paw: str):
        """ Kills an agent on the target

        :param agent_paw: The paw identifying this agent
        :return:
        """
        payload = {"watchdog": 1,
                   "sleep_min": 3,
                   "sleep_max": 3}
        data = self.__contact_server__(payload, method="patch", rest_path=f"api/v2/agents/{agent_paw}")
        return data

    def add_operation(self, **kwargs):
        """ Adds a new operation

        :param kwargs:
        :return:
        """

        # name, adversary_id, source_id = "basic", planner_id = "atomic", group = "", state: str = "running", obfuscator: str = "plain-text", jitter: str = '4/8'

        name: str = kwargs.get("name")
        adversary_id: str = kwargs.get("adversary_id")
        source_id: str = kwargs.get("source_id", "basic")
        planner_id: str = kwargs.get("planner_id", "atomic")
        group: str = kwargs.get("group", "")
        state: str = kwargs.get("state", "running")
        obfuscator: str = kwargs.get("obfuscator", "plain-text")
        jitter: str = kwargs.get("jitter", "4/8")

        payload = {"name": name,
                   "group": group,
                   "adversary": {"adversary_id": adversary_id},
                   "auto_close": False,
                   "state": state,
                   "autonomous": 1,
                   "planner": {"id": planner_id},
                   "source": {"id": source_id},
                   "use_learning_parsers": True,
                   "obfuscator": obfuscator,
                   "jitter": jitter,
                   "visibility": "51"}
        data = {"operations": [self.__contact_server__(payload, method="post", rest_path="api/v2/operations")]}
        operations = OperationList(**data)
        return operations

    def delete_operation(self, operation_id):
        """ Deletes an operation

        :param operation_id: The Id of the operation to delete
        :return:
        """

        payload = {}

        data = self.__contact_server__(payload, method="delete", rest_path=f"api/v2/operations/{operation_id}")

        return data

    def view_operation_report(self, operation_id):
        """ Views the report of a finished operation

        :param operation_id: The id of this operation
        :return:
        """

        payload = {
            "enable_agent_output": True
        }

        data = self.__contact_server__(payload, method="post", rest_path=f"api/v2/operations/{operation_id}/report")

        return data

    def get_ability(self, abid: str):
        """" Return an ability by id

        @param abid: Ability id
        """

        res = []

        print(f"Number of abilities: {len(self.list_abilities())}")

        with open("debug_removeme.txt", "wt") as fh:
            fh.write(pformat(self.list_abilities()))

        for ability in self.list_abilities()["abilities"]:
            if ability.get("ability_id", None) == abid or ability.get("auto_generated_guid", None) == abid:
                res.append(ability)
        return res

    def pretty_print_ability(self, abi):
        """ Pretty pritns an ability

        @param abi: A ability dict
        """

        print("""
        TTP: {technique_id}
        Technique name: {technique_name}
        Tactic: {tactic}
        Name: {name}
        ID: {ability_id}
        Description: {description}

        """.format(**abi))
