#!/usr/bin/env python3

""" Configuration loader for PurpleDome """

from typing import Optional
import yaml
from app.config_verifier import MainConfig

from app.exceptions import ConfigurationError


# So the config being read is distributed into several files and they will have different formats (yaml, CACAO)
# Currently it is a single file and YAML only.
# We want to be independent from file structure or number of config files

# TODO: Attack control also by config class. Used in experimentcontrol. Will change with scripts !


class MachineConfig():
    """ Sub config for a specific machine"""

    def __init__(self, machinedata):
        """ Init machine control config

        :param machinedata: dict containing machine data
        """
        if machinedata is None:
            raise ConfigurationError

        self.raw_config = machinedata

    def vmname(self) -> str:
        """ Returns the vmname """

        return self.raw_config.vm_name

    def get_nicknames(self) -> list[str]:
        """ Gets the nicknames """

        if self.raw_config.has_key("nicknames"):
            return self.raw_config.nicknames or []

        return []

    def vmcontroller(self) -> str:
        """ Returns the vm controller. lowercase """

        if not self.raw_config.has_key("vm_controller"):
            raise ConfigurationError

        return self.raw_config.vm_controller.vm_type.lower()

    def vm_ip(self) -> str:
        """ Return the configured ip/domain name (whatever is needed to reach the machine). Returns None if missing """

        if not self.raw_config.has_key("vm_controller"):
            return self.vmname()

        if not self.raw_config.vm_controller.has_key("ip"):
            return self.vmname()

        try:
            return self.raw_config.vm_controller.ip
        except KeyError:
            return self.vmname()

    def os(self) -> str:  # pylint: disable=invalid-name
        """ returns the os. lowercase """

        return self.raw_config.os.lower()

    def use_existing_machine(self) -> bool:
        """ Returns if we want to use the existing machine """

        return self.raw_config.get("use_existing_machine", False)

    def machinepath(self) -> str:
        """ Returns the machine path. If not configured it will fall back to the vm_name """

        if self.raw_config.has_key("machinepath"):
            return self.raw_config.machinepath

        return self.vmname()

    def get_playground(self) -> Optional[str]:
        """ Returns the machine specific playground where all the implants and tools will be installed """

        return self.raw_config.get("playground", None)

    def caldera_paw(self) -> Optional[str]:
        """ Returns the paw (caldera id) of the machine """

        return self.raw_config.get("paw", None)

    def caldera_group(self) -> Optional[str]:
        """ Returns the group (caldera group id) of the machine """

        return self.raw_config.get("group", None)

    def ssh_keyfile(self) -> Optional[str]:
        """ Returns the configured SSH keyfile """

        return self.raw_config.get("ssh_keyfile", None)

    def ssh_user(self) -> str:
        """ Returns configured ssh user or "vagrant" as default  """

        return self.raw_config.get("ssh_user", "vagrant")

    def ssh_password(self) -> Optional[str]:
        """ Returns configured ssh password or None as default  """

        return self.raw_config.get("ssh_password", None)

    def halt_needs_force(self) -> bool:
        """ Returns if halting the machine needs force False as default  """

        return self.raw_config.get("halt_needs_force", False)

    def vagrantfilepath(self) -> str:
        """ Vagrant specific config: The vagrant file path """

        if not self.raw_config.vm_controller.has_key("vagrantfilepath"):
            raise ConfigurationError("Vagrantfilepath missing")
        return self.raw_config.vm_controller.vagrantfilepath

    def sensors(self) -> list[str]:
        """ Return a list of sensors configured for this machine """
        if self.raw_config.has_key("sensors"):
            return self.raw_config.sensors or []
        return []

    def vulnerabilities(self) -> list[str]:
        """ Return a list of vulnerabilities configured for this machine """
        if self.raw_config.has_key("vulnerabilities"):
            return self.raw_config.vulnerabilities or []
        return []

    def is_active(self) -> bool:
        """ Returns if this machine is set to active. Default is true """

        return self.raw_config.get("active", True)


class ExperimentConfig():
    """ Configuration class for a whole experiments """

    def __init__(self, configfile: str):
        """ Init the config, process the file

        :param configfile: The configuration file to process
        """

        self.raw_config: MainConfig = None
        self._targets: list[MachineConfig] = []
        self._attackers: list[MachineConfig] = []
        self.load(configfile)

        # Test essential data that is a hard requirement. Should throw errors if anything is wrong
        self.loot_dir()

    def load(self, configfile: str):
        """ Loads the configuration file

        :param configfile: The configuration file to process
        """

        with open(configfile) as fh:
            data = yaml.safe_load(fh)

        if data is None:
            raise ConfigurationError("Config file is empty")

        self.raw_config = MainConfig(**data)

        # Process targets
        if self.raw_config.targets is None:
            raise ConfigurationError("Config file does not specify targets")

        for target in self.raw_config.targets:
            self._targets.append(MachineConfig(target))

        # Process attackers
        if self.raw_config.attackers is None:
            raise ConfigurationError("Config file does not specify attackers")
        for attacker in self.raw_config.attackers:
            self._attackers.append(MachineConfig(attacker))

    def targets(self) -> list[MachineConfig]:
        """ Return config for targets as MachineConfig objects """

        return self._targets

    def attackers(self) -> list[MachineConfig]:
        """ Return config for attackers as MachineConfig objects """

        return self._attackers

    def attacker(self, mid: int) -> MachineConfig:
        """ Return config for attacker as MachineConfig objects

        :param mid: id of the attacker, 0 is main attacker
        """

        return self.attackers()[mid]

    def caldera_apikey(self) -> str:
        """ Returns the caldera apikey """

        if self.raw_config is None:
            raise ConfigurationError("Config file is empty")

        return self.raw_config.caldera.apikey

    def loot_dir(self) -> str:
        """ Returns the loot dir """

        if self.raw_config is None:
            raise ConfigurationError("Config file is empty")

        try:
            res = self.raw_config.results.loot_dir
        except KeyError as error:
            raise ConfigurationError("results/loot_dir not properly set in configuration") from error
        return res

    def attack_conf(self, attack: str) -> dict:
        """ Get kali config for a specific kali attack

        :param attack: Name of the attack to look up config for
        """

        if self.raw_config is None:
            raise ConfigurationError("Config file is empty")

        try:
            res = self.raw_config.attack_conf[attack]
        except KeyError:
            res = {}
        if res is None:
            res = {}

        return res

    def get_caldera_obfuscator(self) -> str:
        """ Get the caldera configuration. In this case: The obfuscator. Will default to plain-text """

        if self.raw_config is None:
            raise ConfigurationError("Config file is empty")

        try:
            return self.raw_config.attacks.caldera_obfuscator
        except KeyError:
            return "plain-text"

    def get_caldera_jitter(self) -> str:
        """ Get the caldera configuration. In this case: Jitter. Will default to 4/8 """

        if self.raw_config is None:
            raise ConfigurationError("Config file is empty")

        try:
            return self.raw_config.attacks.caldera_jitter
        except KeyError:
            return "4/8"

    def get_plugin_based_attacks(self, for_os: str) -> list[str]:
        """ Get the configured kali attacks to run for a specific OS

        :param for_os: The os to query the registered attacks for
        """

        if self.raw_config is None:
            raise ConfigurationError("Config file is empty")

        if not self.raw_config.has_key("plugin_based_attacks"):
            return []
        if not self.raw_config.plugin_based_attacks.has_key(for_os):
            return []
        res = self.raw_config.plugin_based_attacks.get(for_os)
        if res is None:
            return []
        return res

    def get_caldera_attacks(self, for_os: str) -> list:
        """ Get the configured caldera attacks to run for a specific OS

        :param for_os: The os to query the registered attacks for
        """

        if self.raw_config is None:
            raise ConfigurationError("Config file is empty")

        if not self.raw_config.has_key("caldera_attacks"):
            return []
        if not self.raw_config.caldera_attacks.has_key(for_os):
            return []
        res = self.raw_config.caldera_attacks.get(for_os)
        if res is None:
            return []
        return res

    def get_nap_time(self) -> int:
        """ Returns the attackers nap time between attack steps """

        if self.raw_config is None:
            raise ConfigurationError("Config file is empty")

        try:
            return int(self.raw_config.attacks.nap_time)
        except KeyError:
            return 0

    def get_sensor_config(self, name: str) -> dict:
        """ Return the config for a specific sensor

        :param name: name of the sensor
        """

        if self.raw_config is None:
            raise ConfigurationError("Config file is empty")

        if self.raw_config.sensor_conf is None:  # Better for unit tests that way.
            return {}
        if name in self.raw_config.sensor_conf:
            return self.raw_config.sensor_conf[name]

        return {}
