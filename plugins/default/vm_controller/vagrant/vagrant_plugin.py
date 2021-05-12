#!/usr/bin/env python3

# A plugin to control vagrant machines

from plugins.base.machinery import MachineryPlugin, MachineStates
import subprocess
import vagrant
from fabric import Connection
import os
from app.exceptions import ConfigurationError
# from app.exceptions import NetworkError
# from invoke.exceptions import UnexpectedExit
# import paramiko
from plugins.base.ssh_features import SSHFeatures

# Experiment with paramiko instead of fabric. Seems fabric has some issues with the "put" command to Windows. There seems no fix (just my workarounds). Maybe paramiko is better.


class VagrantPlugin(SSHFeatures, MachineryPlugin):

    # Boilerplate
    name = "vagrant"
    description = "A plugin for vagrant machines"

    required_files = []    # Files shipped with the plugin which are needed by the machine. Will be copied to the share

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__
        self.v = None
        self.c = None
        self.vagrantfilepath = None
        self.vagrantfile = None
        self.sysconf = {}

    def process_config(self, config):
        """ Machine specific processing of configuration """
        super().process_config(config)

        self.vagrantfilepath = os.path.abspath(self.config.vagrantfilepath())
        self.vagrantfile = os.path.join(self.vagrantfilepath, "Vagrantfile")
        if not os.path.isfile(self.vagrantfile):
            raise ConfigurationError(f"Vagrantfile not existing: {self.vagrantfile}")
        self.v = vagrant.Vagrant(root=self.vagrantfilepath)

    def create(self, reboot=True):
        """ Create a machine

        @param reboot: Reboot the VM during installation. Required if you want to install software
        """
        self.up()
        if reboot:
            self.halt()
            self.up()

    def up(self):
        """ Start a machine, create it if it does not exist """
        try:
            self.v.up(vm_name=self.config.vmname())
        except subprocess.CalledProcessError as e:
            if self.v.status(vm_name=self.config.vmname())[0].state == self.v.RUNNING:
                return  # Everything is fine
            else:
                raise e

    def halt(self):
        """ Halt a machine """
        forceit = self.config.halt_needs_force()
        try:
            self.v.halt(vm_name=self.config.vmname(), force=forceit)
        except subprocess.CalledProcessError:
            self.v.halt(vm_name=self.config.vmname(), force=True)

    def destroy(self):
        """ Destroy a machine """
        self.v.destroy(vm_name=self.config.vmname())

    def connect(self):
        """ Connect to a machine. If there is already a connection we keep it """

        # For linux we are using Vagrant style
        if self.config.os() == "linux":
            if self.c:
                return self.c

            uhp = self.v.user_hostname_port(vm_name=self.config.vmname())
            self.vprint(f"Connecting to {uhp}", 3)
            self.c = Connection(uhp, connect_kwargs={"key_filename": self.v.keyfile(vm_name=self.config.vmname())})
            return self.c

        else:
            return super().connect()

        # if self.config.os() == "linux":
        #     super

        # if self.config.os() == "windows":
        #     args = {"key_filename": os.path.join(self.sysconf["abs_machinepath_external"], self.config.ssh_keyfile())}
        #     if self.config.ssh_password():
        #         args["password"] = self.config.ssh_password()
        #     uhp = self.get_ip()
        #     print(uhp)
        #     print(args)
        #     print(self.config.ssh_user())
        #     self.c = Connection(uhp, user=self.config.ssh_user(), connect_kwargs=args)
        #     print(self.c)
        #     return self.c

    def get_state(self):
        """ Get detailed state of a machine """

        vstate = self.v.status(vm_name=self.config.vmname())[0].state

        # mapping vagrant states to PurpleDome states
        mapping = {self.v.RUNNING: MachineStates.RUNNING,
                   self.v.NOT_CREATED: MachineStates.NOT_CREATED,
                   self.v.POWEROFF: MachineStates.POWEROFF,
                   self.v.ABORTED: MachineStates.ABORTED,
                   self.v.SAVED: MachineStates.SAVED,
                   self.v.STOPPED: MachineStates.STOPPED,
                   self.v.FROZEN: MachineStates.FROZEN,
                   self.v.SHUTOFF: MachineStates.SHUTOFF
                   }

        return mapping[vstate]

    def get_ip(self):
        """ Return the machine ip """

        # TODO: Create special code to extract windows IPs

        # TODO: Find a smarter way to get the ip

        # ips = []
        # cmd = "ifconfig"
        # res = self.vm_manager.__call_remote_run__(cmd)

        # for line in res.split("\n"):
        #     m = re.match(r".*inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*", line)
        #     if m:
        #         print(m.group(1))
        #         ips.append(m.group(1))

        filename = os.path.join(self.sysconf["abs_machinepath_external"], "ip4.txt")
        with open(filename, "rt") as fh:
            return fh.readline().strip()
