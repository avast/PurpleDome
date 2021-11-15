#!/usr/bin/env python3

# A plugin to nmap targets slow motion, to evade sensors

from plugins.base.attack import AttackPlugin, Requirement


class MissingRunPlugin(AttackPlugin):

    # Boilerplate
    name = "missing_run"
    description = "Migrate meterpreter to another process via metasploit"
    ttp = "T1055"
    references = ["https://attack.mitre.org/techniques/T1055/"]

    required_files = []    # Files shipped with the plugin which are needed by the kali tool. Will be copied to the kali share

    requirements = [Requirement.METASPLOIT]

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__
