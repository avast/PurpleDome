#!/usr/bin/env python3
""" A class you can use to add SSH features to you plugin. Useful for vm_controller/machinery classes """
import os.path
import socket
import time
from typing import Any, Optional

import paramiko
from fabric import Connection  # type: ignore
from invoke.exceptions import UnexpectedExit  # type: ignore

from app.exceptions import ConfigurationError, SSHError
from app.config import MachineConfig
from app.exceptions import NetworkError
from plugins.base.plugin_base import BasePlugin


class SSHFeatures(BasePlugin):
    """ A Mixin class to add SSH features to all kind of VM machinery """

    def __init__(self) -> None:
        self.config: Optional[MachineConfig] = None
        super().__init__()
        self.connection = None

    def get_ip(self) -> str:
        """ Get the IP of a machine, must be overwritten in the machinery class """
        raise NotImplementedError

    def connect(self) -> Connection:
        """ Connect to a machine """

        if self.connection is not None:
            return self.connection

        if self.config is None:
            raise ConfigurationError("Missing config")

        retries = 10
        retry_sleep = 10
        timeout = 30
        while retries:
            try:
                if self.config.os() == "linux":
                    uhp = self.get_ip()
                    self.vprint(f"SSH connecting to {uhp}", 3)
                    self.connection = Connection(uhp, connect_timeout=timeout)

                if self.config.os() == "windows":
                    args = {}
                    # args = {"key_filename": self.config.ssh_keyfile() or self.v.keyfile(vm_name=self.config.vmname())}
                    if self.config.ssh_keyfile():
                        args["key_filename"] = self.config.ssh_keyfile()
                    if self.config.ssh_password():
                        args["password"] = self.config.ssh_password()
                    self.vprint(str(args), 3)
                    uhp = self.get_ip()
                    self.vprint(f"IP to connect to: {uhp}", 3)
                    self.connection = Connection(uhp, connect_timeout=timeout, user=self.config.ssh_user(), connect_kwargs=args)
            except (paramiko.ssh_exception.SSHException, socket.timeout):
                self.vprint(f"Failed to connect, will retry {retries} times. Timeout: {timeout}", 0)
                retries -= 1
                timeout += 10
                time.sleep(retry_sleep)
            else:
                self.vprint(f"Connection: {self.connection}", 3)
                return self.connection

        self.vprint("SSH network error", 0)
        raise NetworkError

    def remote_run(self, cmd: str, disown: bool = False, must_succeed: bool = False) -> str:
        """ Connects to the machine and runs a command there

        :param cmd: The command to execute
        :param disown: Send the connection into background
        :param must_succeed: Throw an exception if the command being run fails.
        :returns: The results as string
        """

        if cmd is None:
            return ""

        self.connect()
        cmd = cmd.strip()

        self.vprint("Running SSH remote run: " + cmd, 3)
        self.vprint("Disown: " + str(disown), 3)
        # self.vprint("Connection: " + self.connection, 1)
        result = None
        retry = 10
        while retry >= 0:
            do_retry = False
            try:
                print(f"Running cmd {cmd}")
                if self.connection is None:
                    raise SSHError("Connection broken")
                result = self.connection.run(cmd, disown=disown)
                print(result)
                # paramiko.ssh_exception.SSHException in the next line is needed for windows openssh
            except (paramiko.ssh_exception.NoValidConnectionsError, paramiko.ssh_exception.SSHException) as error:
                if retry <= 0:
                    raise NetworkError from error
                do_retry = True
            except UnexpectedExit as error:
                if must_succeed:
                    if retry <= 0:
                        raise NetworkError from error
                    do_retry = True
                else:
                    # breakpoint()
                    break
            except Exception as error:
                raise NetworkError from error
            if do_retry:
                time.sleep(5)
                self.disconnect()
                time.sleep(5)
                self.connect()
                retry -= 1
                self.vprint(f"Got some SSH errors. Retrying {retry}", 2)
            else:
                break

        if result and result.stderr:
            self.vprint("Debug: Stderr: " + str(result.stderr.strip()), 0)
            return result.stderr.strip()

        if result:
            return result.stdout.strip()

        return ""

    def put(self, src: str, dst: Optional[str]) -> Any:
        """ Send a file to a machine

        :param src: source dir
        :param dst: destination
        """
        self.connect()

        self.vprint(f"PUT {src} -> {dst}", 3)

        res = ""
        retries = 10
        retry_sleep = 10
        timeout = 30
        while retries > 0:
            do_retry = False
            try:
                if self.connection is None:
                    raise SSHError("Connection broken")
                res = self.connection.put(src, dst)
            except (paramiko.ssh_exception.SSHException, socket.timeout, UnexpectedExit):
                self.vprint("SSH PUT: Failed to connect", 1)
                do_retry = True
            except paramiko.ssh_exception.NoValidConnectionsError as error:
                self.vprint(f"SSH PUT: No valid connection. Errors: {error.errors}", 1)
                do_retry = True
            except FileNotFoundError as error:
                self.vprint(f"SSH PUT: File not found: {error}", 0)
                break
            except OSError:
                self.vprint("SSH PUT: Obscure OSError, ignoring (file should have been copied)", 1)
                # do_retry = True
                # breakpoint()

            if do_retry:
                self.vprint(f"SSH PUT: Will retry {retries} times. Timeout: {timeout}", 3)
                retries -= 1
                timeout += 10
                time.sleep(retry_sleep)
                self.disconnect()
                self.connect()
            else:
                return res
        self.vprint("SSH network error on PUT command", 0)
        raise NetworkError

    def get(self, src: str, dst: str) -> Any:
        """ Get a file to a machine

        :param src: source dir
        :param dst: destination
        """
        self.connect()
        res = None

        if os.path.isdir(dst):
            dst = os.path.join(dst, os.path.basename(src))

        retry = 2
        while retry > 0:
            do_retry = False
            try:
                if self.connection is None:
                    raise SSHError("Connection broken")
                res = self.connection.get(src, dst)
            except (UnexpectedExit) as error:
                if retry <= 0:
                    raise NetworkError from error
                do_retry = True
            except paramiko.ssh_exception.NoValidConnectionsError as error:
                self.vprint(f"SSH GET: No valid connection. Errors: {error.errors}", 1)
                do_retry = True
            except FileNotFoundError as error:
                self.vprint(str(error), 0)
                break
            except OSError:
                self.vprint("SSH GET: Obscure OSError, ignoring (file should have been copied)", 1)
                # do_retry = True
            if do_retry:
                self.disconnect()
                self.connect()
                retry -= 1
                self.vprint("Got some SSH errors. Retrying", 2)
            else:
                break

        return res

    def disconnect(self) -> None:
        """ Disconnect from a machine """
        if self.connection:
            self.connection.close()
            self.connection = None
