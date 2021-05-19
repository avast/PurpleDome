#!/usr/bin/env python3

""" A class to control a whole experiment. From setting up the machines to running the attacks """

import glob
import os
import subprocess
import time
import zipfile
from datetime import datetime

from app.attack_log import AttackLog
from app.config import ExperimentConfig
from app.interface_sfx import CommandlineColors
from caldera_control import CalderaControl
from machine_control import Machine
from app.exceptions import ServerError
from plugins.base.kali import KaliPlugin
from app.pluginmanager import PluginManager


# TODO: Multi threading at least when starting machines

class Experiment():
    """ Class handling experiments """

    def __init__(self, configfile, verbosity=0, caldera_attacks: list = None):
        """

        @param configfile: Path to the configfile to load
        @param verbosity: verbosity level between 0 and 3
        @param caldera_attacks: an optional argument to override caldera attacks in the config file and run just this one caldera attack. A list of caldera ID
        """
        self.attacker_1 = None

        self.experiment_config = ExperimentConfig(configfile)
        self.attack_logger = AttackLog(verbosity)
        self.plugin_manager = PluginManager(self.attack_logger)
        self.__start_attacker()
        caldera_url = "http://" + self.attacker_1.getip() + ":8888"
        caldera_control = CalderaControl(caldera_url, attack_logger=self.attack_logger, config=self.experiment_config)
        # Deleting all currently registered Caldera gents
        self.attack_logger.vprint(caldera_control.kill_all_agents(), 3)
        self.attack_logger.vprint(caldera_control.delete_all_agents(), 3)

        self.starttime = datetime.now().strftime("%Y_%m_%d___%H_%M_%S")
        self.lootdir = os.path.join(self.experiment_config.loot_dir(), self.starttime)
        os.makedirs(self.lootdir)

        self.targets = []
        # start target machines
        for target_conf in self.experiment_config.targets():
            if not target_conf.is_active():
                continue

            tname = target_conf.vmname()

            self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}preparing target {tname} ....{CommandlineColors.ENDC}", 1)
            target_1 = Machine(target_conf, attack_logger=self.attack_logger)
            target_1.set_caldera_server(self.attacker_1.getip())
            try:
                if not target_conf.use_existing_machine():
                    target_1.destroy()
            except subprocess.CalledProcessError:
                # Maybe the machine just does not exist yet
                pass
            target_1.install_caldera_service()
            target_1.up()
            needs_reboot = target_1.prime_sensors()
            if needs_reboot:
                target_1.reboot()
            self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}Target is up: {tname}  {CommandlineColors.ENDC}", 1)
            self.targets.append(target_1)

        # Install vulnerabilities
        for a_target in self.targets:
            self.attack_logger.vprint(f"Installing vulnerabilities on {a_target.get_paw()}", 2)
            a_target.install_vulnerabilities()
            a_target.start_vulnerabilities()

        # Install sensor plugins
        for a_target in self.targets:
            self.attack_logger.vprint(f"Installing sensors on {a_target.get_paw()}", 2)
            a_target.install_sensors()
            a_target.start_sensors()

        # First start of caldera implants
        for target_1 in self.targets:
            target_1.start_caldera_client()
            self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}Initial start of caldera client: {tname}  {CommandlineColors.ENDC}", 1)
        time.sleep(20)   # Wait for all the clients to contact the caldera server

        self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Contacting caldera agents on all targets ....{CommandlineColors.ENDC}", 1)
        # Wait until all targets are registered as Caldera targets
        for target_1 in self.targets:
            running_agents = caldera_control.list_paws_of_running_agents()
            self.attack_logger.vprint(f"Agents currently running: {running_agents}", 2)
            while target_1.get_paw() not in running_agents:
                self.attack_logger.vprint(f"Connecting to caldera {caldera_url}, running agents are: {running_agents}", 3)
                self.attack_logger.vprint(f"Missing agent: {target_1.get_paw()} ...", 3)
                target_1.start_caldera_client()
                self.attack_logger.vprint(f"Restarted caldera agent: {target_1.get_paw()} ...", )
                time.sleep(120)    # Was 30, but maybe there are timing issues
                running_agents = caldera_control.list_paws_of_running_agents()
        self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}Caldera agents reached{CommandlineColors.ENDC}", 1)

        # Attack them
        self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Running Caldera attacks{CommandlineColors.ENDC}", 1)
        for target_1 in self.targets:
            if caldera_attacks is None:
                # Run caldera attacks
                caldera_attacks = self.experiment_config.get_caldera_attacks(target_1.get_os())
            if caldera_attacks:
                for attack in caldera_attacks:
                    # TODO: Work with snapshots
                    # TODO: If we have several targets in the same group, it is nonsense to attack each one separately. Make this smarter
                    self.attack_logger.vprint(f"Attacking machine with PAW: {target_1.get_paw()} with {attack}", 2)
                    caldera_control = CalderaControl("http://" + self.attacker_1.getip() + ":8888", self.attack_logger, config=self.experiment_config)

                    it_worked = caldera_control.attack(attack_logger=self.attack_logger,
                                                       paw=target_1.get_paw(),
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
                        self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Restarting caldera server and waiting for clients to re-connect{CommandlineColors.ENDC}", 1)
                        self.attacker_1.start_caldera_server()
                        self.attack_logger.vprint(f"Pausing before next attack (config: nap_time): {self.experiment_config.get_nap_time()}", 2)
                        time.sleep(self.experiment_config.get_nap_time())
                        retries = 100
                        for target_system in self.targets:
                            running_agents = caldera_control.list_paws_of_running_agents()
                            self.attack_logger.vprint(f"Agents currently connected to the server: {running_agents}", 2)
                            while target_system.get_paw() not in running_agents:
                                time.sleep(1)
                                running_agents = caldera_control.list_paws_of_running_agents()
                                retries -= 1
                                self.attack_logger.vprint(f"Waiting for clients to re-connect ({retries}, {running_agents}) ", 3)
                                if retries <= 0:
                                    raise ServerError
                        self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}Restarted caldera server clients re-connected{CommandlineColors.ENDC}", 1)
                        # End of fix

        self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}Finished Caldera attacks{CommandlineColors.ENDC}", 1)

        # Run Kali attacks
        self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Running Kali attacks{CommandlineColors.ENDC}", 1)
        for target_1 in self.targets:
            kali_attacks = self.experiment_config.get_kali_attacks(target_1.get_os())
            for attack in kali_attacks:
                # TODO: Work with snapshots
                self.attack_logger.vprint(f"Attacking machine with PAW: {target_1.get_paw()} with attack: {attack}", 1)
                # self.attacker_1.kali_attack(attack, target_1.getip(), self.experiment_config)
                self.attack(target_1, attack)
                self.attack_logger.vprint(f"Pausing before next attack (config: nap_time): {self.experiment_config.get_nap_time()}", 3)
                time.sleep(self.experiment_config.get_nap_time())

        self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}Finished Kali attacks{CommandlineColors.ENDC}", 1)

        # Stop sensor plugins
        # Collect data
        for a_target in self.targets:
            a_target.stop_sensors()
            a_target.collect_sensors(self.lootdir)

        # Uninstall vulnerabilities
        for a_target in self.targets:
            self.attack_logger.vprint(f"{CommandlineColors.OKBLUE} Uninstalling vulnerabilities on {a_target.get_paw()} {CommandlineColors.ENDC}", 1)
            a_target.stop_vulnerabilities()
            self.attack_logger.vprint(f"{CommandlineColors.OKGREEN} Done uninstalling vulnerabilities on {a_target.get_paw()} {CommandlineColors.ENDC}", 1)

        # Stop target machines
        for target_1 in self.targets:
            target_1.halt()
        self.__stop_attacker()

        self.attack_logger.write_json(os.path.join(self.lootdir, "attack.json"))
        self.zip_loot()

    def attack(self, target, attack):
        """ Pick an attack and run it

        @param attack: Name of the attack to run
        @param target: IP address of the target
        @returns: The output of the cmdline attacking tool
        """

        # TODO: Extend beyond Kali

        for plugin in self.plugin_manager.get_plugins(KaliPlugin, [attack]):
            name = plugin.get_name()

            self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Running Kali plugin {name}{CommandlineColors.ENDC}", 2)
            plugin.process_config(self.experiment_config.kali_conf(plugin.get_config_section_name()))    # TODO: De-kalify
            plugin.set_attacker_machine(self.attacker_1)

            # plugin.__set_logger__(self.attack_logger)
            plugin.__execute__([target.getip()])

    def zip_loot(self):
        """ Zip the loot together """

        filename = os.path.join(self.lootdir, self.starttime + ".zip")
        globs = ["/**/*.json",
                 "/**/*.proto",
                 "/*/**/*.zip",

                 ]

        self.attack_logger.vprint(f"Creating zip file {filename}", 1)

        with zipfile.ZipFile(filename, "w") as zfh:
            for a_glob in globs:
                a_glob = self.lootdir + a_glob
                for a_file in glob.iglob(a_glob, recursive=True):
                    if a_file != filename:
                        self.attack_logger.vprint(a_file, 2)
                        zfh.write(a_file)

    @staticmethod
    def __get_results_files(root):
        """ Yields a list of potential result files

        @param root: Root dir of the machine to collect data from
        """
        # TODO: Properly implement. Get proper root parameter

        total = [os.path.join(root, "logstash", "filebeat.json")]
        for a_file in total:
            if os.path.exists(a_file):
                yield a_file

    def __clean_result_files(self, root):
        """ Deletes result files

        @param root: Root dir of the machine to collect data from
        """

        # TODO: Properly implement. Get proper root parameter

        for a_file in self.__get_results_files(root):
            os.remove(a_file)

    def __collect_loot(self, root):
        """ Collect results into loot dir

        @param root: Root dir of the machine to collect data from
        """

        try:
            os.makedirs(os.path.abspath(self.experiment_config.loot_dir()))
        except FileExistsError:
            pass
        for a_file in self.__get_results_files(root):
            self.attack_logger.vprint("Copy {} {}".format(a_file, os.path.abspath(self.experiment_config.loot_dir())), 3)

    def __start_attacker(self):
        """ Start the attacking VM """

        # Preparing attacker
        self.attacker_1 = Machine(self.experiment_config.attacker(0).raw_config, attack_logger=self.attack_logger)

        if not self.experiment_config.attacker(0).use_existing_machine():
            try:
                self.attacker_1.destroy()
            except subprocess.CalledProcessError:
                # Machine does not exist
                pass
            self.attacker_1.create(reboot=False)
            self.attacker_1.up()
            self.attacker_1.install_caldera_server(cleanup=False)
        else:
            self.attacker_1.up()
            self.attacker_1.install_caldera_server(cleanup=False)

        self.attacker_1.start_caldera_server()
        # self.attacker_1.set_attack_logger(self.attack_logger)

    def __stop_attacker(self):
        """ Stop the attacking VM """
        self.attacker_1.halt()
