#!/usr/bin/env python3
""" Base class for all plugin types """

import os
import yaml
# from shutil import copy

# TODO: Proper planning and re-building of plugin system. Especially the default config handling should be streamlined. All the plugin types should have a very similar programming interface.


class BasePlugin():
    """ Base class for plugins """

    required_files = None   # a list of files shipped with the plugin to be installed
    name = None  # The name of the plugin
    alternative_names = []  # The is an optional list of alternative names
    description = None  # The description of this plugin

    def __init__(self):
        # self.machine = None
        self.plugin_path = None
        self.machine_plugin = None
        self.sysconf = {}
        self.conf = {}

        self.default_config_name = "default_config.yaml"

    def setup(self):
        """ Prepare everything for the plugin """

        for a_file in self.required_files:
            src = os.path.join(os.path.dirname(self.plugin_path), a_file)
            print(src)
            self.copy_to_machine(src)

    def set_machine_plugin(self, machine_plugin):
        """ Set the machine plugin class to communicate with

        @param machine_plugin: Machine plugin to communicate with
        """

        self.machine_plugin = machine_plugin

    def set_sysconf(self, config):
        """ Set system config

        @param config: A dict with system configuration relevant for all plugins
        """

        self.sysconf["abs_machinepath_internal"] = config["abs_machinepath_internal"]
        self.sysconf["abs_machinepath_external"] = config["abs_machinepath_external"]
        self.load_default_config()

    def process_config(self, config):
        """ process config and use defaults if stuff is missing

        @param config: The config dict
        """

        # TODO: Move to python 3.9 syntax z = x | y

        self.conf = {**self.conf, **config}

        print("\n\n\n\n\n BASE plugin")
        print(self.conf)

    def copy_to_machine(self, filename):
        """ Copies a file shipped with the plugin to the machine share folder

        @param filename: File from the plugin folder to copy to the machine share.
        """

        self.machine_plugin.put(filename, self.machine_plugin.get_playground())

    def get_from_machine(self, src, dst):
        """ Get a file from the machine """
        self.machine_plugin.get(src, dst)  # nosec

    def run_cmd(self, command, warn=True, disown=False):
        """ Execute a command on the vm using the connection

         @param command: Command to execute
         @param disown: Run in background
         """

        print(f"      Plugin running command {command}")

        res = self.machine_plugin.__call_remote_run__(command, disown=disown)
        return res

    def get_name(self):
        """ Returns the name of the plugin, please set in boilerplate """
        if self.name:
            return self.name

        raise NotImplementedError

    def get_names(self) -> []:
        """ Adds the name of the plugin to the alternative names and returns the list """

        res = set()

        if self.name:
            res.add(self.name)

        for i in self.alternative_names:
            res.add(i)

        if len(res):
            return list(res)

        raise NotImplementedError

    def get_description(self):
        """ Returns the description of the plugin, please set in boilerplate """
        if self.description:
            return self.description

        raise NotImplementedError

    def get_default_config_filename(self):
        """ Generate the default filename of the default configuration file """

        return os.path.join(os.path.dirname(self.plugin_path), self.default_config_name)

    def get_raw_default_config(self):
        """ Returns the default config as string. Usable as an example and for documentation """

        if os.path.isfile(self.get_default_config_filename()):
            with open(self.get_default_config_filename(), "rt") as fh:
                return fh.read()
        else:
            return f"# The plugin {self.get_name()} does not support configuration"

    def load_default_config(self):
        """ Reads and returns the default config as dict """

        filename = self.get_default_config_filename()

        if not os.path.isfile(filename):
            print(f"Did not find default config {filename}")
            self.conf = {}
        else:
            with open(filename) as fh:
                print(f"Loading default config {filename}")
                self.conf = yaml.safe_load(fh)
            if self.conf is None:
                self.conf = {}
