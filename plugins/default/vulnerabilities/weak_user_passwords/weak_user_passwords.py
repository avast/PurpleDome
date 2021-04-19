#!/usr/bin/env python3

# Some users are created (with weak passwords) and sshd is set to allow password-based access

from plugins.base.vulnerability_plugin import VulnerabilityPlugin


class WeakPasswordVulnerabilityVulnerability(VulnerabilityPlugin):

    # Boilerplate
    name = "weak_user_passwords"
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

            # user with password "test"
            cmd = "useradd -m -p '$6$bc4k4Tq2.1GW$0ysyuxyfyds2JkfVEf9xHy39MhpS.hhnAo4sBLprNfIHqcpaa9GJseRJJsrq0cSOWwYlOPrdHQNHp10E1ekO81' -s /bin/bash test"
            print(cmd)
            self.run_cmd(cmd)

            # user with password "passw0rd"
            cmd = "useradd -m -p '$6$q5PAnDI5K0uv$hMGMJQleeS9F2yLOiHXs2PxZHEmV.ook8jyWILzDGDxSTJmTTZSe.QgLVrnuwiyAl5PFJVARkMsSnPICSndJR1' -s /bin/bash password"
            print(cmd)
            self.run_cmd(cmd)
        elif self.machine_plugin.config.os() == "windows":
            # net user username password /add
            cmd = "net user test test /add"
            print(cmd)
            self.run_cmd(cmd)

            cmd = "net user password passw0rd /add"
            print(cmd)
            self.run_cmd(cmd)

            # Adding the new users to RDP (just in case we want to test RDP)
            cmd = """NET LOCALGROUP "Remote Desktop Users" password /ADD"""
            print(cmd)
            self.run_cmd(cmd)

            cmd = """NET LOCALGROUP "Remote Desktop Users" test /ADD"""
            print(cmd)
            self.run_cmd(cmd)

        else:
            raise NotImplementedError

    def stop(self):

        if self.machine_plugin.config.os() == "linux":
            # Remove user
            cmd = "sudo userdel -r test"
            print(cmd)
            self.run_cmd(cmd)

            # Remove user
            cmd = "sudo userdel -r password"
            print(cmd)
            self.run_cmd(cmd)
        elif self.machine_plugin.config.os() == "windows":
            # net user username /delete

            cmd = "net user test /delete"
            print(cmd)
            self.run_cmd(cmd)

            cmd = "net user password /delete"
            print(cmd)
            self.run_cmd(cmd)

            # Remove the new users to RDP (just in case we want to test RDP)
            cmd = """NET LOCALGROUP "Remote Desktop Users" password /DELETE"""
            print(cmd)
            self.run_cmd(cmd)

            cmd = """NET LOCALGROUP "Remote Desktop Users" test /DELETE"""
            print(cmd)
            self.run_cmd(cmd)

        else:
            raise NotImplementedError
