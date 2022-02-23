#!/usr/bin/env python3

""" Pydantic verifier for config structure """

from enum import Enum
from typing import Optional
from pydantic.dataclasses import dataclass
from pydantic import conlist  # pylint: disable=no-name-in-module

# TODO: Move from has_key to iterators and "is in"


class OSEnum(str, Enum):
    """ List of all supported OS-es """
    LINUX = "linux"
    WINDOWS = "windows"


class VMControllerTypeEnum(str, Enum):
    """ List of all supported controlled plugins. This is only done for VM controller plugins !
        I do not expect many new ones. And typos in config can be a waste of time. Let's see if I am right.  """
    VAGRANT = "vagrant"
    RUNNING_VM = "running_vm"


@dataclass
class CalderaConfig:
    """ Configuration for the Caldera server """
    apikey: str

    def has_key(self, keyname):
        """ Checks if a key exists
        Required for compatibility with DotMap which is used in Unit tests
        """
        if keyname in self.__dict__.keys():
            return True
        return False


@dataclass
class VMController:
    """ Configuration for the VM controller """
    vm_type: VMControllerTypeEnum
    vagrantfilepath: str
    ip: Optional[str] = ""  # pylint: disable=invalid-name

    def has_key(self, keyname):
        """ Checks if a key exists
            Required for compatibility with DotMap which is used in Unit tests
        """
        if keyname in self.__dict__.keys():
            return True
        return False

    # def __dict__(self):
    #     return {"vm_type": self.vm_type,
    #             "vagrantfilepath": self.vagrantfilepath,
    #            "ip": self.ip}


@dataclass
class Attacker:
    """ Configuration for a attacker VM """
    name: str
    vm_controller: VMController
    vm_name: str
    nicknames: Optional[list[str]]
    machinepath: str
    os: OSEnum  # pylint: disable=invalid-name
    use_existing_machine: bool = False
    playground: Optional[str] = None

    def has_key(self, keyname):
        """ Checks if a key exists
            Required for compatibility with DotMap which is used in Unit tests
        """
        if keyname in self.__dict__.keys():
            return True
        return False

    def get(self, keyname, default=None):
        """ Returns the value of a specific key
            Required for compatibility with DotMap which is used in Unit tests
        """
        if self.has_key(keyname):
            return self.__dict__[keyname]
        return default


@dataclass
class Target:
    """ Configuration for a target VM """
    name: str
    vm_controller: VMController
    vm_name: str
    os: OSEnum  # pylint: disable=invalid-name
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
    vulnerabilities: Optional[list[str]] = None

    def has_key(self, keyname):
        """ Checks if a key exists
            Required for compatibility with DotMap which is used in Unit tests
        """
        if keyname in self.__dict__.keys():
            return True
        return False

    def get(self, keyname, default=None):
        """ Returns the value of a specific key
            Required for compatibility with DotMap which is used in Unit tests
        """
        if self.has_key(keyname):
            return self.__dict__[keyname]
        return default


@dataclass
class AttackConfig:
    """ Generic configuration for attacks """
    caldera_obfuscator: str = "plain-text"
    caldera_jitter: str = "4/8"
    nap_time: int = 5

    def has_key(self, keyname):
        """ Checks if a key exists
            Required for compatibility with DotMap which is used in Unit tests
        """
        if keyname in self.__dict__.keys():
            return True
        return False


@dataclass
class AttackList:
    """ A list of attacks to run. Either plugin based or caldera based """
    linux: Optional[list[str]]
    windows: Optional[list[str]]

    def has_key(self, keyname):
        """ Checks if a key exists
            Required for compatibility with DotMap which is used in Unit tests
        """
        if keyname in self.__dict__.keys():
            return True
        return False

    def get(self, keyname, default=None):
        """ Returns the value of a specific key
            Required for compatibility with DotMap which is used in Unit tests
        """
        if self.has_key(keyname):
            return self.__dict__[keyname]
        return default


@dataclass
class Results:
    """ What to do with the results """
    loot_dir: str

    def has_key(self, keyname):
        """ Checks if a key exists
            Required for compatibility with DotMap which is used in Unit tests
        """
        if keyname in self.__dict__.keys():
            return True
        return False


@dataclass
class MainConfig:
    """ Central configuration for PurpleDome """
    caldera: CalderaConfig
    attackers: conlist(Attacker, min_items=1)  # type: ignore
    targets: conlist(Target, min_items=1)  # type: ignore
    attacks: AttackConfig
    caldera_attacks: AttackList
    plugin_based_attacks: AttackList
    results: Results

    # Free form configuration for plugins
    attack_conf: Optional[dict]
    sensor_conf: Optional[dict]

    def has_key(self, keyname):
        """ Checks if a key exists
            Required for compatibility with DotMap which is used in Unit tests
        """
        if keyname in self.__dict__.keys():
            return True
        return False


# TODO: Check for name duplication
