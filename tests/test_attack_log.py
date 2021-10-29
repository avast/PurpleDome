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

        default = {"boilerplate": {'log_format_major_version': 1, 'log_format_minor_version': 1},
                   "system_overview": [],
                   "attack_log": []}
        self.assertEqual(al.get_dict(), default)

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
        self.assertEqual(data["attack_log"][0]["event"], "start")
        self.assertEqual(data["attack_log"][0]["type"], "attack")
        self.assertEqual(data["attack_log"][0]["sub_type"], "caldera")
        self.assertEqual(data["attack_log"][0]["source"], source)
        self.assertEqual(data["attack_log"][0]["target_paw"], paw)
        self.assertEqual(data["attack_log"][0]["target_group"], group)
        self.assertEqual(data["attack_log"][0]["ability_id"], ability_id)
        self.assertEqual(data["attack_log"][0]["hunting_tag"], "MITRE_" + ttp)
        self.assertEqual(data["attack_log"][0]["name"], name)
        self.assertEqual(data["attack_log"][0]["description"], description)

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
        self.assertEqual(data["attack_log"][0]["event"], "stop")
        self.assertEqual(data["attack_log"][0]["type"], "attack")
        self.assertEqual(data["attack_log"][0]["sub_type"], "caldera")
        self.assertEqual(data["attack_log"][0]["source"], source)
        self.assertEqual(data["attack_log"][0]["target_paw"], paw)
        self.assertEqual(data["attack_log"][0]["target_group"], group)
        self.assertEqual(data["attack_log"][0]["ability_id"], ability_id)
        self.assertEqual(data["attack_log"][0]["hunting_tag"], "MITRE_" + ttp)
        self.assertEqual(data["attack_log"][0]["name"], name)
        self.assertEqual(data["attack_log"][0]["description"], description)

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
        self.assertEqual(data["attack_log"][0]["event"], "start")
        self.assertEqual(data["attack_log"][0]["type"], "attack")
        self.assertEqual(data["attack_log"][0]["sub_type"], "kali")
        self.assertEqual(data["attack_log"][0]["source"], source)
        self.assertEqual(data["attack_log"][0]["target"], target)
        self.assertEqual(data["attack_log"][0]["kali_name"], attack_name)
        self.assertEqual(data["attack_log"][0]["hunting_tag"], "MITRE_" + ttp)

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
        self.assertEqual(data["attack_log"][0]["event"], "stop")
        self.assertEqual(data["attack_log"][0]["type"], "attack")
        self.assertEqual(data["attack_log"][0]["sub_type"], "kali")
        self.assertEqual(data["attack_log"][0]["source"], source)
        self.assertEqual(data["attack_log"][0]["target"], target)
        self.assertEqual(data["attack_log"][0]["kali_name"], attack_name)
        self.assertEqual(data["attack_log"][0]["hunting_tag"], "MITRE_" + ttp)

    def test_narration_start(self):
        """ Starting a narration """
        al = AttackLog()
        text = "texttextext"

        al.start_narration(text
                           )
        data = al.get_dict()
        self.assertEqual(data["attack_log"][0]["event"], "start")
        self.assertEqual(data["attack_log"][0]["type"], "narration")
        self.assertEqual(data["attack_log"][0]["sub_type"], "user defined narration")
        self.assertEqual(data["attack_log"][0]["text"], text)

    def test_build_start(self):
        """ Starting a build """
        al = AttackLog()
        dl_uri = "asource"
        dl_uris = "a target"
        payload = "1234"
        platform = "a name"
        architecture = "arch"
        lhost = "lhost"
        lport = 8080
        filename = "afilename"
        encoding = "encoded"
        encoded_filename = "ef"
        sRDI_conversion = True
        for_step = 4
        comment = "this is a comment"

        al.start_build(dl_uri=dl_uri,
                       dl_uris=dl_uris,
                       payload=payload,
                       platform=platform,
                       architecture=architecture,
                       lhost=lhost,
                       lport=lport,
                       filename=filename,
                       encoding=encoding,
                       encoded_filename=encoded_filename,
                       sRDI_conversion=sRDI_conversion,
                       for_step=for_step,
                       comment=comment
                       )
        data = al.get_dict()
        self.assertEqual(data["attack_log"][0]["event"], "start")
        self.assertEqual(data["attack_log"][0]["type"], "build")
        self.assertEqual(data["attack_log"][0]["dl_uri"], dl_uri)
        self.assertEqual(data["attack_log"][0]["dl_uris"], dl_uris)
        self.assertEqual(data["attack_log"][0]["payload"], payload)
        self.assertEqual(data["attack_log"][0]["platform"], platform)
        self.assertEqual(data["attack_log"][0]["architecture"], architecture)
        self.assertEqual(data["attack_log"][0]["lhost"], lhost)
        self.assertEqual(data["attack_log"][0]["lport"], lport)
        self.assertEqual(data["attack_log"][0]["filename"], filename)
        self.assertEqual(data["attack_log"][0]["encoding"], encoding)
        self.assertEqual(data["attack_log"][0]["encoded_filename"], encoded_filename)
        self.assertEqual(data["attack_log"][0]["sRDI_conversion"], sRDI_conversion)
        self.assertEqual(data["attack_log"][0]["for_step"], for_step)
        self.assertEqual(data["attack_log"][0]["comment"], comment)

    def test_build_start_default(self):
        """ Starting a build default values"""
        al = AttackLog()

        al.start_build()
        data = al.get_dict()
        self.assertEqual(data["attack_log"][0]["event"], "start")
        self.assertEqual(data["attack_log"][0]["type"], "build")
        self.assertEqual(data["attack_log"][0]["dl_uri"], None)
        self.assertEqual(data["attack_log"][0]["dl_uris"], None)
        self.assertEqual(data["attack_log"][0]["payload"], None)
        self.assertEqual(data["attack_log"][0]["platform"], None)
        self.assertEqual(data["attack_log"][0]["architecture"], None)
        self.assertEqual(data["attack_log"][0]["lhost"], None)
        self.assertEqual(data["attack_log"][0]["lport"], None)
        self.assertEqual(data["attack_log"][0]["filename"], None)
        self.assertEqual(data["attack_log"][0]["encoding"], None)
        self.assertEqual(data["attack_log"][0]["encoded_filename"], None)
        self.assertEqual(data["attack_log"][0]["sRDI_conversion"], False)
        self.assertEqual(data["attack_log"][0]["for_step"], None)
        self.assertEqual(data["attack_log"][0]["comment"], None)

    def test_build_stop(self):
        """ Stopping a build """
        al = AttackLog()
        logid = "lid"

        al.stop_build(logid=logid)
        data = al.get_dict()
        self.assertEqual(data["attack_log"][0]["event"], "stop")
        self.assertEqual(data["attack_log"][0]["type"], "build")
        self.assertEqual(data["attack_log"][0]["logid"], logid)

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
        self.assertEqual(data["attack_log"][0]["event"], "start")
        self.assertEqual(data["attack_log"][0]["type"], "attack")
        self.assertEqual(data["attack_log"][0]["sub_type"], "metasploit")
        self.assertEqual(data["attack_log"][0]["source"], source)
        self.assertEqual(data["attack_log"][0]["target"], target)
        self.assertEqual(data["attack_log"][0]["metasploit_command"], attack_name)
        self.assertEqual(data["attack_log"][0]["hunting_tag"], "MITRE_" + ttp)

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
        self.assertEqual(data["attack_log"][0]["event"], "stop")
        self.assertEqual(data["attack_log"][0]["type"], "attack")
        self.assertEqual(data["attack_log"][0]["sub_type"], "metasploit")
        self.assertEqual(data["attack_log"][0]["source"], source)
        self.assertEqual(data["attack_log"][0]["target"], target)
        self.assertEqual(data["attack_log"][0]["metasploit_command"], attack_name)
        self.assertEqual(data["attack_log"][0]["hunting_tag"], "MITRE_" + ttp)

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
        self.assertEqual(data["attack_log"][0]["event"], "start")
        self.assertEqual(data["attack_log"][0]["type"], "attack")
        self.assertEqual(data["attack_log"][0]["sub_type"], "attack_plugin")
        self.assertEqual(data["attack_log"][0]["source"], source)
        self.assertEqual(data["attack_log"][0]["target"], target)
        self.assertEqual(data["attack_log"][0]["plugin_name"], attack_name)
        self.assertEqual(data["attack_log"][0]["hunting_tag"], "MITRE_" + ttp)

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
        self.assertEqual(data["attack_log"][0]["event"], "stop")
        self.assertEqual(data["attack_log"][0]["type"], "attack")
        self.assertEqual(data["attack_log"][0]["sub_type"], "attack_plugin")
        self.assertEqual(data["attack_log"][0]["source"], source)
        self.assertEqual(data["attack_log"][0]["target"], target)
        self.assertEqual(data["attack_log"][0]["plugin_name"], attack_name)
        self.assertEqual(data["attack_log"][0]["hunting_tag"], "MITRE_" + ttp)

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
        self.assertEqual(data["attack_log"][0]["event"], "start")
        self.assertEqual(data["attack_log"][0]["type"], "dropping_file")
        self.assertEqual(data["attack_log"][0]["sub_type"], "by PurpleDome")
        self.assertEqual(data["attack_log"][0]["source"], source)
        self.assertEqual(data["attack_log"][0]["target"], target)
        self.assertEqual(data["attack_log"][0]["file_name"], file_name)

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
        self.assertEqual(data["attack_log"][0]["event"], "stop")
        self.assertEqual(data["attack_log"][0]["type"], "dropping_file")
        self.assertEqual(data["attack_log"][0]["sub_type"], "by PurpleDome")
        self.assertEqual(data["attack_log"][0]["source"], source)
        self.assertEqual(data["attack_log"][0]["target"], target)
        self.assertEqual(data["attack_log"][0]["file_name"], file_name)

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
        self.assertEqual(data["attack_log"][0]["event"], "start")
        self.assertEqual(data["attack_log"][0]["type"], "execute_payload")
        self.assertEqual(data["attack_log"][0]["sub_type"], "by PurpleDome")
        self.assertEqual(data["attack_log"][0]["source"], source)
        self.assertEqual(data["attack_log"][0]["target"], target)
        self.assertEqual(data["attack_log"][0]["command"], command)

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
        self.assertEqual(data["attack_log"][0]["event"], "stop")
        self.assertEqual(data["attack_log"][0]["type"], "execute_payload")
        self.assertEqual(data["attack_log"][0]["sub_type"], "by PurpleDome")
        self.assertEqual(data["attack_log"][0]["source"], source)
        self.assertEqual(data["attack_log"][0]["target"], target)
        self.assertEqual(data["attack_log"][0]["command"], command)

    def test_mitre_fix_ttp_is_none(self):
        """ Testing the mitre ttp fix for ttp being none """
        self.assertEqual(app.attack_log.__mitre_fix_ttp__(None), "")

    def test_mitre_fix_ttp_is_MITRE_SOMETHING(self):
        """ Testing the mitre ttp fix for ttp being MITRE_ """
        self.assertEqual(app.attack_log.__mitre_fix_ttp__("MITRE_FOO"), "MITRE_FOO")

    # tests for a bunch of default data covering caldera attacks. That way we will have some fallback if no data is submitted:
    def test_get_caldera_default_name_missing(self):
        """ Testing getting the caldera default name """
        al = AttackLog()
        self.assertEqual(al.get_caldera_default_name("missing"), None)

    def test_get_caldera_default_name(self):
        """ Testing getting the caldera default name """
        al = AttackLog()
        self.assertEqual(al.get_caldera_default_name("bd527b63-9f9e-46e0-9816-b8434d2b8989"), "whoami")

    def test_get_caldera_default_description_missing(self):
        """ Testing getting the caldera default description """
        al = AttackLog()
        self.assertEqual(al.get_caldera_default_description("missing"), None)

    def test_get_caldera_default_description(self):
        """ Testing getting the caldera default description """
        al = AttackLog()
        self.assertEqual(al.get_caldera_default_description("bd527b63-9f9e-46e0-9816-b8434d2b8989"), "Obtain user from current session")

    def test_get_caldera_default_tactics_missing(self):
        """ Testing getting the caldera default tactics """
        al = AttackLog()
        self.assertEqual(al.get_caldera_default_tactics("missing", None), None)

    def test_get_caldera_default_tactics(self):
        """ Testing getting the caldera default tactics """
        al = AttackLog()
        self.assertEqual(al.get_caldera_default_tactics("bd527b63-9f9e-46e0-9816-b8434d2b8989", None), "System Owner/User Discovery")

    def test_get_caldera_default_tactics_id_missing(self):
        """ Testing getting the caldera default tactics_id """
        al = AttackLog()
        self.assertEqual(al.get_caldera_default_tactics_id("missing", None), None)

    def test_get_caldera_default_tactics_id(self):
        """ Testing getting the caldera default tactics_id """
        al = AttackLog()
        self.assertEqual(al.get_caldera_default_tactics_id("bd527b63-9f9e-46e0-9816-b8434d2b8989", None), "T1033")

    def test_get_caldera_default_situation_description_missing(self):
        """ Testing getting the caldera default situation_description """
        al = AttackLog()
        self.assertEqual(al.get_caldera_default_situation_description("missing"), None)

    def test_get_caldera_default_situation_description(self):
        """ Testing getting the caldera default situation_description """
        al = AttackLog()
        self.assertEqual(al.get_caldera_default_situation_description("bd527b63-9f9e-46e0-9816-b8434d2b8989"), None)

    def test_get_caldera_default_countermeasure_missing(self):
        """ Testing getting the caldera default countermeasure """
        al = AttackLog()
        self.assertEqual(al.get_caldera_default_countermeasure("missing"), None)

    def test_get_caldera_default_countermeasure(self):
        """ Testing getting the caldera default countermeasure """
        al = AttackLog()
        self.assertEqual(al.get_caldera_default_countermeasure("bd527b63-9f9e-46e0-9816-b8434d2b8989"), None)
