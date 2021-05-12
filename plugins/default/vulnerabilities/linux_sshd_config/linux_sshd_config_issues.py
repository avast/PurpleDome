#!/usr/bin/env python3

# Some users are created (with weak passwords) and sshd is set to allow password-based access

from plugins.base.vulnerability_plugin import VulnerabilityPlugin


class SshdVulnerability(VulnerabilityPlugin):

    # Boilerplate
    name = "sshd_config_vul"
    description = "Allowing passwords based sshd access"
    ttp = "T1110"
    references = ["https://attack.mitre.org/techniques/T1110/"]

    required_files = []    # Files shipped with the plugin which are needed by the machine. Will be copied to the share

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__

    def start(self):

        # allow password access via ssh
        cmd = "sudo sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config"
        self.run_cmd(cmd)

        # Restart ssh
        cmd = "sudo service ssh restart"
        self.run_cmd(cmd)

    def stop(self):

        # Re-configure sshd to stable state
        cmd = "sudo sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config"
        self.run_cmd(cmd)

        # Restart ssh
        cmd = "sudo service ssh restart"
        self.run_cmd(cmd)
