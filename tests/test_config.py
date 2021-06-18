#!/usr/bin/env python3

# Testing the central configuration loader

import unittest
# import os
from app.config import ExperimentConfig, MachineConfig
from app.exceptions import ConfigurationError

# https://docs.python.org/3/library/unittest.html


class TestMachineConfig(unittest.TestCase):
    """ Test machine specific config """

    def test_empty_init(self):
        """ The init is empty """

        with self.assertRaises(ConfigurationError):
            MachineConfig(None)

    def test_basic_init(self):
        """ The init is basic and working """
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "vm_controller": {
                                "type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target1"})
        self.assertEqual(mc.raw_config["root"], "systems/attacker1")
        self.assertEqual(mc.raw_config["vm_controller"]["type"], "vagrant")

    def test_missing_vm_name(self):
        """ The vm name is missing """

        with self.assertRaises(ConfigurationError):
            MachineConfig({"root": "systems/attacker1",
                           "os": "linux",
                           "vm_controller": {
                               "type": "vagrant",
                               "vagrantfilepath": "systems",
                           }})

    def test_use_existing_machine_is_true(self):
        """ Testing use_existing:machine setting """
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "vm_controller": {
                                "type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target1",
                            "use_existing_machine": True})
        self.assertEqual(mc.use_existing_machine(), True)

    def test_use_existing_machine_is_false(self):
        """ Testing use_existing:machine setting """
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "vm_controller": {
                                "type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target1",
                            "use_existing_machine": False})
        self.assertEqual(mc.use_existing_machine(), False)

    def test_use_existing_machine_is_default(self):
        """ Testing use_existing:machine setting """
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "vm_controller": {
                                "type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target1"})
        self.assertEqual(mc.use_existing_machine(), False)

    def test_windows_is_valid_os(self):
        """ Testing if windows is valid os """
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "windows",
                            "vm_controller": {
                                "type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target1"})
        self.assertEqual(mc.os(), "windows")

    def test_windows_is_valid_os_casefix(self):
        """ Testing if windows is valid os - using lowercase fix"""
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "WINDOWS",
                            "vm_controller": {
                                "type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target1"})
        self.assertEqual(mc.os(), "windows")

    def test_linux_is_valid_os(self):
        """ Testing if windows is valid os """
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "vm_controller": {
                                "type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target1"})
        self.assertEqual(mc.os(), "linux")

    def test_missing_os(self):
        """ The os is missing """

        with self.assertRaises(ConfigurationError):
            MachineConfig({"root": "systems/attacker1",
                           "vm_controller": {
                               "type": "vagrant",
                               "vagrantfilepath": "systems",
                           },
                           "vm_name": "target1"})

    def test_wrong_os(self):
        """ The os is wrong """

        with self.assertRaises(ConfigurationError):
            MachineConfig({"root": "systems/attacker1",
                           "os": "BROKEN",
                           "vm_controller": {
                               "type": "vagrant",
                               "vagrantfilepath": "systems",
                           },
                           "vm_name": "target1"})

    def test_vagrant_is_valid_vmcontroller(self):
        """ Testing if vagrant is valid vmcontroller """
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "vm_controller": {
                                "type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target1"})
        self.assertEqual(mc.vmcontroller(), "vagrant")

    def test_vagrant_is_valid_vmcontroller_casefix(self):
        """ Testing if vagrant is valid vmcontroller case fixxed"""
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "vm_controller": {
                                "type": "VAGRANT",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target1"})
        self.assertEqual(mc.vmcontroller(), "vagrant")

    def test_invalid_vmcontroller(self):
        """ Testing if vagrant is valid vmcontroller case fixxed"""
        with self.assertRaises(ConfigurationError):
            MachineConfig({"root": "systems/attacker1",
                           "os": "linux",
                           "vm_controller": {
                               "type": "BROKEN",
                               "vagrantfilepath": "systems",
                           },
                           "vm_name": "target1"})

    def test_missing_vmcontroller_2(self):
        """ Testing if vagrant is valid vmcontroller case fixxed"""
        with self.assertRaises(ConfigurationError):
            MachineConfig({"root": "systems/attacker1",
                           "os": "linux",
                           "vm_name": "target1"})

    def test_vagrant_is_valid_vmip(self):
        """ Testing if vagrant is valid ip/url """
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "vm_controller": {
                                "type": "vagrant",
                                "ip": "kali",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target1"})
        self.assertEqual(mc.vm_ip(), "kali")

    def test_missing_vmip(self):
        """ Testing if missing vm ip is handled"""
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "vm_controller": {
                                "type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target1"})
        self.assertEqual(mc.vm_ip(), None)

    def test_machinepath(self):
        """ Testing machinepath setting """
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "vm_controller": {
                                "type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target1",
                            "use_existing_machine": False,
                            "machinepath": "foo"})
        self.assertEqual(mc.machinepath(), "foo")

    def test_machinepath_fallback(self):
        """ Testing machinepath setting fallback to vmname"""
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "vm_controller": {
                                "type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target1",
                            "use_existing_machine": False})
        self.assertEqual(mc.machinepath(), "target1")

    def test_paw(self):
        """ Testing for caldera paw """
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "paw": "Bar",
                            "vm_controller": {
                                "type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target1",
                            "use_existing_machine": False})
        self.assertEqual(mc.caldera_paw(), "Bar")

    def test_paw_fallback(self):
        """ Testing for caldera paw fallback """
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "vm_controller": {
                                "type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target1",
                            "use_existing_machine": False})
        self.assertEqual(mc.caldera_paw(), None)

    def test_group(self):
        """ Testing for caldera group """
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "group": "Bar",
                            "vm_controller": {
                                "type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target1",
                            "use_existing_machine": False})
        self.assertEqual(mc.caldera_group(), "Bar")

    def test_group_fallback(self):
        """ Testing for caldera group fallback """
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "vm_controller": {
                                "type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target1",
                            "use_existing_machine": False})
        self.assertEqual(mc.caldera_group(), None)

    def test_ssh_keyfile(self):
        """ Testing keyfile config """
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "ssh_keyfile": "Bar",
                            "vm_controller": {
                                "type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target1",
                            "use_existing_machine": False})
        self.assertEqual(mc.ssh_keyfile(), "Bar")

    def test_ssh_keyfile_default(self):
        """ Testing keyfile config default """
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "vm_controller": {
                                "type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target1",
                            "use_existing_machine": False})
        self.assertEqual(mc.ssh_keyfile(), None)

    def test_ssh_user(self):
        """ Testing ssh user config """
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "ssh_user": "Bob",
                            "vm_controller": {
                                "type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target1",
                            "use_existing_machine": False})
        self.assertEqual(mc.ssh_user(), "Bob")

    def test_ssh_user_default(self):
        """ Testing ssh user default config """
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "vm_controller": {
                                "type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target1",
                            "use_existing_machine": False})
        self.assertEqual(mc.ssh_user(), "vagrant")

    def test_ssh_password(self):
        """ Testing ssh password config """
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "ssh_user": "Bob",
                            "ssh_password": "Ross",
                            "vm_controller": {
                                "type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target1",
                            "use_existing_machine": False})
        self.assertEqual(mc.ssh_password(), "Ross")

    def test_ssh_password_default(self):
        """ Testing ssh password default config """
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "vm_controller": {
                                "type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target1",
                            "use_existing_machine": False})
        self.assertIsNone(mc.ssh_password())

    def test_halt_needs_force_default(self):
        """ Testing 'halt needs force' default config """
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "vm_controller": {
                                "type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target1",
                            "use_existing_machine": False})
        self.assertEqual(mc.halt_needs_force(), False)

    def test_halt_needs_force(self):
        """ Testing 'halt needs force' config """
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "halt_needs_force": True,
                            "vm_controller": {
                                "type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target1",
                            "use_existing_machine": False})
        self.assertEqual(mc.halt_needs_force(), True)

    def test_vagrantfilepath(self):
        """ Testing vagrantfilepath config """
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "halt_needs_force": True,
                            "vm_controller": {
                                "type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target1",
                            "use_existing_machine": False})
        self.assertEqual(mc.vagrantfilepath(), "systems")

    def test_vagrantfilepath_missing(self):
        """ Testing missing vagrantfilepath config """

        with self.assertRaises(ConfigurationError):
            mc = MachineConfig({"root": "systems/attacker1",
                                "os": "linux",
                                "halt_needs_force": True,
                                "vm_controller": {
                                    "type": "vagrant",
                                },
                                "vm_name": "target1",
                                "use_existing_machine": False})
            mc.vagrantfilepath()

    def test_sensors_empty(self):
        """ Testing empty sensor config """

        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "halt_needs_force": True,
                            "vm_controller": {
                                "type": "vagrant",
                            },
                            "vm_name": "target1",
                            "use_existing_machine": False})
        self.assertEqual(mc.sensors(), [])

    def test_sensors_set(self):
        """ Testing empty sensor config """

        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "halt_needs_force": True,
                            "vm_controller": {
                                "type": "vagrant",
                            },
                            "vm_name": "target1",
                            "use_existing_machine": False,
                            "sensors": ["linux_idp", "test_sensor"]})
        self.assertEqual(mc.sensors(), ["linux_idp", "test_sensor"])

    def test_vulnerabilities_empty(self):
        """ Testing empty vulnerabilities config """

        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "halt_needs_force": True,
                            "vm_controller": {
                                "type": "vagrant",
                            },
                            "vm_name": "target1",
                            "use_existing_machine": False})
        self.assertEqual(mc.vulnerabilities(), [])

    def test_vulnerabilities_set(self):
        """ Testing empty vulnerabilities config """

        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "halt_needs_force": True,
                            "vm_controller": {
                                "type": "vagrant",
                            },
                            "vm_name": "target1",
                            "use_existing_machine": False,
                            "vulnerabilities": ["PEBKAC", "USER"]})
        self.assertEqual(mc.vulnerabilities(), ["PEBKAC", "USER"])

    def test_active_not_set(self):
        """ machine active not set """

        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "halt_needs_force": True,
                            "vm_controller": {
                                "type": "vagrant",
                            },
                            "vm_name": "target1",
                            "use_existing_machine": False,
                            "sensors": ["linux_idp", "test_sensor"]})
        self.assertEqual(mc.is_active(), True)

    def test_active_is_false(self):
        """ machine active is set to false """

        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "halt_needs_force": True,
                            "vm_controller": {
                                "type": "vagrant",
                            },
                            "vm_name": "target1",
                            "use_existing_machine": False,
                            "active": False,
                            "sensors": ["linux_idp", "test_sensor"]})
        self.assertEqual(mc.is_active(), False)

    def test_active_is_true(self):
        """ machine active is set to true """

        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "halt_needs_force": True,
                            "vm_controller": {
                                "type": "vagrant",
                            },
                            "vm_name": "target1",
                            "use_existing_machine": False,
                            "active": True,
                            "sensors": ["linux_idp", "test_sensor"]})
        self.assertEqual(mc.is_active(), True)


class TestExperimentConfig(unittest.TestCase):
    def test_missing_config_file(self):
        """  Missing config file """
        with self.assertRaises(FileNotFoundError):
            ExperimentConfig("tests/data/missing.yaml")

    def test_basic_loading(self):
        """ Existing, basic config file, testing the values are loaded properly """

        ex = ExperimentConfig("tests/data/basic.yaml")
        self.assertEqual(ex.raw_config["caldera"]["apikey"], "ADMIN123")
        self.assertEqual(ex.caldera_apikey(), "ADMIN123")

    def test_loot_dir(self):
        """ Test with existing loot dir """

        ex = ExperimentConfig("tests/data/basic.yaml")
        self.assertEqual(ex.loot_dir(), "loot")

    def test_missing_loot_dir(self):
        """ Test with missing loot dir """

        with self.assertRaises(ConfigurationError):
            ExperimentConfig("tests/data/basic_loot_missing.yaml")

    def test_missing_results(self):
        """ Test with missing results """

        with self.assertRaises(ConfigurationError):
            ExperimentConfig("tests/data/basic_results_missing.yaml")

    def test_basic_loading_targets_read(self):
        """ Targets in config: can be found """
        ex = ExperimentConfig("tests/data/basic.yaml")
        self.assertEqual(len(ex._targets), 2)
        self.assertEqual(ex._targets[0].raw_config["vm_name"], "target1")
        self.assertEqual(ex._targets[0].vmname(), "target1")
        self.assertEqual(ex.targets()[0].vmname(), "target1")

    def test_basic_loading_attacker_read(self):
        """ Attackers in config: can be found """
        ex = ExperimentConfig("tests/data/basic.yaml")
        self.assertEqual(len(ex._targets), 2)
        self.assertEqual(ex._attackers[0].raw_config["vm_name"], "attacker")
        self.assertEqual(ex._attackers[0].vmname(), "attacker")
        self.assertEqual(ex.attackers()[0].vmname(), "attacker")
        self.assertEqual(ex.attacker(0).vmname(), "attacker")

    def test_nicknames_missing(self):
        """ Test when the machine nicknames are non existing """
        ex = ExperimentConfig("tests/data/basic.yaml")
        self.assertEqual(ex._attackers[0].get_nicknames(), [])

    def test_nicknames_present_but_empty(self):
        """ Test when the machine nicknames are empty """
        ex = ExperimentConfig("tests/data/attacker_has_empty_nicknames.yaml")
        self.assertEqual(ex._attackers[0].get_nicknames(), [])

    def test_nicknames_present(self):
        """ Test when the machine nicknames are there """
        ex = ExperimentConfig("tests/data/attacker_has_empty_nicknames.yaml")
        self.assertEqual(ex._targets[0].get_nicknames(), [1, 2, 3])

    def test_missing_kali_config(self):
        """  Getting kali config for a specific attack. Attack missing """

        ex = ExperimentConfig("tests/data/basic.yaml")
        self.assertEqual(ex.kali_conf("BOOM"), {})

    def test_working_kali_config(self):
        """  Getting kali config for a specific attack """

        ex = ExperimentConfig("tests/data/basic.yaml")

        data = ex.kali_conf("hydra")
        self.assertEqual(data["userfile"], "users.txt")

    def test_kali_config_missing_attack_data(self):
        """  Getting kali config for a specific attack: Missing """

        ex = ExperimentConfig("tests/data/attacks_missing.yaml")

        data = ex.kali_conf("missing")
        self.assertEqual(data, {})

    def test_missing_caldera_config_obfuscator(self):
        """ A config file with no caldera config at all """

        ex = ExperimentConfig("tests/data/basic.yaml")
        self.assertEqual(ex.get_caldera_obfuscator(), "plain-text")

    def test_broken_caldera_config_obfuscator(self):
        """ A config file with broken caldera config at all """

        ex = ExperimentConfig("tests/data/partial.yaml")
        self.assertEqual(ex.get_caldera_obfuscator(), "plain-text")

    def test_good_caldera_config_obfuscator(self):
        """ A config file with broken caldera config at all """

        ex = ExperimentConfig("tests/data/attacks_perfect.yaml")
        self.assertEqual(ex.get_caldera_obfuscator(), "foo-bar")

    def test_missing_caldera_config_jitter(self):
        """ A config file with no caldera config at all """

        ex = ExperimentConfig("tests/data/basic.yaml")
        self.assertEqual(ex.get_caldera_jitter(), "4/8")

    def test_broken_caldera_config_jitter(self):
        """ A config file with broken caldera config at all """

        ex = ExperimentConfig("tests/data/partial.yaml")
        self.assertEqual(ex.get_caldera_jitter(), "4/8")

    def test_good_caldera_config_jitter(self):
        """ A config file with broken caldera config at all """

        ex = ExperimentConfig("tests/data/attacks_perfect.yaml")
        self.assertEqual(ex.get_caldera_jitter(), "08/15")

    def test_nap_time(self):
        """ nap time is set """

        ex = ExperimentConfig("tests/data/basic.yaml")

        self.assertEqual(ex.get_nap_time(), 5)

    def test_nap_time_not_set(self):
        """ nap time is not set """

        ex = ExperimentConfig("tests/data/nap_time_missing.yaml")

        self.assertEqual(ex.get_nap_time(), 0)

    def test_kali_attacks_missing(self):
        """ kali attacks entry fully missing from config """

        ex = ExperimentConfig("tests/data/attacks_missing.yaml")

        self.assertEqual(ex.get_kali_attacks("linux"), [])

    def test_kali_attacks_empty(self):
        """ zero entries in kali attacks list """

        ex = ExperimentConfig("tests/data/attacks_perfect.yaml")

        self.assertEqual(ex.get_kali_attacks("missing"), [])

    def test_kali_attacks_one(self):
        """ One entry in kali attacks list """

        ex = ExperimentConfig("tests/data/attacks_perfect.yaml")

        self.assertEqual(ex.get_kali_attacks("linux"), ["hydra"])

    def test_kali_attacks_many(self):
        """ Many entries in kali attacks list """

        ex = ExperimentConfig("tests/data/attacks_perfect.yaml")

        self.assertEqual(ex.get_kali_attacks("windows"), ["hydra", "medusa", "skylla"])

    def test_caldera_attacks_missing(self):
        """ caldera attacks entry fully missing from config """

        ex = ExperimentConfig("tests/data/attacks_missing.yaml")

        self.assertEqual(ex.get_caldera_attacks("linux"), [])

    def test_kali_attacks_half(self):
        """ kali attacks entry partially missing from config """

        ex = ExperimentConfig("tests/data/attacks_half.yaml")

        self.assertEqual(ex.get_kali_attacks("linux"), ["hydra"])
        self.assertEqual(ex.get_kali_attacks("windows"), [])

    def test_caldera_attacks_half(self):
        """ caldera attacks entry partially missing from config """

        ex = ExperimentConfig("tests/data/attacks_half.yaml")

        self.assertEqual(ex.get_caldera_attacks("linux"), ["bd527b63-9f9e-46e0-9816-b8434d2b8989"])
        self.assertEqual(ex.get_caldera_attacks("windows"), [])

    def test_caldera_attacks_empty(self):
        """ zero entries in caldera attacks list """

        ex = ExperimentConfig("tests/data/attacks_perfect.yaml")

        self.assertEqual(ex.get_caldera_attacks("missing"), [])

    def test_caldera_attacks_one(self):
        """ One entry in caldera attacks list """

        ex = ExperimentConfig("tests/data/attacks_perfect.yaml")

        self.assertEqual(ex.get_caldera_attacks("linux"), ["bd527b63-9f9e-46e0-9816-b8434d2b8989"])

    def test_caldera_attacks_many(self):
        """ Many entries in caldera attacks list """

        ex = ExperimentConfig("tests/data/attacks_perfect.yaml")

        self.assertEqual(ex.get_caldera_attacks("windows"), ["bd527b63-9f9e-46e0-9816-b8434d2b8989", "foo", "bar"])

    def test_basic_sensor_config(self):
        """ Test global configuration for a specific sensor """

        ex = ExperimentConfig("tests/data/basic.yaml")

        self.assertEqual(ex.get_sensor_config("windows_sensor"), {"dll_name": "windows_sensor.dll", "sensor_tool_folder": "windows_sensor"})

    def test_basic_sensor_config_missing(self):
        """ Test global configuration for a specific and missing sensor """

        ex = ExperimentConfig("tests/data/basic.yaml")

        self.assertEqual(ex.get_sensor_config("missing_windows_sensor"), {})

    def test_basic_sensor_entry_missing(self):
        """ Test global configuration for a specific and missing sensor entry"""

        ex = ExperimentConfig("tests/data/attacks_missing.yaml")

        self.assertEqual(ex.get_sensor_config("windows_sensor"), {})

    def test_basic_sensor_entry_empty(self):
        """ Test global configuration for a specific and empty sensor entry"""

        ex = ExperimentConfig("tests/data/basic_empty_sensor.yaml")

        self.assertEqual(ex.get_sensor_config("windows_sensor"), {})


if __name__ == '__main__':
    unittest.main()
