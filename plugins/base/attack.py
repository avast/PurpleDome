#!/usr/bin/env python3
""" Base class for Kali plugins """

from enum import Enum
import os
from typing import Optional, Any

from app.calderacontrol import CalderaControl
from app.exceptions import PluginError, ConfigurationError, RequirementError
from app.metasploit import MetasploitInstant
from plugins.base.machinery import MachineryPlugin
from plugins.base.plugin_base import BasePlugin
# from app.machinecontrol import Machine


class Requirement(Enum):
    """ Requirements for this plugin """
    METASPLOIT = 1
    CALDERA = 2


class AttackPlugin(BasePlugin):
    """ Class to execute a command on a kali system targeting another system """

    # Boilerplate
    # name: Optional[str] = None
    # description: Optional[str] = None
    ttp: Optional[str] = None  #: TTP of this attack. Or ??? if unknown
    references: list[str] = []  #: A list of urls or other references

    required_files: list[str] = []  # Better use the other required_files features
    required_files_attacker: list[str] = []  #: A list of files to automatically install to the attacker
    required_files_target: list[str] = []    #: A list of files to automatically copy to the targets

    requirements: Optional[list[Requirement]] = []  #: Requirements to run this plugin, Available are METASPLOIT and CALDERA at the moment

    def __init__(self) -> None:
        super().__init__()
        self.conf: dict = {}     # Plugin specific configuration
        # self.sysconf = {}  # System configuration. common for all plugins
        self.attacker_machine_plugin: Optional[MachineryPlugin] = None  # The machine plugin referencing the attacker. The Kali machine should be the perfect candidate
        self.target_machine_plugin: Optional[MachineryPlugin] = None  # The machine plugin referencing the target
        self.caldera: Optional[CalderaControl] = None  # The Caldera connection object
        self.targets: list[Any] = []

        self.metasploit_password: str = "password"
        self.metasploit_user: str = "user"
        self.metasploit: Optional[MetasploitInstant] = None

    def run(self, targets: list[str]) -> str:
        """ The attack is ran here. This method **must be implemented**

        :param targets: A list of targets, ip addresses will do
        :return: The result as a string
        """
        raise NotImplementedError

    def install(self) -> None:  # pylint: disable=no-self-use
        """ Install and setup requirements for the attack

        This step is *optional*

        """

        return None

    def needs_caldera(self) -> bool:
        """ Returns True if this plugin has Caldera in the requirements

        :meta private:

        :returns: True if this plugin requires Caldera
        """
        if self.requirements is not None:
            if Requirement.CALDERA in self.requirements:
                return True
        return False

    def needs_metasploit(self) -> bool:
        """ Returns True if this plugin has Metasploit in the requirements

        :meta private:
        :returns: True if this plugin requires Metasploit
        """
        if self.requirements is not None:
            if Requirement.METASPLOIT in self.requirements:
                return True
        return False

    def connect_metasploit(self) -> None:
        """ Inits metasploit

        :meta private:
        """

        if self.attack_logger is None:
            raise PluginError("Attack logger is required")

        if self.needs_metasploit():
            self.metasploit = MetasploitInstant(self.metasploit_password,
                                                attack_logger=self.attack_logger,
                                                attacker=self.attacker_machine_plugin,
                                                username=self.metasploit_user)
        # If metasploit requirements are not set, self.metasploit stay None and using metasploit from a plugin not having the requirements will trigger an exception

    def copy_to_attacker_and_defender(self) -> None:
        """ Copy attacker/defender specific files to the machines. Called by setup, do not call it yourself. template processing happens before

        :meta private:

        """

        if self.plugin_path is None:
            raise PluginError("Path for plugin not set")

        if self.attacker_machine_plugin is None:
            raise PluginError("Attacker machine not registered")

        for a_file in self.required_files_attacker:
            src = os.path.join(os.path.dirname(self.plugin_path), a_file)
            self.vprint(src, 3)
            self.attacker_machine_plugin.put(src, self.attacker_machine_plugin.get_playground())

        # TODO: add target(s)

    def teardown(self) -> None:
        """ Cleanup afterwards

        This is an *optional* method which is called after the attack. If you want to do some cleanup in your plugin, implement it.

        """
        pass  # pylint: disable=unnecessary-pass

    def attacker_run_cmd(self, command: str, disown: bool = False) -> str:
        """ Execute a command on the attacker

         :param command: Command to execute
         :param disown: Run in background
         """

        if self.attacker_machine_plugin is None:
            raise PluginError("machine to run command on is not registered")

        self.vprint(f"      Plugin running command {command}", 3)

        res = self.attacker_machine_plugin.remote_run(command, disown=disown)
        return res

    def targets_run_cmd(self, command: str, disown: bool = False) -> str:
        """ Execute a command on the target

         :param command: Command to execute
         :param disown: Run in background
         """

        if self.target_machine_plugin is None:
            raise PluginError("machine to run command on is not registered")

        self.vprint(f"      Plugin running command {command}", 3)

        res = self.target_machine_plugin.remote_run(command, disown=disown)
        return res

    def set_target_machines(self, machine: MachineryPlugin) -> None:
        """ Set the machine to target

        :param machine: Machine plugin to communicate with
        """

        self.target_machine_plugin = machine

    def set_attacker_machine(self, machine: MachineryPlugin) -> None:
        """ Set the machine plugin class to target

        :param machine: Machine to communicate with
        """

        self.attacker_machine_plugin = machine

    def set_caldera(self, caldera: CalderaControl) -> None:
        """ Set the caldera control to be used for caldera attacks

         @param caldera: The caldera object to connect through
         """

        if self.needs_caldera():
            self.caldera = caldera

    def caldera_attack(self, target: MachineryPlugin, ability_id: str, parameters: Optional[dict] = None, **kwargs) -> None:
        """ Attack a single target using caldera

        :param target: Target machine object
        :param ability_id: Ability or caldera ability to run
        :param parameters: parameters to pass to the ability
        """

        if not self.needs_caldera():
            raise RequirementError("Caldera not in requirements")

        if self.caldera is None:
            raise PluginError("Caldera not configured")

        self.caldera.attack(paw=target.get_paw(),
                            ability_id=ability_id,
                            group=target.get_group(),
                            target_platform=target.get_os(),
                            parameters=parameters,
                            **kwargs
                            )

    def get_attacker_playground(self) -> Optional[str]:
        """ Returns the attacker machine specific playground

         This is the folder on the machine where we run our tasks in

         :returns: playground on the attacker (path, str)
         """

        if self.attacker_machine_plugin is None:
            raise PluginError("Attacker machine not configured.")

        playground = self.attacker_machine_plugin.get_playground()

        return playground

    def __execute__(self, targets: list[Any]) -> str:
        """ Execute the plugin. This is called by the code

        :meta private:

        :param targets: A list of targets => machines (and it would be smarter to use MachineryPlugin instead of machine)
        """

        # TODO: Use MachineryPlugin instead of Machine

        if self.attack_logger is None:
            raise PluginError("Attack logger not defined")
        if self.name is None:
            raise PluginError("Plugin has no name")
        if self.attacker_machine_plugin is None:
            raise PluginError("No attacker machine plugin present")
        if self.attacker_machine_plugin.config is None:
            raise PluginError("Configuration broken")

        self.targets = targets
        target_ip = targets[0].get_ip()
        self.setup()
        self.attack_logger.start_attack_plugin(self.attacker_machine_plugin.config.vmname(), target_ip, self.name, ttp=self.get_ttp())
        res = self.run(targets)
        self.teardown()
        self.attack_logger.stop_attack_plugin(self.attacker_machine_plugin.config.vmname(), target_ip, self.name, ttp=self.get_ttp())
        return res

    def get_ttp(self) -> str:
        """ Returns the ttp of the plugin, please set in boilerplate

        :meta private:

        """
        if self.ttp:
            return self.ttp

        raise NotImplementedError

    def get_references(self) -> list[str]:
        """ Returns the references of the plugin, please set in boilerplate

        :meta private:

        """
        if self.references:
            return self.references

        raise NotImplementedError

    def get_target_by_name(self, name: str) -> Any:
        """ Returns a target machine out of the target pool by matching the name
        If there is no matching name it will look into the "nicknames" list of the machine config

        @param name: The name to match for
        @returns: the machine
        """

        # TODO: Current return is Machine, but refactoring should replace it with MachineryPlugin

        if self.targets is None:
            raise PluginError("No targets available")

        for target in self.targets:
            if target.get_name() == name:
                return target

        for target in self.targets:
            if name in target.get_nicknames():
                return target

        raise ConfigurationError(f"No matching machine in experiment config for {name}")
