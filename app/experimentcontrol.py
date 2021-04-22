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


# TODO: Multi threading at least when starting machines

class Experiment():
    """ Class handling experiments """

    def __init__(self, configfile):
        """

        @param configfile: Path to the configfile to load """

        self.attacker_1 = None

        self.experiment_control = ExperimentConfig(configfile)
        self.attack_logger = AttackLog()
        self.__start_attacker()

        self.starttime = datetime.now().strftime("%Y_%m_%d___%H_%M_%S")
        self.lootdir = os.path.join(self.experiment_control.loot_dir(), self.starttime)
        os.makedirs(self.lootdir)

        self.targets = []
        # start target machines
        for target_conf in self.experiment_control.targets():
            if not target_conf.is_active():
                continue

            tname = target_conf.vmname()

            print(f"{CommandlineColors.OKBLUE}preparing target {tname} ....{CommandlineColors.ENDC}")
            target_1 = Machine(target_conf)
            target_1.set_caldera_server(self.attacker_1.getip())
            try:
                if not target_conf.use_existing_machine():
                    target_1.destroy()
            except subprocess.CalledProcessError:
                # Maybe the machine just does not exist yet
                pass
            target_1.install_caldera_service()
            target_1.up()
            # TODO prime sensors here
            needs_reboot = target_1.prime_sensors()
            if needs_reboot:
                target_1.reboot()
            print(f"{CommandlineColors.OKGREEN}Target is up: {tname}  {CommandlineColors.ENDC}")
            target_1.start_caldera_client()
            print(f"{CommandlineColors.OKGREEN}Initial start of caldera client: {tname}  {CommandlineColors.ENDC}")
            self.targets.append(target_1)

        # TODO: Install vulnerabilities by plugin

        print(f"{CommandlineColors.OKBLUE}Contacting caldera agents on all targets ....{CommandlineColors.ENDC}")
        time.sleep(20)
        # Wait until all targets are registered as Caldera targets
        for target_1 in self.targets:
            caldera_url = "http://" + self.attacker_1.getip() + ":8888"

            caldera_control = CalderaControl(caldera_url, config=self.experiment_control)
            running_agents = [i["paw"] for i in caldera_control.list_agents()]
            while target_1.get_paw() not in running_agents:
                print(f"Connecting to caldera {caldera_url}, running agents are: {running_agents}")
                print(f"Missing agent: {target_1.get_paw()} ...")
                target_1.start_caldera_client()
                print(f"Restarted caldera agent: {target_1.get_paw()} ...")
                time.sleep(120)    # Was 30, but maybe there are timing issues
                running_agents = [i["paw"] for i in caldera_control.list_agents()]
        print(f"{CommandlineColors.OKGREEN}Caldera agents reached{CommandlineColors.ENDC}")

        # Install vulnerabilities
        for a_target in self.targets:
            print(f"Installing vulnerabilities on {a_target.get_paw()}")
            a_target.install_vulnerabilities()
            a_target.start_vulnerabilities()

        # Install sensor plugins
        for a_target in self.targets:
            print(f"Installing sensors on {a_target.get_paw()}")
            a_target.install_sensors()
            a_target.start_sensors()

        # Attack them
        print(f"{CommandlineColors.OKBLUE}Running Caldera attacks{CommandlineColors.ENDC}")
        for target_1 in self.targets:
            # Run caldera attacks
            caldera_attacks = self.experiment_control.get_caldera_attacks(target_1.get_os())
            if caldera_attacks:
                for attack in caldera_attacks:
                    # TODO: Work with snapshots
                    # TODO: If we have several targets in the same group, it is nonsense to attack each one separately. Make this smarter
                    print(f"Attacking machine with PAW: {target_1.get_paw()}")
                    caldera_control = CalderaControl("http://" + self.attacker_1.getip() + ":8888", config=self.experiment_control)

                    caldera_control.attack(self.attack_logger, target_1.get_paw(), attack, target_1.get_group())

                    time.sleep(self.experiment_control.get_nap_time())
        print(f"{CommandlineColors.OKGREEN}Finished Caldera attacks{CommandlineColors.ENDC}")

        # Run Kali attacks
        print(f"{CommandlineColors.OKBLUE}Running Kali attacks{CommandlineColors.ENDC}")
        for target_1 in self.targets:
            kali_attacks = self.experiment_control.get_kali_attacks(target_1.get_os())
            for attack in kali_attacks:
                # TODO: Work with snapshots

                self.attacker_1.kali_attack(attack, target_1.getip(), self.experiment_control)

                time.sleep(self.experiment_control.get_nap_time())

        print(f"{CommandlineColors.OKGREEN}Finished Kali attacks{CommandlineColors.ENDC}")

        # Stop sensor plugins
        # Collect data
        for a_target in self.targets:
            a_target.stop_sensors()
            a_target.collect_sensors(self.lootdir)

        # Uninstall vulnerabilities
        for a_target in self.targets:
            print(f"Uninstalling vulnerabilities on {a_target.get_paw()}")
            a_target.stop_vulnerabilities()

        # TODO: Zip result dir

        # Stop target machines
        for target_1 in self.targets:
            target_1.halt()

        self.__stop_attacker()
        self.attack_logger.write_json(os.path.join(self.lootdir, "attack.json"))
        self.zip_loot()

    def zip_loot(self):
        """ Zip the loot together """

        filename = os.path.join(self.lootdir, self.starttime + ".zip")
        globs = ["/**/*.json",
                 "/**/*.proto",
                 "/*/**/*.zip",

                 ]

        print(f"Creating zip file {filename}")

        with zipfile.ZipFile(filename, "w") as zfh:
            for a_glob in globs:
                a_glob = self.lootdir + a_glob
                for a_file in glob.iglob(a_glob, recursive=True):
                    if a_file != filename:
                        print(a_file)
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
            os.makedirs(os.path.abspath(self.experiment_control.loot_dir()))
        except FileExistsError:
            pass
        for a_file in self.__get_results_files(root):
            print("Copy {} {}".format(a_file, os.path.abspath(self.experiment_control.loot_dir())))

    def __start_attacker(self):
        """ Start the attacking VM """

        # Preparing attacker
        self.attacker_1 = Machine(self.experiment_control.attacker(0).raw_config)

        if not self.experiment_control.attacker(0).use_existing_machine():
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
        self.attacker_1.set_attack_logger(self.attack_logger)

    def __stop_attacker(self):
        """ Stop the attacking VM """
        self.attacker_1.halt()
