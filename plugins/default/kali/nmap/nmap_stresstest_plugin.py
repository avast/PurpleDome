#!/usr/bin/env python3

# A plugin to nmap targets - in an agressive way to break sensors

from plugins.base.kali import KaliPlugin


class NmapStresstestPlugin(KaliPlugin):

    # Boilerplate
    name = "nmap_stresstest"
    description = "Nmap scan the target. As aggressive as possible to overload sensors. Maybe even crash them"
    ttp = "T1595"
    references = ["https://attack.mitre.org/techniques/T1595/"]

    required_files = []    # Files shipped with the plugin which are needed by the kali tool. Will be copied to the kali share

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__

    def run(self, targets):
        """ Run the command

        @param targets: A list of targets, ip addresses will do
        """

        res = ""

        cmd = f"cd {self.get_playground()};"
        for t in targets:
            cmd += f"nmap -T5 --min-parallelism 100 --max-scan-delay 1 {t};"

        res += self.run_cmd(cmd) or ""

        return res

    def get_config_section_name(self):
        """ Use nmap configuration """

        return "nmap"
