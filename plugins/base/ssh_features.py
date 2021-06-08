#!/usr/bin/env python3
""" A class you can use to add SSH features to you plugin. Useful for vm_controller/machinery classes """
import os.path

from fabric import Connection
from app.exceptions import NetworkError
from invoke.exceptions import UnexpectedExit
import paramiko
import time
import socket
from plugins.base.plugin_base import BasePlugin


class SSHFeatures(BasePlugin):

    def __init__(self):
        super().__init__()
        self.c = None

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
                    self.vprint(f"Connecting to {uhp}", 3)
                    self.c = Connection(uhp, connect_timeout=timeout)

                if self.config.os() == "windows":
                    args = {}
                    # args = {"key_filename": self.config.ssh_keyfile() or self.v.keyfile(vm_name=self.config.vmname())}
                    if self.config.ssh_keyfile():
                        args["key_filename"] = self.config.ssh_keyfile()
                    if self.config.ssh_password():
                        args["password"] = self.config.ssh_password()
                    self.vprint(args, 3)
                    uhp = self.get_ip()
                    self.vprint(uhp, 3)
                    self.c = Connection(uhp, connect_timeout=timeout, user=self.config.ssh_user(), connect_kwargs=args)
            except (paramiko.ssh_exception.SSHException, socket.timeout):
                self.vprint(f"Failed to connect, will retry {retries} times. Timeout: {timeout}", 0)
                retries -= 1
                timeout += 10
                time.sleep(retry_sleep)
            else:
                self.vprint(f"Connection: {self.c}", 3)
                return self.c

        self.vprint("SSH network error", 0)
        raise NetworkError

    def remote_run(self, cmd, disown=False):
        """ Connects to the machine and runs a command there

        @param cmd: The command to execute
        @param disown: Send the connection into background
        """

        if cmd is None:
            return ""

        self.connect()
        cmd = cmd.strip()

        self.vprint("Running SSH remote run: " + cmd, 3)
        self.vprint("Disown: " + str(disown), 3)
        result = None
        retry = 2
        while retry > 0:
            try:
                result = self.c.run(cmd, disown=disown)
                print(result)
                # paramiko.ssh_exception.SSHException in the next line is needed for windows openssh
            except (paramiko.ssh_exception.NoValidConnectionsError, UnexpectedExit, paramiko.ssh_exception.SSHException):
                if retry <= 0:
                    raise NetworkError
                else:
                    self.disconnect()
                    self.connect()
                    retry -= 1
                    self.vprint("Got some SSH errors. Retrying", 2)
            else:
                break

        if result and result.stderr:
            self.vprint("Debug: Stderr: " + str(result.stderr.strip()), 0)

        if result:
            return result.stdout.strip()

        return ""

    def put(self, src, dst):
        """ Send a file to a machine

        @param src: source dir
        @param dst: destination
        """
        self.connect()

        self.vprint(f"PUT {src} -> {dst}", 3)

        res = ""
        retries = 10
        retry_sleep = 10
        timeout = 30
        while retries:
            try:
                res = self.c.put(src, dst)
            except (paramiko.ssh_exception.SSHException, socket.timeout, UnexpectedExit):
                self.vprint(f"PUT Failed to connect, will retry {retries} times. Timeout: {timeout}", 3)
                retries -= 1
                timeout += 10
                time.sleep(retry_sleep)
                self.disconnect()
                self.connect()
            except FileNotFoundError as e:
                self.vprint(f"File not found: {e}", 0)
                break
            else:
                return res
        self.vprint("SSH network error on PUT command", 0)
        raise NetworkError

    def get(self, src, dst):
        """ Get a file to a machine

        @param src: source dir
        @param dst: destination
        """
        self.connect()

        if os.path.isdir(dst):
            dst = os.path.join(dst, os.path.basename(src))

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
                    self.vprint("Got some SSH errors. Retrying", 2)
            except FileNotFoundError as e:
                self.vprint(e, 0)
                break
            else:
                break

        return res

    def disconnect(self):
        """ Disconnect from a machine """
        if self.c:
            self.c.close()
            self.c = None
