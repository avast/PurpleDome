#!/usr/bin/env python3
""" Base class for all plugin types """

import os
# from shutil import copy


class BasePlugin():
    """ Base class for plugins """

    required_files = None   # a list of files shipped with the plugin to be installed
    name = None  # The name of the plugin
    description = None  # The description of this plugin

    def __init__(self):
        # self.machine = None
        self.plugin_path = None
        self.machine_plugin = None
        self.sysconf = {}

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

    def copy_to_machine(self, filename):
        """ Copies a file shipped with the plugin to the machine share folder

        @param filename: File from the plugin folder to copy to the machine share.
        """

        self.machine_plugin.put(filename, self.machine_plugin.get_playground())

        # plugin_folder = os.path.dirname(os.path.realpath(self.plugin_path))
        # src = os.path.join(plugin_folder, filename)

        # if os.path.commonprefix((os.path.realpath(src), plugin_folder)) != plugin_folder:
        #    raise PluginError

        # copy(src, self.sysconf["abs_machinepath_external"])

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

    def get_description(self):
        """ Returns the description of the plugin, please set in boilerplate """
        if self.description:
            return self.description

        raise NotImplementedError
