#!/usr/bin/env python3

""" Pydantic verifier for config structure """

from pydantic.dataclasses import dataclass
from pydantic import conlist, BaseModel
from typing import Literal, Optional, TypedDict, Union
from enum import Enum


class OSEnum(str, Enum):
    linux = "linux"
    windows = "windows"


@dataclass
class CalderaConfig:
    apikey: str


@dataclass
class Attacker:
    name: str
    vm_controller: dict
    vm_name: str
    machinepath: str
    os: OSEnum
    use_existing_machine: bool = False


@dataclass
class VMController:
    type: str
    vagrantfilepath: str
    ip: Optional[str] = ""

@dataclass
class Target:
    name: str
    vm_controller: VMController
    vm_name: str
    os: OSEnum
    paw: str
    group: str
    machinepath: str
    sensors: Optional[list[str]]
    active: bool = True
    use_existing_machine: bool = False
    playground: Optional[str] = None
    halt_needs_force: Optional[str] = None
    ssh_user: Optional[str] = None
    ssh_password: Optional[str] = None
    ssh_keyfile: Optional[str] = None
    vulnerabilities: list[str] = None


@dataclass
class AttackConfig:
    nap_time: int
    caldera_obfuscator: str
    caldera_jitter: str


@dataclass
class AttackList:
    linux: Optional[list[str]]
    windows: Optional[list[str]]


@dataclass
class Results:
    loot_dir: str


@dataclass
class MainConfig():
    caldera: CalderaConfig
    attackers: conlist(Attacker, min_items=1)
    targets: conlist(Target, min_items=1)
    attacks: AttackConfig
    caldera_attacks: AttackList
    plugin_based_attacks: AttackList
    results: Results

    # Free form configuration for plugins
    attack_conf: dict
    sensor_conf: dict


# TODO: Check for name duplication