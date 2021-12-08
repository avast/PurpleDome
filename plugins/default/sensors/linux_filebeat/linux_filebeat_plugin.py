#!/usr/bin/env python3

# A plugin to experiment with Linux logstash filebeat sensors
# https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-installation-configuration.html

from plugins.base.sensor import SensorPlugin
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
import time


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

        pg = self.get_playground()

        self.vprint("Installing Linux filebeat sensor", 3)

        # Filebeat
        fb_file = "filebeat-7.15.2-amd64.deb"
        self.run_cmd(f"curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/{fb_file}")
        self.run_cmd(f"sudo dpkg -i {fb_file}")

        # Logstash

        self.run_cmd("wget -qO- https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -")
        self.run_cmd("sudo apt-get install apt-transport-https")
        self.run_cmd("echo 'deb https://artifacts.elastic.co/packages/7.x/apt stable main' | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list")
        self.run_cmd("sudo apt update && sudo apt install logstash")

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

        self.run_cmd("sudo filebeat modules enable system iptables")
        self.run_cmd("sudo filebeat setup --pipelines --modules iptables,system,")
        # self.run_cmd("sudo systemctl start logstash.service")
        self.run_cmd("sudo nohup /usr/share/logstash/bin/logstash  -f /etc/logstash/conf.d/filebeat.conf &", disown=True)
        time.sleep(20)
        self.run_cmd("sudo service filebeat start")

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
