#!/usr/bin/env python3

""" Base class for classes to control any kind of machine: vm, bare metal, cloudified """

from enum import Enum

from app.config import MachineConfig
from app.interface_sfx import CommandlineColors
from plugins.base.plugin_base import BasePlugin
import os


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
    name = None

    required_files = []

    ###############
    # This is stuff you might want to implement

    def __init__(self):
        super().__init__()
        self.connection = None  # Connection
        self.config = None

    def create(self, reboot=True):
        """ Create a machine

        @param reboot: Optionally reboot the machine after creation
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
        """ Connect to a machine """
        raise NotImplementedError

    def remote_run(self, cmd, disown=False):
        """ Connects to the machine and runs a command there


        @param cmd: command to run int he machine's shell
        @param disown: Send the connection into background
        """

        raise NotImplementedError

    def disconnect(self):
        """ Disconnect from a machine """
        raise NotImplementedError

    def put(self, src, dst):
        """ Send a file to a machine

        @param src: source dir
        @param dst: destination
        """
        raise NotImplementedError

    def get(self, src, dst):
        """ Get a file to a machine

        @param src: source dir
        @param dst: destination
        """
        raise NotImplementedError

    def is_running(self):
        """ Returns if the machine is running """
        return self.get_state() == MachineStates.RUNNING

    def get_state(self):
        """ Get detailed state of a machine """
        raise NotImplementedError

    def get_ip(self):
        """ Return the IP of the machine. If there are several it should be the one accepting ssh or similar. If a resolver is running, a domain is also ok. """
        raise NotImplementedError

    def get_playground(self):
        """ Path on the machine  where all the attack tools will be copied to. """

        return self.config.get_playground()

    def get_vm_name(self):
        """ Get the specific name of the machine """

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
        self.process_config(config.raw_config)

    def __call_remote_run__(self, cmd, disown=False):
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

    def __call_create__(self, reboot=True):
        """ Create a VM

        @param reboot: Reboot the VM during installation. Required if you want to install software
        """

        self.create(reboot)

    def __call_destroy__(self):
        """ Destroys the current machine """

        self.destroy()
