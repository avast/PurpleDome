import unittest
import os
from app.machinecontrol import Machine
from app.exceptions import ConfigurationError
from app.config import MachineConfig
from unittest.mock import patch
from app.attack_log import AttackLog

# https://docs.python.org/3/library/unittest.html


class TestMachineControl(unittest.TestCase):

    def setUp(self) -> None:
        self.attack_logger = AttackLog(0)

    def test_get_os_linux_machine(self):
        m = Machine({"root": "systems/attacker1",
                     "os": "linux",
                     "vm_controller": {
                         "type": "vagrant",
                         "vagrantfilepath": "systems",
                     },
                     "vm_name": "target3"}, self.attack_logger)
        self.assertEqual(m.get_os(), "linux")

    def test_get_os_linux_machine_with_config_class(self):
        mc = MachineConfig({"root": "systems/attacker1",
                            "os": "linux",
                            "vm_controller": {
                                "type": "vagrant",
                                "vagrantfilepath": "systems",
                            },
                            "vm_name": "target3"})
        m = Machine(mc, self.attack_logger)
        self.assertEqual(m.get_os(), "linux")

    def test_get_os_missing(self):
        with self.assertRaises(ConfigurationError):
            Machine({"root": "systems/attacker1",
                     "vm_controller": {
                         "type": "vagrant",
                         "vagrantfilepath": "systems",
                     },
                     "vm_name": "target3"
                     }, self.attack_logger)

    def test_get_os_not_supported(self):
        with self.assertRaises(ConfigurationError):
            Machine({"root": "systems/attacker1",
                     "os": "nintendo_switch",
                     "vm_controller": {
                         "type": "vagrant",
                         "vagrantfilepath": "systems",
                     },
                     "vm_name": "target3"}, self.attack_logger)

    def test_get_paw_good(self):
        m = Machine({"root": "systems/attacker1",
                     "os": "linux",
                     "paw": "testme",
                     "vm_controller": {
                         "type": "vagrant",
                         "vagrantfilepath": "systems",
                     },
                     "vm_name": "target3"}, self.attack_logger)
        self.assertEqual(m.get_paw(), "testme")

    def test_get_paw_missing(self):
        m = Machine({"root": "systems/attacker1",
                     "os": "linux",
                     "vm_controller": {
                         "type": "vagrant",
                         "vagrantfilepath": "systems",
                     },
                     "vm_name": "target3"
                     }, self.attack_logger)
        self.assertEqual(m.get_paw(), None)

    def test_get_group_good(self):
        m = Machine({"root": "systems/attacker1",
                     "os": "linux",
                     "group": "testme",
                     "vm_controller": {
                         "type": "vagrant",
                         "vagrantfilepath": "systems",
                     },
                     "vm_name": "target3"}, self.attack_logger)
        self.assertEqual(m.get_group(), "testme")

    def test_get_group_missing(self):
        m = Machine({"root": "systems/attacker1",
                     "os": "linux",
                     "vm_controller": {
                         "type": "vagrant",
                         "vagrantfilepath": "systems",
                     },
                     "vm_name": "target3"
                     }, self.attack_logger)
        self.assertEqual(m.get_group(), None)

    def test_vagrantfilepath_missing(self):
        with self.assertRaises(ConfigurationError):
            Machine({"root": "systems/attacker1",
                     "os": "linux",
                     "vm_controller": {
                         "type": "vagrant",
                     },
                     "vm_name": "target3"
                     }, self.attack_logger)

    def test_vagrantfile_missing(self):
        with self.assertRaises(ConfigurationError):
            Machine({"root": "systems/attacker1",
                     "os": "linux",
                     "vm_controller": {
                         "type": "vagrant",
                         "vagrantfilepath": "non_existing",
                     },
                     "vm_name": "target3"
                     }, self.attack_logger)

    def test_vagrantfile_existing(self):
        m = Machine({"root": "systems/attacker1",
                     "os": "linux",
                     "vm_controller": {
                         "type": "vagrant",
                         "vagrantfilepath": "systems",
                     },
                     "vm_name": "target3"
                     }, self.attack_logger)
        self.assertIsNotNone(m)

    def test_name_missing(self):
        with self.assertRaises(ConfigurationError):
            Machine({"root": "systems/attacker1",
                     "os": "linux",
                     "vm_controller": {
                         "type": "vagrant",
                         "vagrantfilepath": "systems",
                     },
                     }, self.attack_logger)

    # test: auto generated, dir missing
    def test_auto_generated_machinepath_with_path_missing(self):
        with self.assertRaises(ConfigurationError):
            Machine({"root": "systems/attacker1",
                     "os": "linux",
                     "vm_controller": {
                         "type": "vagrant",
                         "vagrantfilepath": "systems",
                     },
                     "vm_name": "missing"
                     }, self.attack_logger)

    # test manual config, dir missing
    def test_configured_machinepath_with_path_missing(self):
        with self.assertRaises(ConfigurationError):
            Machine({"root": "systems/attacker1",
                     "os": "linux",
                     "vm_controller": {
                         "type": "vagrant",
                         "vagrantfilepath": "systems",
                     },
                     "vm_name": "target3",
                     "machinepath": "missing"
                     }, self.attack_logger)

    # test auto generated, dir there (external/internal dirs must work !)
    def test_auto_generated_machinepath_with_good_config(self):
        m = Machine({"root": "systems/attacker1",
                     "os": "linux",
                     "vm_controller": {
                         "type": "vagrant",
                         "vagrantfilepath": "systems",
                     },
                     "vm_name": "target3"
                     }, self.attack_logger)
        vagrantfilepath = os.path.abspath("systems")
        ext = os.path.join(vagrantfilepath, "target3")
        internal = os.path.join("/vagrant/", "target3")

        self.assertEqual(m.abs_machinepath_external, ext)
        self.assertEqual(m.abs_machinepath_internal, internal)

    # test: manual config, dir there (external/internal dirs must work !)
    def test_configured_machinepath_with_good_config(self):
        m = Machine({"root": "systems/attacker1",
                     "os": "linux",
                     "vm_controller": {
                         "type": "vagrant",
                         "vagrantfilepath": "systems",
                     },
                     "vm_name": "missing",
                     "machinepath": "target3"
                     }, self.attack_logger)
        vagrantfilepath = os.path.abspath("systems")
        ext = os.path.join(vagrantfilepath, "target3")
        internal = os.path.join("/vagrant/", "target3")

        self.assertEqual(m.abs_machinepath_external, ext)
        self.assertEqual(m.abs_machinepath_internal, internal)

    # vm_controller missing
    def test_configured_vm_controller_missing(self):
        with self.assertRaises(ConfigurationError):
            Machine({"root": "systems/attacker1",
                     "os": "linux",
                     "vm_name": "missing",
                     "machinepath": "target3"
                     }, self.attack_logger)

    # vm_controller wrong
    def test_configured_vm_controller_wrong_type(self):
        with self.assertRaises(ConfigurationError):
            Machine({"root": "systems/attacker1",
                     "os": "linux",
                     "vm_controller": {
                         "type": "wrong_controller",
                         "vagrantfilepath": "systems",
                     },
                     "vm_name": "missing",
                     "machinepath": "target3"
                     }, self.attack_logger)

    # Create caldera start command and verify it
    def test_get_linux_caldera_start_cmd(self):
        m = Machine({"root": "systems/attacker1",
                     "os": "linux",
                     "vm_controller": {
                         "type": "vagrant",
                         "vagrantfilepath": "systems",
                     },
                     "vm_name": "target3",
                     "group": "testgroup",
                     "paw": "testpaw"}, self.attack_logger)
        m.set_caldera_server("http://www.test.test")
        with patch.object(m.vm_manager, "get_playground", return_value="/vagrant/target3"):
            cmd = m.create_start_caldera_client_cmd()
        self.assertEqual(cmd.strip(), "cd /vagrant/target3; chmod +x caldera_agent.sh; nohup bash ./caldera_agent.sh".strip())

    # Create caldera start command and verify it (windows)
    def test_get_windows_caldera_start_cmd(self):
        m = Machine({"root": "systems/attacker1",
                     "os": "windows",
                     "vm_controller": {
                         "type": "vagrant",
                         "vagrantfilepath": "systems",
                     },
                     "vm_name": "target3",
                     "group": "testgroup",
                     "paw": "testpaw",
                     "machinepath": "target2w"}, self.attack_logger)
        m.set_caldera_server("www.test.test")
        cmd = m.create_start_caldera_client_cmd()
        self.maxDiff = None
        expected = """
caldera_agent.bat"""
        self.assertEqual(cmd.strip(), expected.strip())


if __name__ == '__main__':
    unittest.main()
