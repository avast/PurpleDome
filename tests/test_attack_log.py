#!/usr/bin/env python3

# Testing the attack log class

import unittest
from app.attack_log import AttackLog
import app.attack_log
# from unittest.mock import patch, call
# from app.exceptions import ConfigurationError

# https://docs.python.org/3/library/unittest.html


class TestMachineConfig(unittest.TestCase):
    """ Test machine specific config """

    def test_init(self):
        """ The init is empty """
        al = AttackLog()
        self.assertIsNotNone(al)
        self.assertEqual(al.get_dict(), [])

    def test_caldera_attack_start(self):
        """ Starting a caldera attack """
        al = AttackLog()
        source = "asource"
        paw = "apaw"
        group = "agroup"
        ability_id = "aability_id"
        ttp = "1234"
        name = "aname"
        description = "adescription"
        al.start_caldera_attack(source=source,
                                paw=paw,
                                group=group,
                                ability_id=ability_id,
                                ttp=ttp,
                                name=name,
                                description=description
                                )
        data = al.get_dict()
        self.assertEqual(data[0]["event"], "start")
        self.assertEqual(data[0]["type"], "attack")
        self.assertEqual(data[0]["sub-type"], "caldera")
        self.assertEqual(data[0]["source"], source)
        self.assertEqual(data[0]["target_paw"], paw)
        self.assertEqual(data[0]["target_group"], group)
        self.assertEqual(data[0]["ability_id"], ability_id)
        self.assertEqual(data[0]["hunting_tag"], "MITRE_" + ttp)
        self.assertEqual(data[0]["name"], name)
        self.assertEqual(data[0]["description"], description)

    def test_caldera_attack_stop(self):
        """ Stopping a caldera attack """
        al = AttackLog()
        source = "asource"
        paw = "apaw"
        group = "agroup"
        ability_id = "aability_id"
        ttp = "1234"
        name = "aname"
        description = "adescription"
        al.stop_caldera_attack(source=source,
                               paw=paw,
                               group=group,
                               ability_id=ability_id,
                               ttp=ttp,
                               name=name,
                               description=description
                               )
        data = al.get_dict()
        self.assertEqual(data[0]["event"], "stop")
        self.assertEqual(data[0]["type"], "attack")
        self.assertEqual(data[0]["sub-type"], "caldera")
        self.assertEqual(data[0]["source"], source)
        self.assertEqual(data[0]["target_paw"], paw)
        self.assertEqual(data[0]["target_group"], group)
        self.assertEqual(data[0]["ability_id"], ability_id)
        self.assertEqual(data[0]["hunting_tag"], "MITRE_" + ttp)
        self.assertEqual(data[0]["name"], name)
        self.assertEqual(data[0]["description"], description)

    def test_kali_attack_start(self):
        """ Starting a kali attack """
        al = AttackLog()
        source = "asource"
        target = "a target"
        ttp = "1234"
        attack_name = "a name"
        al.start_kali_attack(source=source,
                             target=target,
                             attack_name=attack_name,
                             ttp=ttp,
                             )
        data = al.get_dict()
        self.assertEqual(data[0]["event"], "start")
        self.assertEqual(data[0]["type"], "attack")
        self.assertEqual(data[0]["sub-type"], "kali")
        self.assertEqual(data[0]["source"], source)
        self.assertEqual(data[0]["target"], target)
        self.assertEqual(data[0]["kali_name"], attack_name)
        self.assertEqual(data[0]["hunting_tag"], "MITRE_" + ttp)

    def test_kali_attack_stop(self):
        """ Stopping a kali attack """
        al = AttackLog()
        source = "asource"
        target = "a target"
        ttp = "1234"
        attack_name = "a name"
        al.stop_kali_attack(source=source,
                            target=target,
                            attack_name=attack_name,
                            ttp=ttp,
                            )
        data = al.get_dict()
        self.assertEqual(data[0]["event"], "stop")
        self.assertEqual(data[0]["type"], "attack")
        self.assertEqual(data[0]["sub-type"], "kali")
        self.assertEqual(data[0]["source"], source)
        self.assertEqual(data[0]["target"], target)
        self.assertEqual(data[0]["kali_name"], attack_name)
        self.assertEqual(data[0]["hunting_tag"], "MITRE_" + ttp)

    def test_metasploit_attack_start(self):
        """ Starting a metasploit attack """
        al = AttackLog()
        source = "asource"
        target = "a target"
        ttp = "1234"
        attack_name = "a name"
        al.start_metasploit_attack(source=source,
                                   target=target,
                                   metasploit_command=attack_name,
                                   ttp=ttp,
                                   )
        data = al.get_dict()
        self.assertEqual(data[0]["event"], "start")
        self.assertEqual(data[0]["type"], "attack")
        self.assertEqual(data[0]["sub-type"], "metasploit")
        self.assertEqual(data[0]["source"], source)
        self.assertEqual(data[0]["target"], target)
        self.assertEqual(data[0]["metasploit_command"], attack_name)
        self.assertEqual(data[0]["hunting_tag"], "MITRE_" + ttp)

    def test_metasploit_attack_stop(self):
        """ Stopping a metasploit attack """
        al = AttackLog()
        source = "asource"
        target = "a target"
        ttp = "1234"
        attack_name = "a name"
        al.stop_metasploit_attack(source=source,
                                  target=target,
                                  metasploit_command=attack_name,
                                  ttp=ttp,
                                  )
        data = al.get_dict()
        self.assertEqual(data[0]["event"], "stop")
        self.assertEqual(data[0]["type"], "attack")
        self.assertEqual(data[0]["sub-type"], "metasploit")
        self.assertEqual(data[0]["source"], source)
        self.assertEqual(data[0]["target"], target)
        self.assertEqual(data[0]["metasploit_command"], attack_name)
        self.assertEqual(data[0]["hunting_tag"], "MITRE_" + ttp)

    def test_attack_plugin_start(self):
        """ Starting a attack plugin """
        al = AttackLog()
        source = "asource"
        target = "a target"
        ttp = "1234"
        attack_name = "a name"
        al.start_attack_plugin(source=source,
                               target=target,
                               plugin_name=attack_name,
                               ttp=ttp,
                               )
        data = al.get_dict()
        self.assertEqual(data[0]["event"], "start")
        self.assertEqual(data[0]["type"], "attack")
        self.assertEqual(data[0]["sub-type"], "attack_plugin")
        self.assertEqual(data[0]["source"], source)
        self.assertEqual(data[0]["target"], target)
        self.assertEqual(data[0]["plugin_name"], attack_name)
        self.assertEqual(data[0]["hunting_tag"], "MITRE_" + ttp)

    def test_attack_plugin_stop(self):
        """ Stopping a attack plugin"""
        al = AttackLog()
        source = "asource"
        target = "a target"
        ttp = "1234"
        attack_name = "a name"
        al.stop_attack_plugin(source=source,
                              target=target,
                              plugin_name=attack_name,
                              ttp=ttp,
                              )
        data = al.get_dict()
        self.assertEqual(data[0]["event"], "stop")
        self.assertEqual(data[0]["type"], "attack")
        self.assertEqual(data[0]["sub-type"], "attack_plugin")
        self.assertEqual(data[0]["source"], source)
        self.assertEqual(data[0]["target"], target)
        self.assertEqual(data[0]["plugin_name"], attack_name)
        self.assertEqual(data[0]["hunting_tag"], "MITRE_" + ttp)

    def test_file_write_start(self):
        """ Starting a file write """
        al = AttackLog()
        source = "asource"
        target = "a target"
        file_name = "a generic filename"
        al.start_file_write(source=source,
                            target=target,
                            file_name=file_name,
                            )
        data = al.get_dict()
        self.assertEqual(data[0]["event"], "start")
        self.assertEqual(data[0]["type"], "dropping_file")
        self.assertEqual(data[0]["sub-type"], "by PurpleDome")
        self.assertEqual(data[0]["source"], source)
        self.assertEqual(data[0]["target"], target)
        self.assertEqual(data[0]["file_name"], file_name)

    def test_file_write_stop(self):
        """ Stopping a file write """
        al = AttackLog()
        source = "asource"
        target = "a target"
        file_name = "a generic filename"
        al.stop_file_write(source=source,
                           target=target,
                           file_name=file_name,
                           )
        data = al.get_dict()
        self.assertEqual(data[0]["event"], "stop")
        self.assertEqual(data[0]["type"], "dropping_file")
        self.assertEqual(data[0]["sub-type"], "by PurpleDome")
        self.assertEqual(data[0]["source"], source)
        self.assertEqual(data[0]["target"], target)
        self.assertEqual(data[0]["file_name"], file_name)

    def test_execute_payload_start(self):
        """ Starting a execute payload """
        al = AttackLog()
        source = "asource"
        target = "a target"
        command = "a generic command"
        al.start_execute_payload(source=source,
                                 target=target,
                                 command=command,
                                 )
        data = al.get_dict()
        self.assertEqual(data[0]["event"], "start")
        self.assertEqual(data[0]["type"], "execute_payload")
        self.assertEqual(data[0]["sub-type"], "by PurpleDome")
        self.assertEqual(data[0]["source"], source)
        self.assertEqual(data[0]["target"], target)
        self.assertEqual(data[0]["command"], command)

    def test_execute_payload_stop(self):
        """ Stopping a execute payload """
        al = AttackLog()
        source = "asource"
        target = "a target"
        command = "a generic command"
        al.stop_execute_payload(source=source,
                                target=target,
                                command=command,
                                )
        data = al.get_dict()
        self.assertEqual(data[0]["event"], "stop")
        self.assertEqual(data[0]["type"], "execute_payload")
        self.assertEqual(data[0]["sub-type"], "by PurpleDome")
        self.assertEqual(data[0]["source"], source)
        self.assertEqual(data[0]["target"], target)
        self.assertEqual(data[0]["command"], command)

    def test_mitre_fix_ttp_is_none(self):
        """ Testing the mitre ttp fix for ttp being none """
        self.assertEqual(app.attack_log.__mitre_fix_ttp__(None), "")

    def test_mitre_fix_ttp_is_MITRE_SOMETHING(self):
        """ Testing the mitre ttp fix for ttp being MITRE_ """
        self.assertEqual(app.attack_log.__mitre_fix_ttp__("MITRE_FOO"), "MITRE_FOO")
