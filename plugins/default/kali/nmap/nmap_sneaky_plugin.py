#!/usr/bin/env python3

# A plugin to nmap targets slow motion, to evade sensors

from plugins.base.attack import AttackPlugin


class NmapSneakyPlugin(AttackPlugin):

    # Boilerplate
    name = "nmap_sneaky"
    description = "Nmap scan the target slowly. To sneak past detection"
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
        pg = self.get_attacker_playground()
        cmd = f"cd {pg};"
        for t in targets:
            cmd += f"sudo nmap -T1 -F -D RND:5 -f --randomize-hosts {t.get_ip()};"

        res += self.attacker_run_cmd(cmd) or ""

        return res

    def get_config_section_name(self):
        """ Use nmap configuration """

        return "nmap"
