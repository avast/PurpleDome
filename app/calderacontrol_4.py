#!/usr/bin/env python3

""" Remote control a caldera 4 server. Starting compatible to the old control 2.8 calderacontrol. Maybe it will stop being compatible if refactoring is an option """

import json
import os
import time

from pprint import pprint, pformat
from typing import Optional
import requests
import simplejson
from typing import Optional
from pydantic.dataclasses import dataclass
from pydantic import conlist, constr  # pylint: disable=no-name-in-module

from app.exceptions import CalderaError
from app.interface_sfx import CommandlineColors


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
    additionalProp1: Optional[str] = None
    additionalProp2: Optional[str] = None
    additionalProp3: Optional[str] = None

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

@dataclass
class Ability:
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


@dataclass
class AbilityList:
    abilities: conlist(Ability, min_items=1)


@dataclass
class Obfuscator:
    description: str
    name: str
    module: Optional[str] = None  # Documentation error !!!

@dataclass
class ObfuscatorList:
    obfuscators: conlist(Obfuscator, min_items=1)

@dataclass
class Adversary:
    has_repeatable_abilities: bool
    adversary_id: str
    description: str
    name: str
    atomic_ordering: list[str]
    objective: str
    plugin: str
    tags: list[str]

@dataclass
class AdversaryList:
    adversaries: conlist(Adversary, min_items=1)


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
    id: str
    collect: str
    command: str
    cleanup: int
    relationships: list[Relationship]
    jitter: int
    deadman: bool



@dataclass
class Agent:
    paw: str
    location: str
    platform: str
    last_seen: str   #  Error in document
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


@dataclass
class AgentList:
    agents: conlist(Agent, min_items=1)


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
    id: str
    adjustments: Optional[list[Adjustment]] = None


@dataclass
class SourceList:
    sources: list[Source]


@dataclass
class Planner:
    module: str
    name: str
    plugin: str
    id: str
    stopping_conditions: list[Fact]
    params: dict
    ignore_enforcement_module: list[str]
    description: str
    allow_repeatable_abilities: bool


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
    id: str


@dataclass
class Operation:
    obfuscator: str
    state: str
    jitter: str
    autonomous: int
    name: str
    source: Source
    adversary: Adversary
    objective: Objective
    host_group: list[Agent]
    start: str
    group: str
    use_learning_parsers: bool
    planner: Planner
    visibility: int
    id: str
    auto_close: bool


@dataclass
class OperationList:
    operations: conlist(Operation)

class CalderaControl():
    """ Remote control Caldera through REST api """

    def __init__(self, server: str, attack_logger, config=None, apikey=None):
        """

        @param server: Caldera server url/ip
        @param attack_logger: The attack logger to use
        @param config: The configuration
        """
        # print(server)
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
                  "accept": "application/json"}
        if method.lower() == "post":
            request = requests.post(url, headers=header, data=json.dumps(payload))
        elif method.lower() == "put":
            request = requests.put(url, headers=header, data=json.dumps(payload))
        elif method.lower() == "get":
            request = requests.get(url, headers=header, data=json.dumps(payload))
        elif method.lower() == "head":
            request = requests.head(url, headers=header, data=json.dumps(payload))
        elif method.lower() == "delete":
            request = requests.delete(url, headers=header, data=json.dumps(payload))
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
                print(f"Status code: {request.status_code}")
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
        return abilities

    def list_obfuscators(self):
        """ Return all obfuscators """

        payload = None
        data = {"obfuscators": self.__contact_server__(payload, method="get", rest_path="api/v2/obfuscators")}
        obfuscators = ObfuscatorList(**data)
        return obfuscators

    def list_adversaries(self):
        """ Return all adversaries """

        payload = None
        data = {"adversaries": self.__contact_server__(payload, method="get", rest_path="api/v2/adversaries")}
        print(data)
        adversaries = AdversaryList(**data)
        return adversaries

    def list_sources(self):
        """ Return all sources """

        payload = None
        data = {"sources": self.__contact_server__(payload, method="get", rest_path="api/v2/sources")}
        print(data)
        sources = SourceList(**data)
        return sources

    def list_operations(self):
        """ Return all operations """

        payload = None
        data = {"operations": self.__contact_server__(payload, method="get", rest_path="api/v2/operations")}
        print(data)
        operations = OperationList(**data)
        return operations

    def list_agents(self):
        """ Return all agents """

        payload = None
        data = {"agents": self.__contact_server__(payload, method="get", rest_path="api/v2/agents")}
        print(data)
        agents = AgentList(**data)
        return agents

    # TODO: list_sources
    # TODO: list_sources_for_name
    # TODO: list_facts_for_name
    # TODO: list_paws_of_running_agents
    # TODO: list_objectives
    # TODO: get_operation
    # TODO: get_adversary
    # TODO: get_source
    # TODO: get_ability
    # TODO: does_ability_support_platform
    # TODO: get_operation_by_id
    # TODO: view_operation_report
    # TODO: view_operation_output
    # TODO: add_sources
    # TODO: add_operation
    # TODO: execute_operation
    # TODO: delete_operation
    # TODO: delete_agent
    # TODO: kill_agent

    # TODO is_operation_finished
    # TODO: attack


    def add_adversary(self, name: str, ability: str, description: str = "created automatically"):
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
        print(data)
        # agents = AgentList(**data)
        return data

    def delete_adversary(self, adversary_id: str):
        payload = None
        data = {"agents": self.__contact_server__(payload, method="delete", rest_path=f"api/v2/adversaries/{adversary_id}")}
        print(data)
        # agents = AgentList(**data)
        return data

    def add_operations(self, adversary_id):
        payload = {
            "adversary": {"adversary_id": adversary_id},
            "planner": {"id": "foo"},
            "source": {"id": "foo"}
        }
        data = {"agents": self.__contact_server__(payload, method="post", rest_path="api/v2/operations")}
        print(data)
        # agents = AgentList(**data)
        return data

    def get_ability(self, abid: str):
        """" Return an ability by id

        @param abid: Ability id
        """

        res = []

        print(f"Number of abilities: {len(self.list_abilities())}")

        with open("debug_removeme.txt", "wt") as fh:
            fh.write(pformat(self.list_abilities()))

        for ability in self.list_abilities():
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