#!/usr/bin/env python3

""" A class to control a whole experiment. From setting up the machines to running the attacks """

import os
import subprocess
import time
import zipfile
import shutil
from datetime import datetime
from typing import Optional

from app.attack_log import AttackLog
from app.config import ExperimentConfig
from app.interface_sfx import CommandlineColors
from app.exceptions import ServerError
from app.pluginmanager import PluginManager
from app.doc_generator import DocGenerator
from app.calderacontrol import CalderaControl
from app.machinecontrol import Machine
from plugins.base.attack import AttackPlugin


# TODO: Multi threading at least when starting machines

class Experiment():
    """ Class handling experiments """

    def __init__(self, configfile: str, verbosity=0):
        """

        :param configfile: Path to the configfile to load
        :param verbosity: verbosity level between 0 and 3
        """
        self.start_time: Optional[datetime] = None  #: time the experiment started
        self.caldera_control: Optional[CalderaControl] = None
        self.loot_dir: Optional[str] = None
        self.targets = []

        self.attacker_1: Optional[Machine] = None

        self.experiment_config = ExperimentConfig(configfile)
        self.attack_logger = AttackLog(verbosity)
        self.plugin_manager = PluginManager(self.attack_logger)

    def run(self, caldera_attacks: list = None):
        """
        Run the experiment

        :param caldera_attacks: an optional argument to override caldera attacks in the config file and run just this one caldera attack. A list of caldera ID
        :return:
        """
        self.__start_attacker()

        caldera_url = "http://" + self.attacker_1.get_ip() + ":8888"
        self.caldera_control = CalderaControl(caldera_url, attack_logger=self.attack_logger, config=self.experiment_config)
        # self.caldera_control = CalderaControl("http://" + self.attacker_1.get_ip() + ":8888", self.attack_logger,
        #                                     config=self.experiment_config)
        # Deleting all currently registered Caldera gents
        self.attack_logger.vprint(self.caldera_control.kill_all_agents(), 3)
        self.attack_logger.vprint(self.caldera_control.delete_all_agents(), 3)

        self.start_time = datetime.now().strftime("%Y_%m_%d___%H_%M_%S")
        self.loot_dir = os.path.join(self.experiment_config.loot_dir(), self.start_time)
        os.makedirs(self.loot_dir)

        # start target machines
        tname = self.start_target_machines(caldera_attacks)

        # Install vulnerabilities
        self.install_vulnerabilities()

        # Install sensor plugins
        self.install_sensor_plugins()

        # First start of caldera implants
        self.first_start_of_caldera_implants(caldera_attacks, tname)

        self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Contacting caldera agents on all targets ....{CommandlineColors.ENDC}", 1)
        # Wait until all targets are registered as Caldera targets
        self.wait_until_all_targets_have_caldera_implants(caldera_attacks, caldera_url)
        self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}Caldera agents reached{CommandlineColors.ENDC}", 1)

        # Add running machines to log
        self.add_running_machines_to_log()

        # Attack them
        self.run_caldera_attacks(caldera_attacks)

        # Run plugin based attacks
        self.run_plugin_attacks()

        # Stop sensor plugins
        # Collect data
        zip_this = []
        for a_target in self.targets:
            a_target.stop_sensors()
            zip_this += a_target.collect_sensors(self.loot_dir)

        # Uninstall vulnerabilities
        for a_target in self.targets:
            self.attack_logger.vprint(f"{CommandlineColors.OKBLUE} Uninstalling vulnerabilities on {a_target.get_paw()} {CommandlineColors.ENDC}", 1)
            a_target.stop_vulnerabilities()
            self.attack_logger.vprint(f"{CommandlineColors.OKGREEN} Done uninstalling vulnerabilities on {a_target.get_paw()} {CommandlineColors.ENDC}", 1)

        # Stop target machines
        for target_1 in self.targets:
            target_1.halt()
        self.__stop_attacker()

        self.attack_logger.post_process()
        attack_log_file_path = os.path.join(self.loot_dir, "attack.json")
        self.attack_logger.write_json(attack_log_file_path)
        document_generator = DocGenerator()
        document_generator.generate(attack_log_file_path)
        document_generator.compile_documentation()
        zip_this += document_generator.get_outfile_paths()
        self.zip_loot(zip_this)

    def run_plugin_attacks(self):
        self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Running attack plugins{CommandlineColors.ENDC}", 1)
        for target_1 in self.targets:
            plugin_based_attacks = self.experiment_config.get_plugin_based_attacks(target_1.get_os())
            metasploit_plugins = self.plugin_manager.count_caldera_requirements(AttackPlugin, plugin_based_attacks)
            print(f"Plugins needing metasploit for {target_1.get_paw()} : {metasploit_plugins}")
            for attack in plugin_based_attacks:
                # TODO: Work with snapshots
                self.attack_logger.vprint(f"Attacking machine with PAW: {target_1.get_paw()} with attack: {attack}", 1)

                self.attack(target_1, attack)
                self.attack_logger.vprint(
                    f"Pausing before next attack (config: nap_time): {self.experiment_config.get_nap_time()}", 3)
                time.sleep(self.experiment_config.get_nap_time())
        self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}Finished attack plugins{CommandlineColors.ENDC}", 1)

    def run_caldera_attacks(self, caldera_attacks):
        self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Running Caldera attacks{CommandlineColors.ENDC}", 1)
        for target_1 in self.targets:
            if caldera_attacks is None:
                # Run caldera attacks
                new_caldera_attacks = self.experiment_config.get_caldera_attacks(target_1.get_os())
            else:
                new_caldera_attacks = caldera_attacks
            if new_caldera_attacks:
                for attack in new_caldera_attacks:
                    # TODO: Work with snapshots
                    # TODO: If we have several targets in the same group, it is nonsense to attack each one separately. Make this smarter
                    self.attack_logger.vprint(f"Attacking machine with PAW: {target_1.get_paw()} with {attack}", 2)

                    it_worked = self.caldera_control.attack(paw=target_1.get_paw(),
                                                            ability_id=attack,
                                                            group=target_1.get_group(),
                                                            target_platform=target_1.get_os()
                                                            )

                    # Moved to fix section below. If fix works: can be removed
                    # print(f"Pausing before next attack (config: nap_time): {self.experiment_config.get_nap_time()}")
                    # time.sleep(self.experiment_config.get_nap_time())

                    # Fix: Caldera sometimes gets stuck. This is why we better re-start the caldera server and wait till all the implants re-connected
                    # Reason: In some scenarios we keep the infra up for hours or days. No re-creation like intended. This can cause Caldera to hick up
                    if it_worked:
                        self.attack_logger.vprint(
                            f"{CommandlineColors.OKBLUE}Restarting caldera server and waiting for clients to re-connect{CommandlineColors.ENDC}",
                            1)
                        self.attacker_1.start_caldera_server()
                        self.attack_logger.vprint(
                            f"Pausing before next attack (config: nap_time): {self.experiment_config.get_nap_time()}",
                            2)
                        time.sleep(self.experiment_config.get_nap_time())
                        retries = 100
                        for target_system in self.targets:
                            if self.machine_needs_caldera(target_system, caldera_attacks) == 0:
                                self.attack_logger.vprint(f"No caldera agent needed for: {target_system.get_paw()} ", 3)
                                continue
                            running_agents = self.caldera_control.list_paws_of_running_agents()
                            self.attack_logger.vprint(f"Agents currently connected to the server: {running_agents}", 2)
                            while target_system.get_paw() not in running_agents:
                                time.sleep(1)
                                running_agents = self.caldera_control.list_paws_of_running_agents()
                                retries -= 1
                                self.attack_logger.vprint(
                                    f"Waiting for clients to re-connect ({retries}, {running_agents}) ", 3)
                                if retries <= 0:
                                    raise ServerError
                        self.attack_logger.vprint(
                            f"{CommandlineColors.OKGREEN}Restarted caldera server clients re-connected{CommandlineColors.ENDC}",
                            1)
                        # End of fix
        self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}Finished Caldera attacks{CommandlineColors.ENDC}", 1)

    def add_running_machines_to_log(self):
        for target in self.targets:
            i = target.get_machine_info()
            i["role"] = "target"
            self.attack_logger.add_machine_info(i)
        i = self.attacker_1.get_machine_info()
        i["role"] = "attacker"
        self.attack_logger.add_machine_info(i)

    def wait_until_all_targets_have_caldera_implants(self, caldera_attacks, caldera_url):
        for target_1 in self.targets:
            running_agents = self.caldera_control.list_paws_of_running_agents()
            self.attack_logger.vprint(f"Agents currently running: {running_agents}", 2)
            while target_1.get_paw() not in running_agents:
                if self.machine_needs_caldera(target_1, caldera_attacks) == 0:
                    self.attack_logger.vprint(f"No caldera agent needed for: {target_1.get_paw()} ", 3)
                    break
                self.attack_logger.vprint(f"Connecting to caldera {caldera_url}, running agents are: {running_agents}",
                                          3)
                self.attack_logger.vprint(f"Missing agent: {target_1.get_paw()} ...", 3)
                target_1.start_caldera_client()
                self.attack_logger.vprint(f"Restarted caldera agent: {target_1.get_paw()} ...", 3)
                time.sleep(120)  # Was 30, but maybe there are timing issues
                running_agents = self.caldera_control.list_paws_of_running_agents()

    def first_start_of_caldera_implants(self, caldera_attacks, tname):
        at_least_one_caldera_started = False
        for target_1 in self.targets:
            if self.machine_needs_caldera(target_1, caldera_attacks):
                target_1.start_caldera_client()
                self.attack_logger.vprint(
                    f"{CommandlineColors.OKGREEN}Initial start of caldera client: {tname}  {CommandlineColors.ENDC}", 1)
            else:
                at_least_one_caldera_started = True
        if at_least_one_caldera_started:
            time.sleep(20)  # Wait for all the clients to contact the caldera server
        # TODO: Smarter wait

    def install_sensor_plugins(self):
        for a_target in self.targets:
            self.attack_logger.vprint(f"Installing sensors on {a_target.get_paw()}", 2)
            a_target.install_sensors()
            a_target.start_sensors()

    def install_vulnerabilities(self):
        for a_target in self.targets:
            self.attack_logger.vprint(f"Installing vulnerabilities on {a_target.get_paw()}", 2)
            a_target.install_vulnerabilities()
            a_target.start_vulnerabilities()

    def start_target_machines(self, caldera_attacks):
        for target_conf in self.experiment_config.targets():
            if not target_conf.is_active():
                continue

            tname = target_conf.vmname()

            self.attack_logger.vprint(
                f"{CommandlineColors.OKBLUE}preparing target {tname} ....{CommandlineColors.ENDC}", 1)
            target_1 = Machine(target_conf, attack_logger=self.attack_logger)
            target_1.set_caldera_server(self.attacker_1.get_ip())
            try:
                if not target_conf.use_existing_machine():
                    target_1.destroy()
            except subprocess.CalledProcessError:
                # Maybe the machine just does not exist yet
                pass
            if self.machine_needs_caldera(target_1, caldera_attacks):
                target_1.install_caldera_service()
            target_1.up()
            target_1.reboot()  # Kernel changes on system creation require a reboot
            needs_reboot = target_1.prime_vulnerabilities()
            needs_reboot |= target_1.prime_sensors()
            if needs_reboot:
                self.attack_logger.vprint(
                    f"{CommandlineColors.OKBLUE}rebooting target {tname} ....{CommandlineColors.ENDC}", 1)
                target_1.reboot()
            self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}Target is up: {tname}  {CommandlineColors.ENDC}", 1)
            self.targets.append(target_1)
        return tname

    def machine_needs_caldera(self, target, caldera_conf):
        """ Counts the attacks and plugins needing caldera that are registered for this machine """

        c_cmdline = 0
        if caldera_conf is not None:
            c_cmdline = len(caldera_conf)
        c_conffile = len(self.experiment_config.get_caldera_attacks(target.get_os()))
        plugin_based_attacks = self.experiment_config.get_plugin_based_attacks(target.get_os())
        c_plugins = self.plugin_manager.count_caldera_requirements(AttackPlugin, plugin_based_attacks)

        print(f"Caldera count: From cmdline: {c_cmdline}, From conf: {c_conffile} from plugins: {c_plugins}")

        return c_cmdline + c_conffile + c_plugins

    def attack(self, target, attack):
        """ Pick an attack and run it

        :param attack: Name of the attack to run
        :param target: IP address of the target
        :returns: The output of the cmdline attacking tool
        """

        for plugin in self.plugin_manager.get_plugins(AttackPlugin, [attack]):
            name = plugin.get_name()

            self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Running Attack plugin {name}{CommandlineColors.ENDC}", 2)
            plugin.process_config(self.experiment_config.attack_conf(plugin.get_config_section_name()))
            plugin.set_attacker_machine(self.attacker_1)
            plugin.set_sysconf({})
            plugin.set_logger(self.attack_logger)
            plugin.set_caldera(self.caldera_control)
            plugin.connect_metasploit()
            plugin.install()

            # plugin.__set_logger__(self.attack_logger)
            plugin.__execute__([target])

    def zip_loot(self, zip_this):
        """ Zip the loot together """

        filename = os.path.join(self.loot_dir, self.start_time + ".zip")

        self.attack_logger.vprint(f"Creating zip file {filename}", 1)

        with zipfile.ZipFile(filename, "w") as zfh:
            for a_file in zip_this:
                if a_file != filename:
                    self.attack_logger.vprint(a_file, 2)
                    zfh.write(a_file)

            zfh.write(os.path.join(self.loot_dir, "attack.json"))

        # For automation purpose we copy the file into a standard file name
        defaultname = os.path.join(self.loot_dir, "..", "most_recent.zip")
        shutil.copyfile(filename, defaultname)

    def __start_attacker(self):
        """ Start the attacking VM """

        # Preparing attacker
        self.attacker_1 = Machine(self.experiment_config.attacker(0).raw_config, attack_logger=self.attack_logger)

        if self.attacker_1 is None:
            raise ServerError

        if not self.experiment_config.attacker(0).use_existing_machine():
            try:
                self.attacker_1.destroy()
            except subprocess.CalledProcessError:
                # Machine does not exist
                pass
            self.attacker_1.create(reboot=True)
            self.attacker_1.up()
            self.attacker_1.install_caldera_server(cleanup=False)
        else:
            self.attacker_1.up()
            self.attacker_1.install_caldera_server(cleanup=False)

        self.attacker_1.start_caldera_server()

        if self.attacker_1 is None:
            raise ServerError
        # self.attacker_1.set_attack_logger(self.attack_logger)

    def __stop_attacker(self):
        """ Stop the attacking VM """
        self.attacker_1.halt()
