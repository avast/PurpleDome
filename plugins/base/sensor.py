#!/usr/bin/env python3
""" A base plugin class for sensors. Anything installed on the target to collect system information and identify the attack """

import os
# from typing import Optional
from plugins.base.plugin_base import BasePlugin


class SensorPlugin(BasePlugin):
    """ A sensor will be running on the target machine and monitor attacks. To remote control those sensors
    there are sensor plugins. This is the base class for them

    """

    # Boilerplate
    # name: Optional[str] = None

    # required_files: list[str] = []

    def __init__(self) -> None:
        super().__init__()  # pylint:disable=useless-super-delegation
        self.debugit = False

    def start(self) -> bool:  # pylint: disable=unused-argument, no-self-use
        """ Start the sensor. This is *optional* if your sensor is 'just collecting default OS logs' or something similar

        :returns: Currently, the return value is ignored. Set to True.
        """

        return True

    def stop(self) -> bool:  # pylint: disable=no-self-use
        """ Stop the sensor. This is *optional* if you do not have to stop the sensor before collecting

        :returns: Currently, the return value is ignored. Set to True.
        """

        return True

    def collect(self, path: str) -> list[str]:
        """ Collect data from the sensor. Copy it from sensor collection dir on target OS to the share.
        This step is essential: We want the data.

        :param path: The path to copy the data into
        :returns: A list of files to put into the loot zip
        """
        raise NotImplementedError

    def prime(self) -> bool:  # pylint: disable=no-self-use
        """ prime sets hard core configs in the target. You can use it to call everything that permanently alters the OS by settings.
        If your prime function returns True the machine will be rebooted after prime-ing it. This is very likely what you want. Only use prime if install is not sufficient.
        """

        return False

    def install(self) -> bool:  # pylint: disable=no-self-use
        """ Install the sensor. Executed on the target. Take the sensor from the share and (maybe) copy it to its destination. Do some setup
        """

        return True

    def __call_collect__(self, machine_path: str) -> list[str]:
        """ Generate the data collect command

        :meta private:

        @param machine_path: Machine specific path to collect data into
        """

        path = os.path.join(machine_path, "sensors", self.name)  # type: ignore
        os.makedirs(path)
        return self.collect(path)
