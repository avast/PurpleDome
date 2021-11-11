#!/usr/bin/env python3

""" Pydantic verifier for config structure """

from pydantic.dataclasses import dataclass
from pydantic import conlist
from typing import Optional
from enum import Enum


class OSEnum(str, Enum):
    linux = "linux"
    windows = "windows"


class VMControllerTypeEnum(str, Enum):
    vagrant = "vagrant"
    running_vm = "running_vm"


@dataclass
class CalderaConfig:
    apikey: str

    def has_key(self, keyname):
        if keyname in self.__dict__.keys():
            return True
        return False


@dataclass
class VMController:
    vm_type: VMControllerTypeEnum
    vagrantfilepath: str
    ip: Optional[str] = ""

    def has_key(self, keyname):
        if keyname in self.__dict__.keys():
            return True
        return False

    # def __dict__(self):
    #     return {"vm_type": self.vm_type,
    #             "vagrantfilepath": self.vagrantfilepath,
    #            "ip": self.ip}


@dataclass
class Attacker:
    name: str
    vm_controller: VMController
    vm_name: str
    nicknames: Optional[list[str]]
    machinepath: str
    os: OSEnum
    use_existing_machine: bool = False
    playground: Optional[str] = None

    def has_key(self, keyname):
        if keyname in self.__dict__.keys():
            return True
        return False

    def get(self, keyname, default=None):
        if self.has_key(keyname):
            return self.__dict__[keyname]
        return default


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
    nicknames: Optional[list[str]]
    active: bool = True
    use_existing_machine: bool = False
    playground: Optional[str] = None
    halt_needs_force: Optional[str] = None
    ssh_user: Optional[str] = None
    ssh_password: Optional[str] = None
    ssh_keyfile: Optional[str] = None
    vulnerabilities: list[str] = None

    def has_key(self, keyname):
        if keyname in self.__dict__.keys():
            return True
        return False

    def get(self, keyname, default=None):
        if self.has_key(keyname):
            return self.__dict__[keyname]
        return default


@dataclass
class AttackConfig:
    caldera_obfuscator: str = "plain-text"
    caldera_jitter: str = "4/8"
    nap_time: int = 5

    def has_key(self, keyname):
        if keyname in self.__dict__.keys():
            return True
        return False


@dataclass
class AttackList:
    linux: Optional[list[str]]
    windows: Optional[list[str]]

    def has_key(self, keyname):
        if keyname in self.__dict__.keys():
            return True
        return False

    def get(self, keyname, default=None):
        if self.has_key(keyname):
            return self.__dict__[keyname]
        return default


@dataclass
class Results:
    loot_dir: str

    def has_key(self, keyname):
        if keyname in self.__dict__.keys():
            return True
        return False


@dataclass
class MainConfig:
    caldera: CalderaConfig
    attackers: conlist(Attacker, min_items=1)
    targets: conlist(Target, min_items=1)
    attacks: AttackConfig
    caldera_attacks: AttackList
    plugin_based_attacks: AttackList
    results: Results

    # Free form configuration for plugins
    attack_conf: Optional[dict]
    sensor_conf: Optional[dict]

    def has_key(self, keyname):
        if keyname in self.__dict__.keys():
            return True
        return False


# TODO: Check for name duplication
