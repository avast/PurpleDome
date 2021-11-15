#!/usr/bin/env python3

# Some users are created (with weak passwords) and sshd is set to allow password-based access

from plugins.base.vulnerability_plugin import VulnerabilityPlugin


class VulnerabilityOk(VulnerabilityPlugin):

    # Boilerplate
    name = "missing_start"
    description = "Adding users with weak passwords"
    ttp = "T1110"
    references = ["https://attack.mitre.org/techniques/T1110/"]

    required_files = []    # Files shipped with the plugin which are needed by the machine. Will be copied to the share

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__

    def stop(self):

        if self.machine_plugin.config.os() == "linux":
            for user in self.conf["linux"]:
                # Remove user
                cmd = f"sudo userdel -r {user['name']}"
                self.run_cmd(cmd)

        elif self.machine_plugin.config.os() == "windows":
            for user in self.conf["windows"]:
                # net user username /delete
                cmd = f"net user {user['name']} /delete"
                self.run_cmd(cmd)

            # Remove the new users to RDP (just in case we want to test RDP)
            for user in self.conf["windows"]:
                # net user username /delete
                cmd = f""""NET LOCALGROUP "Remote Desktop Users" {user['name']} /DELETE"""
                self.run_cmd(cmd)

        else:
            raise NotImplementedError
