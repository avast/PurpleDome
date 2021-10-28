#!/usr/bin/env python3

# A plugin to experiment with Linux osquery

# https://github.com/osquery/osquery-python

from plugins.base.sensor import SensorPlugin
# import os
# from jinja2 import Environment, FileSystemLoader, select_autoescape


class LinuxOSQueryPlugin(SensorPlugin):
    # Boilerplate
    name = "osquery"
    description = "Linux osquery plugin"  # Can later be extended to support other OS-es as well

    required_files = []

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__

        self.debugit = False

    def process_templates(self):
        """ process jinja2 templates of the config files and insert own config """

        pass

    def prime(self):
        """ Hard-core install. Requires a reboot """

        # pg = self.get_playground()

        self.vprint("Installing Linux OSQuery", 3)

        self.run_cmd('echo "deb [arch=amd64] https://pkg.osquery.io/deb deb main" | sudo tee /etc/apt/sources.list.d/osquery.list')
        self.run_cmd("sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 1484120AC4E9F8A1A577AEEE97A80C63C9D8B80B")
        self.run_cmd("sudo apt update")
        self.run_cmd("sudo apt -y install osquery")
        self.run_cmd("")
        # sudo apt -y install python3-pip
        # pip install osquery

        return False

    def install(self):
        """ Installs the filebeat sensor """

        return

    def start(self):
        self.run_cmd("osqueryi --ephemeral --disable_logging --disable_database --extensions_socket /home/vagrant/test.sock")  # TODO: Find better socket name

        """
        ec = osquery.ExtensionClient("/home/vagrant/test.sock")
        ec.open()
        c = ec.extension_client()
        c.query("select timestamp from time")
        """

        return None

    def stop(self):
        """ Stop the sensor """
        return

    def collect(self, path):
        """ Collect sensor data """

        dst = ""
        return [dst]
