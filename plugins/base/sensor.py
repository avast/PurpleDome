#!/usr/bin/env python3
""" A base plugin class for sensors. Anything installed on the target to collect system information and identify the attack """

import os
from plugins.base.plugin_base import BasePlugin


class SensorPlugin(BasePlugin):
    """ A sensor will be running on the target machine and monitor attacks. To remote control those sensors
    there are sensor plugins. This is the base class for them

    """

    # Boilerplate
    name = None

    required_files = []

    def __init__(self):
        super().__init__()  # pylint:disable=useless-super-delegation
        self.debugit = False
        # self.machine = None

    def set_sysconf(self, config):
        """ Set system config

        @param config: A dict with system configuration relevant for all plugins
        """

        super().set_sysconf(config)
        self.sysconf["sensor_specific"] = config["sensor_specific"]

    def prime(self):
        """ prime sets hard core configs in the target. You can use it to call everything that permanently alters the OS by settings.
        If your prime function returns True the machine will be rebooted after prime-ing it. This is very likely what you want. Only use prime if install is not sufficient.
        """

        return False

    def install_command(self):
        """ Generate the install command. Put everything you need that does not require a reboot in here. If you want to hard core alter the OS of the target, use the prime method """
        raise NotImplementedError

    def install(self):
        """ Install the sensor. Executed on the target. Take the sensor from the share and (maybe) copy it to its destination. Do some setup
        """

        cmd = self.install_command()
        if cmd:
            self.machine_plugin.__call_remote_run__(cmd)

    def start_command(self):
        """ Generate the start command """

        raise NotImplementedError

    def start(self, disown=None):
        """ Start the sensor. The connection to the client is disowned here. = Sent to background. This keeps the process running.

        @param disown: Send async into background
        """

        if disown is None:
            disown = not self.debugit
        cmd = self.start_command()
        if cmd:
            # self.run_cmd(cmd, disown=not self.debugit)
            self.machine_plugin.__call_remote_run__(cmd, disown=disown)

    def stop_command(self):
        """ Generate the stop command """
        raise NotImplementedError

    def stop(self):
        """ Stop the sensor """
        cmd = self.stop_command()
        if cmd:
            # self.run_cmd(cmd)
            self.machine_plugin.__call_remote_run__(cmd)

    def __call_collect__(self, machine_path):
        """ Generate the data collect command

        @param machine_path: Machine specific path to collect data into
        """

        path = os.path.join(machine_path, "sensors", self.name)
        os.makedirs(path)
        self.collect(path)

    def collect_command(self, path):
        """ Generate the data collect command

        @param path: Path to put the data into
        """

    def collect(self, path):
        """ Collect data from sensor. Copy it from sensor collection dir on target OS to the share

        @param path: The path to copy the data into
        """
        raise NotImplementedError
