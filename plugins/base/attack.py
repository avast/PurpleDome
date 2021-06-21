#!/usr/bin/env python3
""" Base class for Kali plugins """

from plugins.base.plugin_base import BasePlugin
from app.exceptions import PluginError, ConfigurationError
from app.calderacontrol import CalderaControl
# from app.metasploit import MSFVenom, Metasploit
import os


class AttackPlugin(BasePlugin):
    """ Class to execute a command on a kali system targeting another system """

    # Boilerplate
    name = None
    description = None
    ttp = None
    references = None

    required_files = []  # Better use the other required_files features
    required_files_attacker = []  # a list of files to automatically install to the attacker
    required_files_target = []    # a list of files to automatically copy to the targets

    # TODO: parse results

    def __init__(self):
        super().__init__()
        self.conf = {}     # Plugin specific configuration
        self.sysconf = {}  # System configuration. common for all plugins
        self.attacker_machine_plugin = None  # The machine plugin referencing the attacker. The Kali machine should be the perfect candidate
        self.target_machine_plugin = None  # The machine plugin referencing the target
        self.caldera = None  # The Caldera connection object
        self.targets = None

        self.metasploit_password = "password"
        self.metasploit_user = "user"
        self.metasploit = None

    def copy_to_attacker_and_defender(self):
        """ Copy attacker/defender specific files to the machines. Called by setup, do not call it yourself. template processing happens before """

        for a_file in self.required_files_attacker:
            src = os.path.join(os.path.dirname(self.plugin_path), a_file)
            self.vprint(src, 3)
            self.attacker_machine_plugin.put(src, self.attacker_machine_plugin.get_playground())

        # TODO: add target(s)

    def teardown(self):
        """ Cleanup afterwards """
        pass  # pylint: disable=unnecessary-pass

    def attacker_run_cmd(self, command, warn=True, disown=False):
        """ Execute a command on the attacker

         @param command: Command to execute
         @param disown: Run in background
         """

        if self.attacker_machine_plugin is None:
            raise PluginError("machine to run command on is not registered")

        self.vprint(f"      Plugin running command {command}", 3)

        res = self.attacker_machine_plugin.__call_remote_run__(command, disown=disown)
        return res

    def targets_run_cmd(self, command, warn=True, disown=False):
        """ Execute a command on the target

         @param command: Command to execute
         @param disown: Run in background
         """

        if self.target_machine_plugin is None:
            raise PluginError("machine to run command on is not registered")

        self.vprint(f"      Plugin running command {command}", 3)

        res = self.target_machine_plugin.__call_remote_run__(command, disown=disown)
        return res

    def set_target_machines(self, machine):
        """ Set the machine to target

        @param machine: Machine plugin to communicate with
        """

        self.target_machine_plugin = machine.vm_manager

    def set_attacker_machine(self, machine):
        """ Set the machine plugin class to target

        @param machine: Machine to communicate with
        """

        self.attacker_machine_plugin = machine.vm_manager

    def set_caldera(self, caldera: CalderaControl):
        """ Set the caldera control to be used for caldera attacks

         @param caldera: The caldera object to connect through
         """
        self.caldera = caldera

    def caldera_attack(self, target, ability_id, parameters=None):
        """ Attack a single target using caldera

        @param target: Target machine object
        @param ability_id: Ability if od caldera ability to run
        @param parameters: parameters to pass to the ability
        """

        self.caldera.attack(paw=target.get_paw(),
                            ability_id=ability_id,
                            group=target.get_group(),
                            target_platform=target.get_os(),
                            parameters=parameters
                            )

    def get_attacker_playground(self):
        """ Returns the attacker machine specific playground

         Which is the folder on the machine where we run our tasks in
         """

        if self.attacker_machine_plugin is None:
            raise PluginError("Attacker machine not configured.")

        return self.attacker_machine_plugin.get_playground()

    def run(self, targets):
        """ Run the command

        @param targets: A list of targets, ip addresses will do
        """
        raise NotImplementedError

    def install(self):
        """ Install and setup requirements for the attack
        """

        return None

    def __execute__(self, targets):
        """ Execute the plugin. This is called by the code

        @param targets: A list of targets => machines
        """

        self.targets = targets
        ips = [tgt.get_ip() for tgt in targets]
        self.setup()
        self.attack_logger.start_kali_attack(self.attacker_machine_plugin.config.vmname(), ips, self.name, ttp=self.get_ttp())
        res = self.run(targets)
        self.teardown()
        self.attack_logger.stop_kali_attack(self.attacker_machine_plugin.config.vmname(), ips, self.name, ttp=self.get_ttp())
        return res

    def get_ttp(self):
        """ Returns the ttp of the plugin, please set in boilerplate """
        if self.ttp:
            return self.ttp

        raise NotImplementedError

    def get_references(self):
        """ Returns the references of the plugin, please set in boilerplate """
        if self.references:
            return self.references

        raise NotImplementedError

    def get_target_by_name(self, name):
        """ Returns a target machine out of the target pool by matching the name
        If there is no matching name it will look into the "nicknames" list of the machine config

        @param name: The name to match for
        @returns: the machine
        """

        for t in self.targets:
            if t.get_name() == name:
                return t

        for t in self.targets:
            if name in t.get_nicknames():
                return t

        raise ConfigurationError(f"No matching machine in experiment config for {name}")
