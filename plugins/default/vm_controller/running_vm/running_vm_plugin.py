#!/usr/bin/env python3

# A plugin to control already running vms

import os
from plugins.base.machinery import MachineryPlugin, MachineStates
from fabric import Connection
from app.exceptions import ConfigurationError, NetworkError
from invoke.exceptions import UnexpectedExit
import paramiko
import time
import socket


class RunningVMPlugin(MachineryPlugin):

    # Boilerplate
    name = "running_vm"
    description = "A plugin to handle already running machines. The machine will not be started/stopped by this plugin"

    required_files = []    # Files shipped with the plugin which are needed by the machine. Will be copied to the share

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__
        self.c = None
        self.vagrantfilepath = None
        self.vagrantfile = None

    def process_config(self, config):
        """ Machine specific processing of configuration """

        # TODO: Rename vagrantfilepath in the whole project
        # TODO: Is this a copy&paste artefact ?
        self.vagrantfilepath = os.path.abspath(self.config.vagrantfilepath())
        self.vagrantfile = os.path.join(self.vagrantfilepath, "Vagrantfile")
        if not os.path.isfile(self.vagrantfile):
            raise ConfigurationError(f"Vagrantfile not existing: {self.vagrantfile}")

    def create(self, reboot=True):
        """ Create a machine

        @param reboot: Reboot the VM during installation. Required if you want to install software
        """
        return

    def up(self):
        """ Start a machine, create it if it does not exist """
        return

    def halt(self):
        """ Halt a machine """
        return

    def destroy(self):
        """ Destroy a machine """
        return

    def connect(self):
        """ Connect to a machine """

        if self.c:
            return self.c

        retries = 10
        retry_sleep = 10
        timeout = 30
        while retries:
            try:
                if self.config.os() == "linux":
                    uhp = self.get_ip()
                    print(f"Connecting to {uhp}")
                    self.c = Connection(uhp, connect_timeout=timeout)

                if self.config.os() == "windows":
                    args = {}
                    # args = {"key_filename": self.config.ssh_keyfile() or self.v.keyfile(vm_name=self.config.vmname())}
                    if self.config.ssh_keyfile():
                        args["key_filename"] = self.config.ssh_keyfile()
                    if self.config.ssh_password():
                        args["password"] = self.config.ssh_password()
                    uhp = self.get_ip()
                    self.c = Connection(uhp, connect_timeout=timeout, user=self.config.ssh_user(), connect_kwargs=args)
            except (paramiko.ssh_exception.SSHException, socket.timeout):
                print(f"Failed to connect, will retry {retries} times. Timeout: {timeout}")
                retries -= 1
                timeout += 10
                time.sleep(retry_sleep)
            else:
                print(f"Connection: {self.c}")
                return self.c

        print("SSH network error")
        raise NetworkError

    def remote_run(self, cmd, disown=False):
        """ Connects to the machine and runs a command there

        @param disown: Send the connection into background
        """

        if cmd is None:
            return ""

        self.connect()
        cmd = cmd.strip()

        print("Running VM plugin remote run: " + cmd)
        print("Disown: " + str(disown))
        result = None
        retry = 2
        while retry > 0:
            try:
                result = self.c.run(cmd, disown=disown)
                print(result)
            except (paramiko.ssh_exception.NoValidConnectionsError, UnexpectedExit, paramiko.ssh_exception.SSHException):
                if retry <= 0:
                    raise NetworkError
                else:
                    self.disconnect()
                    self.connect()
                    retry -= 1
                    print("Got some SSH errors. Retrying")
            else:
                break

        if result and result.stderr:
            print("Debug: Stderr: " + str(result.stderr.strip()))

        if result:
            return result.stdout.strip()

        return ""

    def put(self, src, dst):
        """ Send a file to a machine

        @param src: source dir
        @param dst: destination
        """
        self.connect()

        print(f"PUT {src} -> {dst}")

        res = ""
        retries = 10
        retry_sleep = 10
        timeout = 30
        while retries:
            try:
                res = self.c.put(src, dst)
            except (paramiko.ssh_exception.SSHException, socket.timeout, UnexpectedExit):
                print(f"PUT Failed to connect, will retry {retries} times. Timeout: {timeout}")
                retries -= 1
                timeout += 10
                time.sleep(retry_sleep)
                self.disconnect()
                self.connect()
            else:
                return res
        print("SSH network error on PUT command")
        raise NetworkError

    def get(self, src, dst):
        """ Get a file to a machine

        @param src: source dir
        @param dst: destination
        """
        self.connect()

        retry = 2
        while retry > 0:
            try:
                res = self.c.get(src, dst)
            except (paramiko.ssh_exception.NoValidConnectionsError, UnexpectedExit):
                if retry <= 0:
                    raise NetworkError
                else:
                    self.disconnect()
                    self.connect()
                    retry -= 1
                    print("Got some SSH errors. Retrying")
            except FileNotFoundError as e:
                print(e)
                break
            else:
                break

        return res

    def disconnect(self):
        """ Disconnect from a machine """
        if self.c:
            self.c.close()
            self.c = None

    def get_state(self):
        """ Get detailed state of a machine """

        return MachineStates.RUNNING

    def get_ip(self):
        """ Return the machine ip """

        return self.config.vm_ip()
