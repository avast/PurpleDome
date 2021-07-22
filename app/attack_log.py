#!/usr/bin/env python3

""" Logger for the attack side. Output must be flexible, because we want to be able to feed it into many different processes. From ML to analysts """

import json
import datetime
from random import randint


def __mitre_fix_ttp__(ttp):
    """ enforce some systematic naming scheme for MITRE TTPs """

    if ttp is None:
        return ""

    if ttp.startswith("MITRE_"):
        return ttp

    return "MITRE_" + ttp


class AttackLog():
    """ A specific logger class to log the progress of the attack steps """

    def __init__(self, verbosity=0):
        """

        @param verbosity: verbosity setting from 0 to 3 for stdout printing
        """
        self.log = []
        self.verbosity = verbosity

        # TODO. As soon as someone wants custom timestamps, make the format variable
        self.datetime_format = "%H:%M:%S.%f"

    def __add_to_log__(self, item: dict):
        """ internal command to add a item to the log

        @param item: data chunk to add
        """

        self.log.append(item)

    def __get_timestamp__(self):
        """ Get the timestamp to add to the log entries. Currently not configurable """

        return datetime.datetime.now().strftime(self.datetime_format)

    def get_caldera_default_name(self, ability_id):
        """ Returns the default name for this ability based on a db """
        data = {"bd527b63-9f9e-46e0-9816-b8434d2b8989": "whoami"}
        if ability_id not in data:
            return None

        return data[ability_id]

    def get_caldera_default_description(self, ability_id):
        """ Returns the default description for this ability based on a db """

        data = {"bd527b63-9f9e-46e0-9816-b8434d2b8989": "Obtain user from current session"}
        if ability_id not in data:
            return None

        return data[ability_id]

    def get_caldera_default_tactics(self, ability_id):
        """ Returns the default tactics for this ability based on a db """

        data = {"bd527b63-9f9e-46e0-9816-b8434d2b8989": " System Owner/User Discovery"}
        if ability_id not in data:
            return None

        return data[ability_id]

    def get_caldera_default_tactics_id(self, ability_id):
        """ Returns the default name for this ability based on a db """

        data = {"bd527b63-9f9e-46e0-9816-b8434d2b8989": "T1033"}
        if ability_id not in data:
            return None

        return data[ability_id]

    def get_caldera_default_situation_description(self, ability_id):
        """ Returns the default situation description for this ability based on a db """

        data = {"bd527b63-9f9e-46e0-9816-b8434d2b8989": None}
        if ability_id not in data:
            return None

        return data[ability_id]

    def get_caldera_default_countermeasure(self, ability_id):
        """ Returns the default countermeasure for this ability based on a db """

        data = {"bd527b63-9f9e-46e0-9816-b8434d2b8989": None}
        if ability_id not in data:
            return None

        return data[ability_id]

    def start_caldera_attack(self, source, paw, group, ability_id, ttp=None, **kwargs):
        """ Mark the start of a caldera attack

        @param source: source of the attack. Attack IP
        @param paw: Caldera paw of the targets being attacked
        @param group: Caldera group of the targets being attacked
        @param ability_id: Caldera ability id of the attack
        @param ttp: TTP of the attack (as stated by Caldera internal settings)
        """

        timestamp = self.__get_timestamp__()
        logid = timestamp + "_" + str(randint(1, 100000))

        data = {"timestamp": timestamp,
                "timestamp_end": None,
                "event": "start",
                "type": "attack",
                "sub_type": "caldera",
                "source": source,
                "target_paw": paw,
                "target_group": group,
                "ability_id": ability_id,
                "hunting_tag": __mitre_fix_ttp__(ttp),
                "logid": logid,
                "name": kwargs.get("name", self.get_caldera_default_name(ability_id)),
                "description": kwargs.get("description", self.get_caldera_default_description(ability_id)),
                "tactics": kwargs.get("tactics", self.get_caldera_default_tactics(ability_id)),
                "tactics_id": kwargs.get("tactics_id", self.get_caldera_default_tactics_id(ability_id)),
                "situation_description": kwargs.get("situation_description", self.get_caldera_default_situation_description(ability_id)),  # Description for the situation this attack was run in. Set by the plugin or attacker emulation
                "countermeasure": kwargs.get("countermeasure", self.get_caldera_default_countermeasure(ability_id)),  # Set by the attack
                "obfuscator": kwargs.get("obfuscator", "default"),
                "jitter": kwargs.get("jitter", "default"),
                }

        self.__add_to_log__(data)

        return logid

    # TODO: Add parameter
    # TODO: Add config
    # TODO: Add results

    def stop_caldera_attack(self, source, paw, group, ability_id, ttp=None, **kwargs):
        """ Mark the end of a caldera attack

        @param source: source of the attack. Attack IP
        @param paw: Caldera oaw of the targets being attacked
        @param group: Caldera group of the targets being attacked
        @param ability_id: Caldera ability id of the attack
        @param ttp: TTP of the attack (as stated by Caldera internal settings)
        @param name: Name of the attack. Data source is Caldera internal settings
        @param description: Descirption of the attack. Caldera is the source
        @param obfuscator: C&C obfuscator being used
        @param jitter: Jitter being used
        """

        data = {"timestamp": self.__get_timestamp__(),
                "event": "stop",
                "type": "attack",
                "sub_type": "caldera",
                "source": source,
                "target_paw": paw,
                "target_group": group,
                "ability_id": ability_id,
                "hunting_tag": __mitre_fix_ttp__(ttp),
                "name": kwargs.get("name", ""),
                "description": kwargs.get("description", ""),
                "obfuscator": kwargs.get("obfuscator", "default"),
                "jitter": kwargs.get("jitter", "default"),
                "logid": kwargs.get("logid", None)
                }
        self.__add_to_log__(data)

    def start_file_write(self, source, target, file_name):
        """ Mark the start of a file being written to the target (payload !)

        @param source: source of the attack. Attack IP (empty if written from controller)
        @param target: Target machine of the attack
        @param file_name: Name of the file being written
        """

        timestamp = self.__get_timestamp__()
        logid = timestamp + "_" + str(randint(1, 100000))

        data = {"timestamp": timestamp,
                "timestamp_end": None,
                "event": "start",
                "type": "dropping_file",
                "sub_type": "by PurpleDome",
                "source": source,
                "target": target,
                "file_name": file_name,
                "logid": logid
                }
        self.__add_to_log__(data)
        return logid

    def stop_file_write(self, source, target, file_name, **kwargs):
        """ Mark the stop of a file being written to the target (payload !)

        @param source: source of the attack. Attack IP (empty if written from controller)
        @param target: Target machine of the attack
        @param attack_name: Name of the attack. From plugin
        @param file_name: Name of the file being written
        @param logid: logid of the corresponding start command

        kwargs: logid to link to start_file_write
        """

        data = {"timestamp": self.__get_timestamp__(),
                "event": "stop",
                "type": "dropping_file",
                "sub_type": "by PurpleDome",
                "source": source,
                "target": target,
                "file_name": file_name,
                "logid": kwargs.get("logid", None)
                }

        self.__add_to_log__(data)

    def start_execute_payload(self, source, target, command):
        """ Mark the start of a payload being executed

        @param source: source of the attack. Attack IP (empty if written from controller)
        @param target: Target machine of the attack
        @param command: Name of the file being written
        """

        timestamp = self.__get_timestamp__()
        logid = timestamp + "_" + str(randint(1, 100000))

        data = {"timestamp": timestamp,
                "timestamp_end": None,
                "event": "start",
                "type": "execute_payload",
                "sub_type": "by PurpleDome",
                "source": source,
                "target": target,
                "command": command,
                "logid": logid
                }
        self.__add_to_log__(data)

        return logid

    def stop_execute_payload(self, source, target, command, **kwargs):
        """ Mark the stop of a payload being executed

        @param source: source of the attack. Attack IP (empty if written from controller)
        @param target: Target machine of the attack
        @param command: Name of the attack. From plugin
        @param file_name: Name of the file being written
        @param kwargs: logid to link to start_file_write
        """

        data = {"timestamp": self.__get_timestamp__(),
                "event": "stop",
                "type": "execute_payload",
                "sub_type": "by PurpleDome",
                "source": source,
                "target": target,
                "command": command,
                "logid": kwargs.get("logid", None)
                }
        self.__add_to_log__(data)

    def start_kali_attack(self, source, target, attack_name, ttp=None, **kwargs):
        """ Mark the start of a Kali based attack

        @param source: source of the attack. Attack IP
        @param target: Target machine of the attack
        @param attack_name: Name of the attack. From plugin
        @param ttp: TTP of the attack. From plugin
        """

        timestamp = self.__get_timestamp__()
        logid = timestamp + "_" + str(randint(1, 100000))

        data = {"timestamp": timestamp,
                "timestamp_end": None,
                "event": "start",
                "type": "attack",
                "sub_type": "kali",
                "source": source,
                "target": target,
                "kali_name": attack_name,
                "hunting_tag": __mitre_fix_ttp__(ttp),
                "logid": logid,
                "name": kwargs.get("name", None),  # Human readable name of the attack
                "kali_command": kwargs.get("kali_command", None),
                "tactics": kwargs.get("tactics", None),
                "tactics_id": kwargs.get("tactics_id", None),
                "description": kwargs.get("description", None),  # Generic description for this attack. Set by the attack
                "situation_description": kwargs.get("situation_description", None),  # Description for the situation this attack was run in. Set by the plugin or attacker emulation
                "countermeasure": kwargs.get("countermeasure", None),  # Set by the attack
                }
        self.__add_to_log__(data)

        return logid

    # TODO: Add parameter
    # TODO: Add config
    # TODO: Add results

    def stop_kali_attack(self, source, target, attack_name, ttp=None, **kwargs):
        """ Mark the end of a Kali based attack

        @param source: source of the attack. Attack IP
        @param target: Target machine of the attack
        @param attack_name: Name of the attack. From plugin
        @param ttp: TTP of the attack. From plugin
        """

        data = {"timestamp": self.__get_timestamp__(),
                "event": "stop",
                "type": "attack",
                "sub_type": "kali",
                "source": source,
                "target": target,
                "kali_name": attack_name,
                "hunting_tag": __mitre_fix_ttp__(ttp),
                "logid": kwargs.get("logid", None)
                }
        self.__add_to_log__(data)

    def start_narration(self, text):
        """ Add some user defined narration. Can be used in plugins to describe the situation before and after the attack, ...
        At the moment there is no stop narration command. I do not think we need one. But I want to stick to the structure

        @param text: Text of the narration
        """

        timestamp = self.__get_timestamp__()
        logid = timestamp + "_" + str(randint(1, 100000))

        data = {"timestamp": timestamp,
                "event": "start",
                "type": "narration",
                "sub_type": "user defined narration",
                "text": text,
                }
        self.__add_to_log__(data)
        return logid

    def start_metasploit_attack(self, source, target, metasploit_command, ttp=None, **kwargs):
        """ Mark the start of a Metasploit based attack

        @param source: source of the attack. Attack IP
        @param target: Target machine of the attack
        @param metasploit_command: The command to metasploit
        @param ttp: TTP of the attack. From plugin
        """

        timestamp = self.__get_timestamp__()
        logid = timestamp + "_" + str(randint(1, 100000))

        data = {"timestamp": timestamp,
                "timestamp_end": None,
                "event": "start",
                "type": "attack",
                "sub_type": "metasploit",
                "source": source,
                "target": target,
                "metasploit_command": metasploit_command,
                "hunting_tag": __mitre_fix_ttp__(ttp),
                "logid": logid,
                "name": kwargs.get("name", None),  # Human readable name of the attack
                "tactics": kwargs.get("tactics", None),
                "tactics_id": kwargs.get("tactics_id", None),
                "description": kwargs.get("description", None),  # Generic description for this attack. Set by the attack
                "situation_description": kwargs.get("situation_description", None),  # Description for the situation this attack was run in. Set by the plugin or attacker emulation
                "countermeasure": kwargs.get("countermeasure", None),  # Set by the attack
                }
        self.__add_to_log__(data)

        return logid

    def stop_metasploit_attack(self, source, target, metasploit_command, ttp=None, **kwargs):
        """ Mark the start of a Metasploit based attack

        @param source: source of the attack. Attack IP
        @param target: Target machine of the attack
        @param metasploit_command: The command to metasploit
        @param ttp: TTP of the attack. From plugin
        """

        data = {"timestamp": self.__get_timestamp__(),
                "event": "stop",
                "type": "attack",
                "sub_type": "metasploit",
                "source": source,
                "target": target,
                "metasploit_command": metasploit_command,
                "hunting_tag": __mitre_fix_ttp__(ttp),
                "logid": kwargs.get("logid", None)
                }
        self.__add_to_log__(data)

    def start_attack_plugin(self, source, target, plugin_name, ttp=None):
        """ Mark the start of an attack plugin

        @param source: source of the attack. Attack IP
        @param target: Target machine of the attack
        @param plugin_name: Name of the plugin
        @param ttp: TTP of the attack. From plugin
        """

        timestamp = self.__get_timestamp__()
        logid = timestamp + "_" + str(randint(1, 100000))

        data = {"timestamp": timestamp,
                "timestamp_end": None,
                "event": "start",
                "type": "attack",
                "sub_type": "attack_plugin",
                "source": source,
                "target": target,
                "plugin_name": plugin_name,
                "hunting_tag": __mitre_fix_ttp__(ttp),
                "logid": logid
                }
        self.__add_to_log__(data)
        return logid

    # TODO: Add parameter
    # TODO: Add config
    # TODO: Add results

    def stop_attack_plugin(self, source, target, plugin_name, **kwargs):
        """ Mark the end of an attack plugin

        @param source: source of the attack. Attack IP
        @param target: Target machine of the attack
        @param plugin_name: Name of the plugin
        @param logid: logid of the corresponding start command
        @param kwargs: *ttp*, *logid*
        """

        data = {"timestamp": self.__get_timestamp__(),
                "event": "stop",
                "type": "attack",
                "sub_type": "attack_plugin",
                "source": source,
                "target": target,
                "plugin_name": plugin_name,
                "hunting_tag": __mitre_fix_ttp__(kwargs.get("ttp", None)),
                "logid": kwargs.get("logid", None)
                }
        self.__add_to_log__(data)

    def write_json(self, filename):
        """ Write the json data for this log

        @param filename: Name of the json file
        """
        with open(filename, "wt") as fh:
            json.dump(self.get_dict(), fh)

    def post_process(self):
        """ Post process the data before using it """

        for entry in self.log:
            if entry["event"] == "stop" and "logid" in entry and entry["logid"] is not None:
                # Search for matching start event and add timestamp
                logid = entry["logid"]
                for replace_entry in self.log:
                    if replace_entry["event"] == "start" and "logid" in replace_entry and replace_entry["logid"] == logid:
                        # Found matching start event. Updating it
                        replace_entry["timestamp_end"] = entry["timestamp"]

    def get_dict(self):
        """ Return logged data in dict format """

        return self.log

    # TODO: doc_start_environment

    # TODO: doc_describe_attack

    # TODO: doc_attack_step

    # TODO: Return full doc

    def vprint(self, text, verbosity):
        """ verbosity based stdout printing

        0: Errors only
        1: Main colored information
        2: Detailed progress information
        3: Debug logs, data dumps, everything

        @param text: The text to print
        @param verbosity: the verbosity level the text has.
        """

        if verbosity <= self.verbosity:
            print(text)
