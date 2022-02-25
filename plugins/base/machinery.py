#!/usr/bin/env python3

""" Base class for classes to control any kind of machine: vm, bare metal, cloudified """

import os
from enum import Enum
from typing import Optional, Any

from app.config import MachineConfig
from app.exceptions import ConfigurationError
from app.interface_sfx import CommandlineColors
from plugins.base.plugin_base import BasePlugin


class MachineStates(Enum):
    """ Potential machine states """
    # TODO: maybe move state handling functions in here like "is running", "is broken"
    RUNNING = 1
    NOT_CREATED = 2
    POWEROFF = 3
    ABORTED = 4
    SAVED = 5
    STOPPED = 6
    FROZEN = 7
    SHUTOFF = 8


class MachineryPlugin(BasePlugin):
    """ Class to control virtual machines, vagrant, .... """

    # Boilerplate
    # name: Optional[str] = None

    # required_files: list[str] = []

    ###############
    # This is stuff you might want to implement

    def __init__(self) -> None:
        super().__init__()
        self.connection = None  # Connection
        self.config: Optional[MachineConfig] = None

    def create(self, reboot: bool = True) -> None:
        """ Create a machine

        @param reboot: Reboot the machine after creation
        """
        raise NotImplementedError

    def up(self) -> None:  # pylint: disable=invalid-name
        """ Start a machine, create it if it does not exist """
        raise NotImplementedError

    def halt(self) -> None:
        """ Halt a machine """
        raise NotImplementedError

    def destroy(self) -> None:
        """ Destroy a machine """
        raise NotImplementedError

    def connect(self) -> Any:
        """ Connect to a machine

        If you want to use SSH, check out the class SSHFeatures, it is already implemented there

        """
        raise NotImplementedError

    def remote_run(self, cmd: str, disown: bool = False) -> str:
        """ Connects to the machine and runs a command there

        If you want to use SSH, check out the class SSHFeatures, it is already implemented there

        :param cmd: command to run int he machine's shell
        :param disown: Send the connection into background
        :returns: the results as string
        """

        raise NotImplementedError

    def disconnect(self) -> None:
        """ Disconnect from a machine

        If you want to use SSH, check out the class SSHFeatures, it is already implemented there

        """
        raise NotImplementedError

    def put(self, src: str, dst: str) -> Any:
        """ Send a file to a machine

        If you want to use SSH, check out the class SSHFeatures, it is already implemented there

        :param src: source dir
        :param dst: destination
        """
        raise NotImplementedError

    def get(self, src: str, dst: str) -> Any:
        """ Get a file to a machine

        If you want to use SSH, check out the class SSHFeatures, it is already implemented there

        :param src: source dir
        :param dst: destination
        """
        raise NotImplementedError

    def is_running(self) -> bool:
        """ Returns if the machine is running """
        return self.get_state() == MachineStates.RUNNING

    def get_state(self) -> MachineStates:
        """ Get detailed state of a machine """
        raise NotImplementedError

    def get_ip(self) -> str:
        """ Return the IP of the machine.
            If there are several it should be the one accepting ssh or similar. If a resolver is running, a machine name is also ok as return value.

            :returns: machine name or ip. Some handle we can use to get a network connection to this machine
            """
        raise NotImplementedError

    def get_paw(self) -> str:
        """ Returns the paw of the current machine """
        if self.config is None:
            raise ConfigurationError
        paw = self.config.caldera_paw()
        if paw is None:
            raise ConfigurationError
        return paw

    def get_group(self) -> str:
        """ Returns the group of the current machine """
        if self.config is None:
            raise ConfigurationError
        group = self.config.caldera_group()
        if group is None:
            raise ConfigurationError
        return group

    def get_os(self) -> str:
        """ Returns the OS of the machine """
        if self.config is None:
            raise ConfigurationError
        the_os = self.config.os()
        if the_os is None:
            raise ConfigurationError
        return the_os

    def get_playground(self) -> Optional[str]:
        """ Path on the machine  where all the attack tools will be copied to. """
        if self.config is None:
            raise ConfigurationError

        return self.config.get_playground()

    def get_vm_name(self) -> str:
        """ Get the specific name of the machine

        @returns: the machine name
        """

        if self.config is None:
            raise ConfigurationError

        return self.config.vmname()

    def get_machine_path_internal(self) -> str:
        """ The vm internal path for all the data """

        # Maybe we do not need that ! playground should replace it

        raise NotImplementedError

    def get_machine_path_external(self) -> str:
        """  The path on the controlling host where vm specific data is stored """

        if self.config is None:
            raise ConfigurationError

        return os.path.join(self.config.vagrantfilepath(), self.config.machinepath())

    ###############
    # This is the interface from the main code to the plugin system. Do not touch
    def __call_halt__(self) -> None:
        """ Wrapper around halt """

        if self.config is None:
            raise ConfigurationError

        self.vprint(f"{CommandlineColors.OKBLUE}Stopping machine: {self.config.vmname()} {CommandlineColors.ENDC}", 1)
        self.halt()
        self.vprint(f"{CommandlineColors.OKGREEN}Machine stopped: {self.config.vmname()}{CommandlineColors.ENDC}", 1)

    def __call_process_config__(self, config: MachineConfig) -> None:
        """ Wrapper around process_config  """

        # print("===========> Processing config")
        self.config = config
        self.process_config(config.raw_config.__dict__)

    def __call_remote_run__(self, cmd: str, disown: bool = False) -> str:
        """ Simplifies connect and run

        @param cmd: Command to run as shell command
        @param disown: run in background
        """

        return self.remote_run(cmd, disown)

    def __call_disconnect__(self) -> None:
        """ Command connection dis-connect """

        self.disconnect()

    def __call_connect__(self) -> None:
        """ command connection. establish it """

        return self.connect()

    def __call_up__(self) -> None:
        """ Starts a VM. Creates it if not already created """

        self.up()

    def __call_create__(self, reboot: bool = True) -> None:
        """ Create a VM

        @param reboot: Reboot the VM during installation. Required if you want to install software
        """

        self.create(reboot)

    def __call_destroy__(self) -> None:
        """ Destroys the current machine """

        self.destroy()
