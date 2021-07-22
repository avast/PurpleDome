#!/usr/bin/env python3

""" Configuration loader for PurpleDome """

import yaml

from app.exceptions import ConfigurationError


# So the config being read is distributed into several files and they will have different formats (yaml, CACAO)
# Currently it is a single file and YAML only.
# We want to be independent from file structure or number of config files

# TODO: Attack control also by config class. Used in experimentcontrol. Will change with scripts !


class MachineConfig():
    """ Sub config for a specific machine"""

    def __init__(self, machinedata):
        """ Init machine control config

        @param machinedata: dict containing machine data
        """
        if machinedata is None:
            raise ConfigurationError

        self.raw_config = machinedata
        self.verify()

    def verify(self):
        """ Verify essential data is present """
        try:
            self.vmname()
            operating_system = self.os()
            vmcontroller = self.vmcontroller()
        except KeyError as exception:
            raise ConfigurationError from exception

        if operating_system not in ["linux", "windows"]:
            raise ConfigurationError

        # TODO: Verify with plugins
        if vmcontroller not in ["vagrant", "running_vm"]:
            raise ConfigurationError

    def vmname(self):
        """ Returns the vmname """

        return self.raw_config["vm_name"]

    def get_nicknames(self):
        """ Gets the nicknames """

        if "nicknames" in self.raw_config:
            return self.raw_config["nicknames"] or []

        return []

    def vmcontroller(self):
        """ Returns the vm controller. lowercase """

        return self.raw_config["vm_controller"]["type"].lower()

    def vm_ip(self):
        """ Return the configured ip/domain name (whatever is needed to reach the machine). Returns None if missing """
        try:
            return self.raw_config["vm_controller"]["ip"]
        except KeyError:
            return self.vmname()

    def os(self):  # pylint: disable=invalid-name
        """ returns the os. lowercase """

        return self.raw_config["os"].lower()

    def use_existing_machine(self):
        """ Returns if we want to use the existing machine """

        return self.raw_config.get("use_existing_machine", False)

    def machinepath(self):
        """ Returns the machine path. If not configured it will fall back to the vm_name """

        return self.raw_config.get("machinepath", self.vmname())

    def get_playground(self):
        """ Returns the machine specific playground where all the implants and tools will be installed """

        return self.raw_config.get("playground", None)

    def caldera_paw(self):
        """ Returns the paw (caldera id) of the machine """

        return self.raw_config.get("paw", None)

    def caldera_group(self):
        """ Returns the group (caldera group id) of the machine """

        return self.raw_config.get("group", None)

    def ssh_keyfile(self):
        """ Returns the configured SSH keyfile """

        return self.raw_config.get("ssh_keyfile", None)

    def ssh_user(self):
        """ Returns configured ssh user or "vagrant" as default  """

        return self.raw_config.get("ssh_user", "vagrant")

    def ssh_password(self):
        """ Returns configured ssh password or None as default  """

        return self.raw_config.get("ssh_password", None)

    def halt_needs_force(self):
        """ Returns if halting the machine needs force False as default  """

        return self.raw_config.get("halt_needs_force", False)

    def vagrantfilepath(self):
        """ Vagrant specific config: The vagrant file path """

        if "vagrantfilepath" not in self.raw_config["vm_controller"]:
            raise ConfigurationError("Vagrantfilepath missing")
        return self.raw_config["vm_controller"]["vagrantfilepath"]

    def sensors(self):
        """ Return a list of sensors configured for this machine """
        if "sensors" in self.raw_config:
            return self.raw_config["sensors"] or []
        return []

    def vulnerabilities(self):
        """ Return a list of vulnerabilities configured for this machine """
        if "vulnerabilities" in self.raw_config:
            return self.raw_config["vulnerabilities"] or []
        return []

    def is_active(self):
        """ Returns if this machine is set to active. Default is true """

        return self.raw_config.get("active", True)


class ExperimentConfig():
    """ Configuration class for a whole experiments """

    def __init__(self, configfile):
        """ Init the config, process the file

        @param configfile: The configuration file to process
        """

        self.raw_config = None
        self._targets = []
        self._attackers = []
        self.load(configfile)

        # Test essential data that is a hard requirement. Should throw errors if anything is wrong
        self.loot_dir()

    def load(self, configfile):
        """ Loads the configuration file

        @param configfile: The configuration file to process
        """

        with open(configfile) as fh:
            self.raw_config = yaml.safe_load(fh)

        # Process targets
        for target in self.raw_config["targets"]:
            self._targets.append(MachineConfig(self.raw_config["targets"][target]))

        # Process attackers
        for attacker in self.raw_config["attackers"]:
            self._attackers.append(MachineConfig(self.raw_config["attackers"][attacker]))

    def targets(self) -> [MachineConfig]:
        """ Return config for targets as MachineConfig objects """

        return self._targets

    def attackers(self) -> [MachineConfig]:
        """ Return config for attackers as MachineConfig objects """

        return self._attackers

    def attacker(self, mid) -> MachineConfig:
        """ Return config for attacker as MachineConfig objects

        @param mid: id of the attacker, 0 is main attacker
        """

        return self.attackers()[mid]

    def caldera_apikey(self):
        """ Returns the caldera apikey """

        return self.raw_config["caldera"]["apikey"]

    def loot_dir(self):
        """ Returns the loot dir """

        if "results" not in self.raw_config or self.raw_config["results"] is None:
            raise ConfigurationError("results missing in configuration")
        try:
            res = self.raw_config["results"]["loot_dir"]
        except KeyError as error:
            raise ConfigurationError("results/loot_dir not properly set in configuration") from error
        return res

    def attack_conf(self, attack):
        """ Get kali config for a specific kali attack

        @param attack: Name of the attack to look up config for
        """

        try:
            res = self.raw_config["attack_conf"][attack]
        except KeyError:
            res = {}
        if res is None:
            res = {}

        return res

    def get_caldera_obfuscator(self):
        """ Get the caldera configuration. In this case: The obfuscator. Will default to plain-text """

        try:
            res = self.raw_config["caldera_conf"]["obfuscator"]
        except KeyError:
            return "plain-text"
        return res

    def get_caldera_jitter(self):
        """ Get the caldera configuration. In this case: Jitter. Will default to 4/8 """

        try:
            res = self.raw_config["caldera_conf"]["jitter"]
        except KeyError:
            return "4/8"
        return res

    def get_plugin_based_attacks(self, for_os):
        """ Get the configured kali attacks to run for a specific OS

        @param for_os: The os to query the registered attacks for
        """

        if "plugin_based_attacks" not in self.raw_config:
            return []
        if for_os not in self.raw_config["plugin_based_attacks"]:
            return []
        res = self.raw_config["plugin_based_attacks"][for_os]
        if res is None:
            return []
        return res

    def get_caldera_attacks(self, for_os):
        """ Get the configured caldera attacks to run for a specific OS

        @param for_os: The os to query the registered attacks for
        """

        if "caldera_attacks" not in self.raw_config:
            return []
        if for_os not in self.raw_config["caldera_attacks"]:
            return []
        res = self.raw_config["caldera_attacks"][for_os]
        if res is None:
            return []
        return res

    def get_nap_time(self):
        """ Returns the attackers nap time between attack steps """

        try:
            return self.raw_config["attacks"]["nap_time"]
        except KeyError:
            return 0

    def get_sensor_config(self, name):
        """ Return the config for a specific sensor

        @param name: name of the sensor
        """
        if "sensors" not in self.raw_config:
            return {}
        if self.raw_config["sensors"] is None:  # Better for unit tests that way.
            return {}
        if name in self.raw_config["sensors"]:
            return self.raw_config["sensors"][name]

        return {}
