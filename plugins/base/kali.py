#!/usr/bin/env python3
""" Base class for Kali plugins """

from plugins.base.plugin_base import BasePlugin


class KaliPlugin(BasePlugin):
    """ Class to execute a command on a kali system targeting another system """

    # Boilerplate
    name = None
    description = None
    ttp = None
    references = None

    required_files = []

    # TODO: parse results

    def __init__(self):
        super().__init__()
        self.conf = {}     # Plugin specific configuration
        self.sysconf = {}  # System configuration. common for all plugins
        self.attack_logger = None

    def teardown(self):
        """ Cleanup afterwards """
        pass  # pylint: disable=unnecessary-pass

    def run(self, targets):
        """ Run the command

        @param targets: A list of targets, ip addresses will do
        """
        raise NotImplementedError

    def __execute__(self, targets):
        """ Execute the plugin. This is called by the code

        @param targets: A list of targets, ip addresses will do
        """

        self.setup()
        self.attack_logger.start_kali_attack(self.machine_plugin.config.vmname(), targets, self.name, ttp=self.get_ttp())
        res = self.run(targets)
        self.teardown()
        self.attack_logger.stop_kali_attack(self.machine_plugin.config.vmname(), targets, self.name, ttp=self.get_ttp())
        return res

    def command(self, targets, config):
        """ Generate command

        @param targets: A list of targets, ip addresses will do
        @param config: dict with command specific configuration
        """

        raise NotImplementedError

    def __set_logger__(self, attack_logger):
        """ Set the attack logger for this machine """
        self.attack_logger = attack_logger

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
