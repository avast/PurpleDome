#!/usr/bin/env python3
""" Unit tests for machinecontrol """

import os
import unittest
from unittest.mock import patch

from dotmap import DotMap

from app.attack_log import AttackLog
from app.config import MachineConfig
from app.config_verifier import Attacker, Target
from app.exceptions import ConfigurationError
from app.machinecontrol import Machine


# https://docs.python.org/3/library/unittest.html


class TestMachineControl(unittest.TestCase):
    """ Unit tests for machine control """
    def setUp(self) -> None:
        self.attack_logger = AttackLog(0)

    def test_get_os_linux_machine(self):
        conf = {  # "root": "systems/attacker1",
            "os": "linux",
            "vm_controller": {
                "vm_type": "vagrant",
                "vagrantfilepath": "systems",
            },
            "vm_name": "target3",
            "machinepath": "target3",
            "nicknames": [],
            "sensors": [],
            "paw": "ignoreme",
            "name": "Foobar",
            "group": "some_group",
        }

        m = Machine(Target(**conf), self.attack_logger)
        self.assertEqual(m.get_os(), "linux")

    def test_get_os_linux_machine_with_config_class(self):
        mc = MachineConfig(DotMap({"root": "systems/attacker1",
                                   "os": "linux",
                                   "vm_controller": {
                                       "vm_type": "vagrant",
                                       "vagrantfilepath": "systems",
                                   },
                                   "vm_name": "target3"}))
        m = Machine(mc, self.attack_logger)
        self.assertEqual(m.get_os(), "linux")

    def test_get_paw_good(self):
        conf = {
            "os": "linux",
            "vm_controller": {
                "vm_type": "vagrant",
                "vagrantfilepath": "systems",
            },
            "vm_name": "target3",
            "machinepath": "target3",
            "nicknames": [],
            "sensors": [],
            "paw": "testme",
            "name": "Foobar",
            "group": "some_group",
        }
        m = Machine(Target(**conf), self.attack_logger)
        self.assertEqual(m.get_paw(), "testme")

    def test_get_paw_missing(self):
        conf = {
            "os": "linux",
            "vm_controller": {
                "vm_type": "vagrant",
                "vagrantfilepath": "systems",
            },
            "vm_name": "target3",
            "machinepath": "target3",
            "nicknames": [],
            "sensors": [],
            "name": "Foobar",
            "group": "some_group",
        }
        with self.assertRaisesRegex(TypeError, 'paw'):
            Machine(Target(**conf), self.attack_logger)

    def test_get_group_good(self):
        conf = {
            "os": "linux",
            "vm_controller": {
                "vm_type": "vagrant",
                "vagrantfilepath": "systems",
            },
            "vm_name": "target3",
            "machinepath": "target3",
            "nicknames": [],
            "sensors": [],
            "name": "Foobar",
            "paw": "some_paw",
            "group": "testme"
        }
        m = Machine(Target(**conf), self.attack_logger)
        self.assertEqual(m.get_group(), "testme")

    def test_get_group_missing(self):
        conf = {
            "os": "linux",
            "vm_controller": {
                "vm_type": "vagrant",
                "vagrantfilepath": "systems",
            },
            "vm_name": "target3",
            "machinepath": "target3",
            "nicknames": [],
            "sensors": [],
            "name": "Foobar",
            "paw": "some_paw",
        }
        with self.assertRaisesRegex(TypeError, 'group'):
            Machine(Target(**conf), self.attack_logger)

    def test_vagrantfilepath_missing(self):
        with self.assertRaises(ConfigurationError):
            Machine(DotMap({"root": "systems/attacker1",
                            "os": "linux",
                            "vm_controller": {
                                "vm_type": "vagrant",
                            },
                            "vm_name": "target3"
                            }), self.attack_logger)

    def test_vagrantfile_missing(self):
        with self.assertRaises(ConfigurationError):
            Machine(DotMap({"root": "systems/attacker1",
                            "os": "linux",
                            "vm_controller": {
                                "vm_type": "vagrant",
                                "vagrantfilepath": "non_existing",
                            },
                            "vm_name": "target3"
                            }), self.attack_logger)

    def test_vagrantfile_existing(self):
        conf = {
            "os": "linux",
            "vm_controller": {
                "vm_type": "vagrant",
                "vagrantfilepath": "systems",
            },
            "vm_name": "target3",
            "name": "test_attacker",
            "nicknames": ["a", "b"],
            "machinepath": "attacker1"
        }
        m = Machine(Attacker(**conf), self.attack_logger)
        self.assertIsNotNone(m)

    # test: auto generated, dir missing
    def test_auto_generated_machinepath_with_path_missing(self):
        with self.assertRaises(ConfigurationError):
            Machine(DotMap({"root": "systems/attacker1",
                            "os": "linux",
                            "vm_controller": {
                                "vm_type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "missing"
                            }), self.attack_logger)

    # test manual config, dir missing
    def test_configured_machinepath_with_path_missing(self):
        with self.assertRaises(ConfigurationError):
            Machine(DotMap({"root": "systems/attacker1",
                            "os": "linux",
                            "vm_controller": {
                                "vm_type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target3",
                            "machinepath": "missing"
                            }), self.attack_logger)

    # test auto generated, dir there (external/internal dirs must work !)
    def test_missing_machinepath_with_good_config_eeception(self):
        conf = {
            "os": "linux",
            "vm_controller": {
                "vm_type": "vagrant",
                "vagrantfilepath": "systems",
            },
            "vm_name": "target3",
            "nicknames": [],
            "sensors": [],
            "name": "Foobar",
            "paw": "some_paw",
            "group": "some_group",
        }

        with self.assertRaisesRegex(TypeError, "machinepath"):
            Machine(Target(**conf), self.attack_logger)

    # test: manual config, dir there (external/internal dirs must work !)
    def test_configured_machinepath_with_good_config(self):
        conf = {
            "os": "linux",
            "vm_controller": {
                "vm_type": "vagrant",
                "vagrantfilepath": "systems",
            },
            "vm_name": "target3",
            "machinepath": "target3",
            "nicknames": [],
            "sensors": [],
            "name": "Foobar",
            "paw": "some_paw",
            "group": "some_group",
        }

        m = Machine(Target(**conf), self.attack_logger)

        vagrantfilepath = os.path.abspath("systems")
        ext = os.path.join(vagrantfilepath, "target3")
        internal = os.path.join("/vagrant/", "target3")

        self.assertEqual(m.abs_machinepath_external, ext)
        self.assertEqual(m.abs_machinepath_internal, internal)

    # vm_controller missing
    def test_configured_vm_controller_missing(self):
        with self.assertRaises(ConfigurationError):
            Machine(DotMap({"root": "systems/attacker1",
                            "os": "linux",
                            "vm_name": "missing",
                            "machinepath": "target3"
                            }), self.attack_logger)

    # Create caldera start command and verify it
    def test_get_linux_caldera_start_cmd(self):
        conf = {
            "os": "linux",
            "vm_controller": {
                "vm_type": "vagrant",
                "vagrantfilepath": "systems",
            },
            "vm_name": "target3",
            "group": "testgroup",
            "paw": "testpaw",
            "name": "test_attacker",
            "nicknames": ["a", "b"],
            "machinepath": "target3",
            "sensors": []
        }
        m = Machine(Target(**conf), self.attack_logger)
        m.set_caldera_server("http://www.test.test")
        with patch.object(m.vm_manager, "get_playground", return_value="/vagrant/target3"):
            cmd = m.create_start_caldera_client_cmd()
        self.assertEqual(cmd.strip(), "cd /vagrant/target3; chmod +x caldera_agent.sh; nohup bash ./caldera_agent.sh".strip())

    # Create caldera start command and verify it (windows)
    def test_get_windows_caldera_start_cmd(self):
        conf = {
            "os": "windows",
            "vm_controller": {
                "vm_type": "vagrant",
                "vagrantfilepath": "systems",
            },
            "vm_name": "target3",
            "group": "testgroup",
            "paw": "testpaw",
            "name": "test_attacker",
            "nicknames": ["a", "b"],
            "machinepath": "target3",
            "sensors": []
        }
        m = Machine(Target(**conf), self.attack_logger)
        m.set_caldera_server("www.test.test")
        cmd = m.create_start_caldera_client_cmd()
        # self.maxDiff = None
        expected = """
caldera_agent.bat"""
        self.assertEqual(cmd.strip(), expected.strip())


if __name__ == '__main__':
    unittest.main()
