#!/usr/bin/env python3

# Testing the attack log class

import unittest
from app.attack_log import AttackLog
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
