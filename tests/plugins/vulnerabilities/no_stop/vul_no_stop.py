#!/usr/bin/env python3

# Some users are created (with weak passwords) and sshd is set to allow password-based access

from plugins.base.vulnerability_plugin import VulnerabilityPlugin


class VulnerabilityOk(VulnerabilityPlugin):

    # Boilerplate
    name = "missing_stop"
    description = "Adding users with weak passwords"
    ttp = "T1110"
    references = ["https://attack.mitre.org/techniques/T1110/"]

    required_files = []    # Files shipped with the plugin which are needed by the machine. Will be copied to the share

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__

    def start(self):

        if self.machine_plugin.config.os() == "linux":
            # Add vulnerable user
            # mkpasswd -m sha-512    # To calc the passwd
            # This is in the debian package "whois"

            for user in self.conf["linux"]:
                cmd = f"sudo useradd -m -p '{user['password']}' -s /bin/bash {user['name']}"
                self.run_cmd(cmd)

        elif self.machine_plugin.config.os() == "windows":

            for user in self.conf["windows"]:
                # net user username password /add
                cmd = f"net user {user['name']} {user['password']} /add"
                self.run_cmd(cmd)

            for user in self.conf["windows"]:
                # Adding the new users to RDP (just in case we want to test RDP)
                cmd = f"""NET LOCALGROUP "Remote Desktop Users" {user['name']} /ADD"""
                self.run_cmd(cmd)

        else:
            raise NotImplementedError