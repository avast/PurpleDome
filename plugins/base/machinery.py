#!/usr/bin/env python3

""" Base class for classes to control any kind of machine: vm, bare metal, cloudified """

from enum import Enum
import os
# from typing import Optional
from app.config import MachineConfig
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

    def __init__(self):
        super().__init__()
        self.connection = None  # Connection
        self.config = None

    def create(self, reboot: bool = True):
        """ Create a machine

        @param reboot: Reboot the machine after creation
        """
        raise NotImplementedError

    def up(self):  # pylint: disable=invalid-name
        """ Start a machine, create it if it does not exist """
        raise NotImplementedError

    def halt(self):
        """ Halt a machine """
        raise NotImplementedError

    def destroy(self):
        """ Destroy a machine """
        raise NotImplementedError

    def connect(self):
        """ Connect to a machine

        If you want to use SSH, check out the class SSHFeatures, it is already implemented there

        """
        raise NotImplementedError

    def remote_run(self, cmd: str, disown: bool = False):
        """ Connects to the machine and runs a command there

        If you want to use SSH, check out the class SSHFeatures, it is already implemented there

        :param cmd: command to run int he machine's shell
        :param disown: Send the connection into background
        """

        raise NotImplementedError

    def disconnect(self):
        """ Disconnect from a machine

        If you want to use SSH, check out the class SSHFeatures, it is already implemented there

        """
        raise NotImplementedError

    def put(self, src: str, dst: str):
        """ Send a file to a machine

        If you want to use SSH, check out the class SSHFeatures, it is already implemented there

        :param src: source dir
        :param dst: destination
        """
        raise NotImplementedError

    def get(self, src: str, dst: str):
        """ Get a file to a machine

        If you want to use SSH, check out the class SSHFeatures, it is already implemented there

        :param src: source dir
        :param dst: destination
        """
        raise NotImplementedError

    def is_running(self):
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

    def get_paw(self):
        """ Returns the paw of the current machine """
        return self.config.caldera_paw()

    def get_group(self):
        """ Returns the group of the current machine """
        return self.config.caldera_group()

    def get_os(self):
        """ Returns the OS of the machine """

        return self.config.os()

    def get_playground(self):
        """ Path on the machine  where all the attack tools will be copied to. """

        return self.config.get_playground()

    def get_vm_name(self) -> str:
        """ Get the specific name of the machine

        @returns: the machine name
        """

        return self.config.vmname()

    def get_machine_path_internal(self):
        """ The vm internal path for all the data """

        # Maybe we do not need that ! playground should replace it

        raise NotImplementedError

    def get_machine_path_external(self):
        """  The path on the controlling host where vm specific data is stored """
        return os.path.join(self.config.vagrantfilepath(), self.config.machinepath())

    ###############
    # This is the interface from the main code to the plugin system. Do not touch
    def __call_halt__(self):
        """ Wrapper around halt """

        self.vprint(f"{CommandlineColors.OKBLUE}Stopping machine: {self.config.vmname()} {CommandlineColors.ENDC}", 1)
        self.halt()
        self.vprint(f"{CommandlineColors.OKGREEN}Machine stopped: {self.config.vmname()}{CommandlineColors.ENDC}", 1)

    def __call_process_config__(self, config: MachineConfig):
        """ Wrapper around process_config  """

        # print("===========> Processing config")
        self.config = config
        self.process_config(config.raw_config.__dict__)

    def __call_remote_run__(self, cmd: str, disown: bool = False):
        """ Simplifies connect and run

        @param cmd: Command to run as shell command
        @param disown: run in background
        """

        return self.remote_run(cmd, disown)

    def __call_disconnect__(self):
        """ Command connection dis-connect """

        self.disconnect()

    def __call_connect__(self):
        """ command connection. establish it """

        return self.connect()

    def __call_up__(self):
        """ Starts a VM. Creates it if not already created """

        self.up()

    def __call_create__(self, reboot: bool = True):
        """ Create a VM

        @param reboot: Reboot the VM during installation. Required if you want to install software
        """

        self.create(reboot)

    def __call_destroy__(self):
        """ Destroys the current machine """

        self.destroy()
