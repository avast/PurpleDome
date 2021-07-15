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

    def prime(self):  # pylint: disable=no-self-use
        """ prime sets hard core configs in the target. You can use it to call everything that permanently alters the OS by settings.
        If your prime function returns True the machine will be rebooted after prime-ing it. This is very likely what you want. Only use prime if install is not sufficient.
        """

        return False

    def install(self):  # pylint: disable=no-self-use
        """ Install the sensor. Executed on the target. Take the sensor from the share and (maybe) copy it to its destination. Do some setup
        """

        return True

    def start(self, disown=None):  # pylint: disable=unused-argument, no-self-use
        """ Start the sensor. The connection to the client is disowned here. = Sent to background. This keeps the process running.

        @param disown: Send async into background
        """

        return True

    def stop(self):  # pylint: disable=no-self-use
        """ Stop the sensor """

        return True

    def __call_collect__(self, machine_path):
        """ Generate the data collect command

        @param machine_path: Machine specific path to collect data into
        """

        path = os.path.join(machine_path, "sensors", self.name)
        os.makedirs(path)
        return self.collect(path)

    def collect(self, path) -> []:
        """ Collect data from sensor. Copy it from sensor collection dir on target OS to the share

        @param path: The path to copy the data into
        @returns: A list of files to put into the loot zip
        """
        raise NotImplementedError
