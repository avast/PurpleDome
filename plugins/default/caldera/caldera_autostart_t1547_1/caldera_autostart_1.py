#!/usr/bin/env python3

# A plugin to nmap targets slow motion, to evade sensors

from plugins.base.attack import AttackPlugin, Requirement
from app.interface_sfx import CommandlineColors


class CalderaAutostartPlugin1(AttackPlugin):

    # Boilerplate
    name = "caldera_autostart_1"
    description = "Setting a registry key for autostart"
    ttp = "T1547.001"
    references = ["https://attack.mitre.org/techniques/T1547/001/"]

    required_files = []    # Files shipped with the plugin which are needed by the kali tool. Will be copied to the kali share
    requirements = [Requirement.CALDERA]

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__

    def run(self, targets):
        """ Run the command

        @param targets: A list of targets, ip addresses will do
        """

        # HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run

        res = ""
        self.attack_logger.vprint(f"{CommandlineColors.OKCYAN}Starting caldera attack to add run key {CommandlineColors.ENDC}", 1)
        self.caldera_attack(self.targets[0],
                            "163b023f43aba758d36f524d146cb8ea",
                            parameters={"command_to_execute": r"C:\\Windows\\system32\\calc.exe"},
                            tactics="Persistence",
                            tactics_id="TA0003",
                            situation_description="Setting an autorun key runonce")
        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Ending caldera attack to add run key {CommandlineColors.ENDC}", 1)

        return res
