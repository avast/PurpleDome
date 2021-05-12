#!/usr/bin/env python3

# Enable RDP for users
# https://pureinfotech.com/enable-remote-desktop-command-prompt-windows-10/

from plugins.base.vulnerability_plugin import VulnerabilityPlugin


class RDPVulnerability(VulnerabilityPlugin):

    # Boilerplate
    name = "rdp_config_vul"
    description = "Allowing rdp access"
    ttp = "T1110"
    references = ["https://attack.mitre.org/techniques/T1110/"]

    required_files = []    # Files shipped with the plugin which are needed by the machine. Will be copied to the share

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__

    def start(self):

        # allow password access via rdp
        cmd = r"""reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f"""
        self.run_cmd(cmd)

        # Open Firewall
        cmd = """netsh advfirewall firewall set rule group="remote desktop" new enable=Yes"""
        self.run_cmd(cmd)

    def stop(self):

        # Re-configure sshd to stable state
        cmd = r"""reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 1 /f"""
        self.run_cmd(cmd)

        # Reset firewall
        cmd = """netsh advfirewall firewall set rule group="remote desktop" new enable=No"""
        self.run_cmd(cmd)
