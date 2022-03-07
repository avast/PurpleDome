#!/usr/bin/env python3
""" Base class for all plugin types """

from inspect import currentframe, getframeinfo
import os
from typing import Optional, Any
import yaml
from app.exceptions import PluginError  # type: ignore
import app.exceptions                   # type: ignore
from app.attack_log import AttackLog


class BasePlugin():
    """ Base class for plugins """

    required_files: list[str] = []   #: a list of files shipped with the plugin to be installed
    name: Optional[str] = None  #: The name of the plugin
    alternative_names: list[str] = []  #: An optional list of alternative names
    description: Optional[str] = None  #: The description of this plugin

    def __init__(self) -> None:
        # self.machine = None
        self.plugin_path: Optional[str] = None
        self.machine_plugin: Any = None
        # self.sysconf = {}
        self.conf: dict = {}
        self.attack_logger: Optional[AttackLog] = None

        self.default_config_name = "default_config.yaml"

    def run_cmd(self, command: str, disown: bool = False) -> str:
        """ Execute a command on the vm using the connection

         :param command: Command to execute
         :param disown: Run in background
         """

        if self.machine_plugin is None:
            raise PluginError("machine to run command on is not registered")

        self.vprint(f"      Plugin running command {command}", 3)

        res = self.machine_plugin.__call_remote_run__(command, disown=disown)
        return res

    def copy_to_machine(self, filename: str) -> None:
        """ Copies a file shipped with the plugin to the machine share folder

        :param filename: File from the plugin folder to copy to the machine share.
        """

        if self.machine_plugin is not None:
            self.machine_plugin.put(filename, self.machine_plugin.get_playground())
        else:
            raise PluginError("Missing machine")

    def get_from_machine(self, src: str, dst: str) -> None:
        """ Get a file from the machine

        :param src: source file name on the machine
        :param dst: destination filename on the host
        """
        if self.machine_plugin is not None:
            self.machine_plugin.get(src, dst)  # nosec
        else:
            raise PluginError("Missing machine")

    def get_filename(self) -> str:
        """ Returns the current filename. This can be used for debugging

        :meta private:

        :returns: Filename of currenty executed py file

        """
        cf = currentframe()  # pylint: disable=invalid-name
        if cf is None:
            raise PluginError("can not get current frame")
        if cf.f_back is None:
            raise PluginError("can not get current frame")
        return getframeinfo(cf.f_back).filename

    def get_linenumber(self) -> int:
        """ Returns the current linenumber.  This can be used for debugging

        :returns: currently executed linenumber
        """
        cf = currentframe()  # pylint: disable=invalid-name
        if cf is None:
            raise PluginError("can not get current frame")
        if cf.f_back is None:
            raise PluginError("can not get current frame")
        return cf.f_back.f_lineno

    def get_playground(self) -> Optional[str]:
        """ Returns the machine specific playground path name

         This is the folder on the machine where we run our tasks in

         :returns: playground path on the target machine
         """

        if self.machine_plugin is None:
            raise PluginError("Default machine not configured. Maybe you are creating an attack plugin. Then there are special attack/target machines")

        return self.machine_plugin.get_playground()

    def set_logger(self, attack_logger: AttackLog) -> None:
        """ Set the attack logger for this machine

        :meta private:

        :param attack_logger: Attack logger object
        """
        self.attack_logger = attack_logger

    def process_templates(self) -> None:  # pylint: disable=no-self-use
        """ A method you can optionally implement to transfer your jinja2 templates into the files yo want to send to the target. See 'required_files'

        :meta private:

        """

        return

    def copy_to_attacker_and_defender(self) -> None:  # pylint: disable=no-self-use
        """ Copy attacker/defender specific files to the machines

        :meta private:

        """

        return

    def setup(self) -> None:
        """ Prepare everything for the plugin

        :meta private:

        """

        self.process_templates()

        for a_file in self.required_files:
            if self.plugin_path is None:
                raise PluginError("Plugin has no path...strange....")
            src = os.path.join(os.path.dirname(self.plugin_path), a_file)
            self.vprint(src, 3)
            self.copy_to_machine(src)

        self.copy_to_attacker_and_defender()

    def set_machine_plugin(self, machine_plugin: Any) -> None:
        """ Set the machine plugin class to communicate with

        :meta private:

        :param machine_plugin: Machine plugin to communicate with
        """

        self.machine_plugin = machine_plugin

    def set_sysconf(self, config: dict) -> None:   # pylint:disable=unused-argument
        """ Set system config

        :meta private:

        :param config: A dict with system configuration relevant for all plugins. Currently ignored
        """

        # self.sysconf["abs_machinepath_internal"] = config["abs_machinepath_internal"]
        # self.sysconf["abs_machinepath_external"] = config["abs_machinepath_external"]
        self.load_default_config()

    def process_config(self, config: dict) -> None:
        """ process config and use defaults if stuff is missing

        :meta private:

        :param config: The config dict
        """

        # TODO: Move to python 3.9 syntax z = x | y

        self.conf = {**self.conf, **config}

    def get_name(self) -> str:
        """ Returns the name of the plugin

        This method checks the boilerplate for the name

        :returns: The plugin name
        """
        if self.name:
            return self.name

        raise NotImplementedError

    def get_names(self) -> list[str]:
        """ Returns a list of names and nicknames for a plugin.

         Please set that in the boilerplate

         :returns: A list of potential names
         """

        res = set()

        if self.name:
            res.add(self.name)

        for i in self.alternative_names:
            res.add(i)

        if len(res) > 0:
            return list(res)

        raise NotImplementedError

    def get_description(self) -> str:
        """ Returns the description of the plugin, please set it in boilerplate

        :returns: The description of the plugin
        """
        if self.description:
            return self.description

        raise NotImplementedError

    def get_plugin_path(self) -> str:
        """ Returns the path the plugin file(s) are stored in

        :meta private:

        :returns: The path with the plugin code
        """

        if self.plugin_path is None:
            raise PluginError("Non existing plugin path")

        return os.path.join(os.path.dirname(self.plugin_path))

    def get_default_config_filename(self) -> str:
        """ Generate the default filename of the default configuration file

        :meta private:

        :returns: The filename of the default config
        """

        return os.path.join(self.get_plugin_path(), self.default_config_name)

    def get_raw_default_config(self) -> str:
        """ Returns the default config as string. Usable as an example and for documentation

        :meta private:

        """

        if os.path.isfile(self.get_default_config_filename()):
            with open(self.get_default_config_filename(), "rt", encoding="utf8") as fh:
                return fh.read()
        else:
            return f"# The plugin {self.get_name()} does not support configuration"

    def load_default_config(self) -> None:
        """ Reads and returns the default config as dict

        :meta private:

        """

        filename = self.get_default_config_filename()

        if not os.path.isfile(filename):
            self.vprint(f"Did not find default config {filename}", 3)
            self.conf = {}
        else:
            with open(filename, encoding="utf8") as fh:
                self.vprint(f"Loading default config {filename}", 3)
                self.conf = yaml.safe_load(fh)
            if self.conf is None:
                self.conf = {}

    def get_config_section_name(self) -> str:
        """ Returns the name for the config sub-section to use for this plugin.

        :meta private:

        Defaults to the name of the plugin. This method should be overwritten if it gets more complicated

        :returns: The name of the config section
        """

        return self.get_name()

    def main_path(self) -> str:  # pylint:disable=no-self-use
        """ Returns the main path of the Purple Dome installation

        :meta private:
        :returns: the main path

        """
        app_dir = os.path.dirname(app.exceptions.__file__)

        return os.path.split(app_dir)[0]

    def vprint(self, text: str, verbosity: int) -> None:
        """ verbosity based stdout printing

        0: Errors only
        1: Main colored information
        2: Detailed progress information
        3: Debug logs, data dumps, everything

        :param text: The text to print
        :param verbosity: the verbosity level the text has.
        """
        if self.attack_logger is not None:
            self.attack_logger.vprint(text, verbosity)
