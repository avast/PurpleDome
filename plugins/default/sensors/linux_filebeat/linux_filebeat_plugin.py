#!/usr/bin/env python3

# A plugin to experiment with Linux logstash filebeat sensors

from plugins.base.sensor import SensorPlugin
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape


class LinuxFilebeatPlugin(SensorPlugin):
    # Boilerplate
    name = "linux_filebeat"
    description = "Linux filebeat plugin"

    required_files = ["filebeat.conf",
                      "filebeat.yml",
                      ]

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__

        self.debugit = False

    def process_templates(self):
        """ process jinja2 templates of the config files and insert own config """

        env = Environment(
            loader=FileSystemLoader(self.get_plugin_path(), encoding='utf-8', followlinks=False),
            autoescape=select_autoescape()
        )
        template = env.get_template("filebeat_template.conf")
        dest = os.path.join(self.get_plugin_path(), "filebeat.conf")
        with open(dest, "wt") as fh:
            res = template.render({"playground": self.get_playground()})
            fh.write(res)

    def prime(self):
        """ Hard-core install. Requires a reboot """

        # For reference: This is the core config we will need. In addition there are two reg files to apply to the registry
        #        sc control aswbidsagent 255
        #        timeout /t 5
        #        'copy /y "cd %userprofile% & aswidptestdll.dll" "c:\Program Files\Avast Software\Avast\"'
        #        reg.exe add "HKLM\SOFTWARE\Avast Software\Avast\properties\IDP\Setting" /v debug_channel.enabled /t REG_DWORD /d 1 /f
        #        timeout /t 2
        #        sc start aswbidsagent

        # Important: AV must be 21.2
        # dll_name = self.conf["dll_name"]

        # idp_tool_folder = self.conf["idp_tool_folder"]

        pg = self.get_playground()

        self.vprint("Installing Linux filebeat sensor", 3)

        self.run_cmd("sudo wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -")
        self.run_cmd('sudo echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-7.x.list')
        self.run_cmd("sudo apt update")
        self.run_cmd("sudo apt -y install default-jre")
        self.run_cmd("sudo apt -y install logstash")
        self.run_cmd("sudo apt -y install filebeat")

        # Copy config
        self.run_cmd(f"sudo cp {pg}/filebeat.yml /etc/filebeat/filebeat.yml")
        self.run_cmd(f"sudo cp {pg}/filebeat.conf /etc/logstash/conf.d")

        # Cleanup
        self.run_cmd(f"rm {pg}/filebeat.json")
        self.run_cmd(f"touch {pg}/filebeat.json")
        self.run_cmd(f"chmod o+w {pg}/filebeat.json")

        return False

    def install(self):
        """ Installs the filebeat sensor """

        return

    def start(self):

        self.run_cmd("sudo filebeat modules enable system,iptables")
        self.run_cmd("sudo filebeat setup --pipelines --modules iptables,system,")
        self.run_cmd("sudo systemctl enable filebeat")
        self.run_cmd("sudo systemctl start filebeat")
        self.run_cmd("sudo systemctl enable logstash.service")
        self.run_cmd("sudo systemctl start logstash.service")

        return None

    def stop(self):
        """ Stop the sensor """
        return

    def collect(self, path):
        """ Collect sensor data """

        pg = self.get_playground()
        dst = os.path.join(path, "filebeat.json")
        self.get_from_machine(f"{pg}/filebeat.json", dst)  # nosec
        return [dst]
