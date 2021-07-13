#!/usr/bin/env python3
""" Manage plugins """

import straight.plugin
from glob import glob
import os

from plugins.base.plugin_base import BasePlugin
from plugins.base.attack import AttackPlugin
from plugins.base.machinery import MachineryPlugin
from plugins.base.sensor import SensorPlugin
from plugins.base.vulnerability_plugin import VulnerabilityPlugin
from app.interface_sfx import CommandlineColors
# from app.interface_sfx import CommandlineColors

sections = [{"name": "Vulnerabilities",
             "subclass": VulnerabilityPlugin},
            {"name": "Machinery",
             "subclass": MachineryPlugin},
            {"name": "Attack",
             "subclass": AttackPlugin},
            {"name": "Sensors",
             "subclass": SensorPlugin},
            ]


class PluginManager():
    """ Manage plugins """

    def __init__(self, attack_logger):
        """

        @param attack_logger: The attack logger to use
        """
        self.base = "plugins/**/*.py"
        self.attack_logger = attack_logger

    def get_plugins(self, subclass, name_filter=None) -> [BasePlugin]:
        """ Returns a list plugins matching specified criteria


        :param subclass: The subclass to use to filter plugins. Currently: AttackPlugin, MachineryPlugin, SensorPlugin, VulnerabilityPlugin
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
                plugin.set_logger(self.attack_logger)
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

        for section in sections:
            print(f'\t\t{section["name"]}')
            plugins = self.get_plugins(section["subclass"])
            for plugin in plugins:
                print(f"Name: {plugin.get_name()}")
                print(f"Description: {plugin.get_description()}")
                print("\t")

    def check(self, plugin):
        """ Checks a plugin for valid implementation

        @returns: A list of issues
        """

        issues = []

        # Sensors
        if issubclass(type(plugin), SensorPlugin):
            # essential methods: collect
            if plugin.collect.__func__ is SensorPlugin.collect:
                report = f"Method 'collect' not implemented in {plugin.get_name()} in {plugin.plugin_path}"
                issues.append(report)

        # Attacks
        if issubclass(type(plugin), AttackPlugin):
            # essential methods: run
            if plugin.run.__func__ is AttackPlugin.run:
                report = f"Method 'run' not implemented in {plugin.get_name()} in {plugin.plugin_path}"
                issues.append(report)

        # Machinery
        if issubclass(type(plugin), MachineryPlugin):
            # essential methods: get_ip, get_state, up. halt, create, destroy
            if plugin.get_state.__func__ is MachineryPlugin.get_state:
                report = f"Method 'get_state' not implemented in {plugin.get_name()} in {plugin.plugin_path}"
                issues.append(report)
            if plugin.get_ip.__func__ is MachineryPlugin.get_ip:
                report = f"Method 'get_ip' not implemented in {plugin.get_name()} in {plugin.plugin_path}"
                issues.append(report)
            if plugin.up.__func__ is MachineryPlugin.up:
                report = f"Method 'up' not implemented in {plugin.get_name()} in {plugin.plugin_path}"
                issues.append(report)
            if plugin.halt.__func__ is MachineryPlugin.halt:
                report = f"Method 'halt' not implemented in {plugin.get_name()} in {plugin.plugin_path}"
                issues.append(report)
            if plugin.create.__func__ is MachineryPlugin.create:
                report = f"Method 'create' not implemented in {plugin.get_name()} in {plugin.plugin_path}"
                issues.append(report)
            if plugin.destroy.__func__ is MachineryPlugin.destroy:
                report = f"Method 'destroy' not implemented in {plugin.get_name()} in {plugin.plugin_path}"
                issues.append(report)

        # Vulnerabilities
        if issubclass(type(plugin), VulnerabilityPlugin):
            # essential methods: start, stop
            if plugin.start.__func__ is VulnerabilityPlugin.start:
                report = f"Method 'start' not implemented in {plugin.get_name()} in {plugin.plugin_path}"
                issues.append(report)
            if plugin.stop.__func__ is VulnerabilityPlugin.stop:
                report = f"Method 'stop' not implemented in {plugin.get_name()} in {plugin.plugin_path}"
                issues.append(report)

        return issues

    def print_check(self):
        """ Iterates through all installed plugins and verifies them """

        # TODO: Identical name
        # TODO: identical class name

        names = {}
        cnames = {}

        issues = []
        for section in sections:
            # print(f'\t\t{section["name"]}')
            plugins = self.get_plugins(section["subclass"])

            for plugin in plugins:
                # print(f"Checking: {plugin.get_name()}")
                # Check for duplicate names
                name = plugin.get_name()
                if name in names:
                    report = f"Name duplication: {name} is used in {names[name]} and {plugin.plugin_path}"
                    issues.append(report)
                    self.attack_logger.vprint(f"{CommandlineColors.BACKGROUND_RED}{report}{CommandlineColors.ENDC}", 0)
                names[name] = plugin.plugin_path

                # Check for duplicate class names
                name = type(plugin).__name__
                if name in cnames:
                    report = f"Class name duplication: {name} is used in {cnames[name]} and {plugin.plugin_path}"
                    issues.append(report)
                    self.attack_logger.vprint(f"{CommandlineColors.BACKGROUND_RED}{report}{CommandlineColors.ENDC}", 0)
                cnames[name] = type(plugin)

                # Deep checks

                result = self.check(plugin)

                for r in result:
                    print(f"* Issue: {r}")
                if len(result):
                    for r in result:
                        issues.append(r)
                        self.attack_logger.vprint(f"{CommandlineColors.BACKGROUND_RED}{r}{CommandlineColors.ENDC}", 1)
        return issues

    # TODO: Add verify command to verify all plugins (or a specific one)

    def print_default_config(self, subclass_name, name):

        subclass = None

        for a in sections:
            if a["name"] == subclass_name:
                subclass = a["subclass"]
        if subclass is None:
            print("Use proper subclass. Available subclasses are: ")
            "\n- ".join([a for a in sections["name"]])

        plugins = self.get_plugins(subclass, [name])
        for plugin in plugins:
            print(plugin.get_raw_default_config())
