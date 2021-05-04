#!/usr/bin/env python3
""" Manage plugins """

import straight.plugin
from glob import glob
import os

from plugins.base.plugin_base import BasePlugin
from plugins.base.kali import KaliPlugin
from plugins.base.machinery import MachineryPlugin
from plugins.base.sensor import SensorPlugin
from plugins.base.vulnerability_plugin import VulnerabilityPlugin
# from app.interface_sfx import CommandlineColors


class PluginManager():
    """ Manage plugins """

    def __init__(self):
        self.base = "plugins/**/*.py"

    def get_plugins(self, subclass, name_filter=None) -> [BasePlugin]:
        """ Returns a list plugins matching specified criteria


        :param subclass: The subclass to use to filter plugins. Currently: KaliPlugin, MachineryPlugin, SensorPlugin, VulnerabilityPlugin
        :param name_filter: an optional list of names to select the plugins by
        :return: A list of instantiated plugins
        """

        res = []

        def get_handlers(a_plugin) -> [subclass]:
            return a_plugin.produce()

        plugin_dirs = set()
        for a_glob in glob(self.base, recursive=True):
            plugin_dirs.add(os.path.dirname(a_glob))

        for a_dir in plugin_dirs:
            plugins = straight.plugin.load(a_dir, subclasses=subclass)

            handlers = get_handlers(plugins)

            for plugin in handlers:
                if name_filter is None:
                    res.append(plugin)
                else:
                    names = set(plugin.get_names())
                    intersection = names.intersection(name_filter)
                    if len(intersection):
                        res.append(plugin)
        return res

    def print_list(self):
        """ Print a pretty list of all available plugins """

        sections = [{"name": "Vulnerabilities",
                     "subclass": VulnerabilityPlugin},
                    {"name": "Machinery",
                     "subclass": MachineryPlugin},
                    {"name": "Kali",
                     "subclass": KaliPlugin},
                    {"name": "Sensors",
                     "subclass": SensorPlugin},
                    ]

        for section in sections:
            print(f'\t\t{section["name"]}')
            plugins = self.get_plugins(section["subclass"])
            for plugin in plugins:
                print(f"Name: {plugin.get_name()}")
                print(f"Description: {plugin.get_description()}")
                print("\t")
