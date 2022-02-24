#!/usr/bin/env python3

""" Logger for the attack side. Output must be flexible, because we want to be able to feed it into many different processes. From ML to analysts """

from inspect import currentframe, getsourcefile
import json
import datetime
from random import randint
from typing import Optional


def __mitre_fix_ttp__(ttp: Optional[str]) -> str:
    """ enforce some systematic naming scheme for MITRE TTPs """

    if ttp is None:
        return ""

    if ttp.startswith("MITRE_"):
        return ttp

    return "MITRE_" + ttp


class AttackLog():
    """ A specific logger class to log the progress of the attack steps """

    def __init__(self, verbosity: int = 0):
        """

        :param verbosity: verbosity setting from 0 to 3 for stdout printing
        """
        self.log: list[dict] = []
        self.machines: list[dict] = []
        self.verbosity = verbosity

        self.datetime_format = "%H:%M:%S.%f"

    def __add_to_log__(self, item: dict) -> None:
        """ internal command to add a item to the log

        :param item: data chunk to add
        """

        self.log.append(item)

    def __get_timestamp__(self) -> str:
        """ Get the timestamp to add to the log entries. Currently not configurable """

        return datetime.datetime.now().strftime(self.datetime_format)

    def get_caldera_default_name(self, ability_id: str) -> Optional[str]:
        """ Returns the default name for this ability based on a db """

        # TODO: Add a proper database. At least an external file

        data = {"bd527b63-9f9e-46e0-9816-b8434d2b8989": "whoami"}
        if ability_id not in data:
            return None

        return data[ability_id]

    def get_caldera_default_description(self, ability_id: str) -> Optional[str]:
        """ Returns the default description for this ability based on a db """

        # TODO: Add a proper database. At least an external file

        data = {"bd527b63-9f9e-46e0-9816-b8434d2b8989": "Obtain user from current session",
                "697e8a432031075e47cccba24417013d": "Copy a VBS file to several startup folders",
                "f39161b2fa5d692ebe3972e0680a8f97": "Copy a BAT file to several startup folders",
                "16e6823c4656f5cd155051f5f1e5d6ad": "Copy a JSE file to several startup folders",
                "443b853ac50a79fc4a85354cb2c90fa2": "Set Regky RunOnce\\0001\\Depend to run a dll",
                "2bfafbee8e3edb25974a5d1aa3d9f431": "Set Regky RunOnce\\0001\\Depend , download a bat",
                "163b023f43aba758d36f524d146cb8ea": "Set Regkey CurrentVersion\\Run to start a exe"}
        if ability_id not in data:
            return None

        return data[ability_id]

    def get_caldera_default_tactics(self, ability_id: str, ttp: Optional[str]) -> Optional[str]:
        """ Returns the default tactics for this ability based on a db """

        # TODO: Add a proper database. At least an external file

        data = {"bd527b63-9f9e-46e0-9816-b8434d2b8989": "System Owner/User Discovery",
                "f39161b2fa5d692ebe3972e0680a8f97": "Persistence",
                "16e6823c4656f5cd155051f5f1e5d6ad": "Persistence",
                "443b853ac50a79fc4a85354cb2c90fa2": "Persistence",
                "2bfafbee8e3edb25974a5d1aa3d9f431": "Persistence",
                "163b023f43aba758d36f524d146cb8ea": "Persistence",
                "697e8a432031075e47cccba24417013d": "Persistence"}

        ttp_data = {"t1547": "Persistence",
                    "t1547.001": "Persistence",
                    "t1547.004": "Persistence",
                    "t1547.005": "Persistence",
                    "t1547.009": "Persistence",
                    "t1547.010": "Persistence"}

        if ability_id in data:
            return data[ability_id]

        if ttp is not None:
            if ttp.lower() in ttp_data:
                return ttp_data[ttp.lower()]

        return None

    def get_caldera_default_tactics_id(self, ability_id: str, ttp: Optional[str]) -> Optional[str]:
        """ Returns the default name for this ability based on a db """

        # TODO: Add a proper database. At least an external file

        data = {"bd527b63-9f9e-46e0-9816-b8434d2b8989": "T1033",
                "f39161b2fa5d692ebe3972e0680a8f97": "TA0003",
                "16e6823c4656f5cd155051f5f1e5d6ad": "TA0003",
                "443b853ac50a79fc4a85354cb2c90fa2": "TA0003",
                "2bfafbee8e3edb25974a5d1aa3d9f431": "TA0003",
                "163b023f43aba758d36f524d146cb8ea": "TA0003",
                "697e8a432031075e47cccba24417013d": "TA0003"}

        ttp_data = {"t1547": "TA0003",
                    "t1547.001": "TA0003",
                    "t1547.004": "TA0003",
                    "t1547.005": "TA0003",
                    "t1547.009": "TA0003",
                    "t1547.010": "TA0003"}

        if ability_id in data:
            return data[ability_id]

        if ttp is not None:
            if ttp.lower() in ttp_data:
                return ttp_data[ttp.lower()]

        return None

    def get_caldera_default_situation_description(self, ability_id: str) -> Optional[str]:
        """ Returns the default situation description for this ability based on a db """

        # TODO: Add a proper database. At least an external file

        data = {"bd527b63-9f9e-46e0-9816-b8434d2b8989": None,
                "697e8a432031075e47cccba24417013d": None,
                "f39161b2fa5d692ebe3972e0680a8f97": None,
                "16e6823c4656f5cd155051f5f1e5d6ad": None,
                "443b853ac50a79fc4a85354cb2c90fa2": None,
                "2bfafbee8e3edb25974a5d1aa3d9f431": None,
                "163b023f43aba758d36f524d146cb8ea": None}
        if ability_id not in data:
            return None

        return data[ability_id]

    def get_caldera_default_countermeasure(self, ability_id: str) -> Optional[str]:
        """ Returns the default countermeasure for this ability based on a db

        :returns: Default countermeasure as string. Or None if not found
        """

        # TODO: Add a proper database. At least an external file

        data = {"bd527b63-9f9e-46e0-9816-b8434d2b8989": None,
                "697e8a432031075e47cccba24417013d": None,
                "f39161b2fa5d692ebe3972e0680a8f97": None,
                "16e6823c4656f5cd155051f5f1e5d6ad": None,
                "443b853ac50a79fc4a85354cb2c90fa2": None,
                "2bfafbee8e3edb25974a5d1aa3d9f431": None,
                "163b023f43aba758d36f524d146cb8ea": None}
        if ability_id not in data:
            return None

        return data[ability_id]

    def start_caldera_attack(self, source: str, paw: str, group: str, ability_id: str, ttp: Optional[str] = None, **kwargs: dict) -> str:
        """ Mark the start of a caldera attack

        :param source: source of the attack. Attack IP
        :param paw: Caldera paw of the targets being attacked
        :param group: Caldera group of the targets being attacked
        :param ability_id: Caldera ability id of the attack
        :param ttp: TTP of the attack (as stated by Caldera internal settings)
        :returns: logid
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
                "tactics": kwargs.get("tactics", self.get_caldera_default_tactics(ability_id, ttp)),
                "tactics_id": kwargs.get("tactics_id", self.get_caldera_default_tactics_id(ability_id, ttp)),
                "situation_description": kwargs.get("situation_description", self.get_caldera_default_situation_description(ability_id)),  # Description for the situation this attack was run in. Set by the plugin or attacker emulation
                "countermeasure": kwargs.get("countermeasure", self.get_caldera_default_countermeasure(ability_id)),  # Set by the attack
                "obfuscator": kwargs.get("obfuscator", "default"),
                "jitter": kwargs.get("jitter", "default"),
                "result": None,
                }

        self.__add_to_log__(data)

        return logid

    # TODO: Add parameter
    # TODO: Add config
    # TODO: Add results

    def stop_caldera_attack(self, source: str, paw: str, group: str, ability_id: str, ttp: str = None, **kwargs: dict) -> None:
        """ Mark the end of a caldera attack

        :param source: source of the attack. Attack IP
        :param paw: Caldera oaw of the targets being attacked
        :param group: Caldera group of the targets being attacked
        :param ability_id: Caldera ability id of the attack
        :param ttp: TTP of the attack (as stated by Caldera internal settings)
        :param name: Name of the attack. Data source is Caldera internal settings
        :param description: Descirption of the attack. Caldera is the source
        :param obfuscator: C&C obfuscator being used
        :param jitter: Jitter being used
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
                "logid": kwargs.get("logid", None),
                "result": kwargs.get("result", None),
                }
        self.__add_to_log__(data)

    def start_file_write(self, source: str, target: str, file_name: str) -> str:
        """ Mark the start of a file being written to the target (payload !)

        :param source: source of the attack. Attack IP (empty if written from controller)
        :param target: Target machine of the attack
        :param file_name: Name of the file being written
        :returns: logid
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

    def stop_file_write(self, source: str, target: str, file_name: str, **kwargs: dict) -> None:
        """ Mark the stop of a file being written to the target (payload !)

        :param source: source of the attack. Attack IP (empty if written from controller)
        :param target: Target machine of the attack
        :param attack_name: Name of the attack. From plugin
        :param file_name: Name of the file being written
        :param logid: logid of the corresponding start command

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

    def start_execute_payload(self, source: str, target: str, command: str) -> str:
        """ Mark the start of a payload being executed

        :param source: source of the attack. Attack IP (empty if written from controller)
        :param target: Target machine of the attack
        :param command:
        :returns: logid
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

    def stop_execute_payload(self, source: str, target: str, command: str, **kwargs: dict) -> None:
        """ Mark the stop of a payload being executed

        :param source: source of the attack. Attack IP (empty if written from controller)
        :param target: Target machine of the attack
        :param command: Name of the attack. From plugin
        :param file_name: Name of the file being written
        :param kwargs: logid to link to start_file_write
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

    def start_kali_attack(self, source: str, target: str, attack_name: str, ttp: Optional[str] = None, **kwargs: dict) -> str:
        """ Mark the start of a Kali based attack

        :param source: source of the attack. Attack IP
        :param target: Target machine of the attack
        :param attack_name: Name of the attack. From plugin
        :param ttp: TTP of the attack. From plugin
        :returns: logid
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
                "result": None,
                }
        self.__add_to_log__(data)

        return logid

    def stop_kali_attack(self, source: str, target: str, attack_name: str, ttp: Optional[str] = None, **kwargs: dict) -> None:
        """ Mark the end of a Kali based attack

        :param source: source of the attack. Attack IP
        :param target: Target machine of the attack
        :param attack_name: Name of the attack. From plugin
        :param ttp: TTP of the attack. From plugin
        """

        data = {"timestamp": self.__get_timestamp__(),
                "event": "stop",
                "type": "attack",
                "sub_type": "kali",
                "source": source,
                "target": target,
                "kali_name": attack_name,
                "hunting_tag": __mitre_fix_ttp__(ttp),
                "logid": kwargs.get("logid", None),
                "result": kwargs.get("result", None),
                }
        self.__add_to_log__(data)

    def start_narration(self, text: str) -> str:
        """ Add some user defined narration. Can be used in plugins to describe the situation before and after the attack, ...
        At the moment there is no stop narration command. I do not think we need one. But I want to stick to the structure

        :param text: Text of the narration
        :returns: logid
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

    def start_attack_step(self, text: str) -> str:
        """ Mark the start of an attack step (several attacks in a chunk)

        :param text: description of the attack step being started
        :returns: logid
        """

        timestamp = self.__get_timestamp__()
        logid = timestamp + "_" + str(randint(1, 100000))

        data = {"timestamp": timestamp,
                "timestamp_end": None,
                "event": "start",
                "type": "attack_step",
                "sub_type": "user defined attack step",
                "text": text,
                "logid": logid,
                }
        self.__add_to_log__(data)

        return logid

    def stop_attack_step(self, text: str, **kwargs: dict) -> None:
        """ Mark the end of an attack step (several attacks in a chunk)

        :param text: description of the attack step being stopped
        """

        data = {"timestamp": self.__get_timestamp__(),
                "event": "stop",
                "type": "attack_step",
                "sub_type": "user defined attack step",
                "text": text,
                "logid": kwargs.get("logid", None)
                }
        self.__add_to_log__(data)

    def start_build(self, **kwargs: dict) -> str:
        """ Mark the start of a tool building/compilation process

        :returns: logid
        """

        timestamp = self.__get_timestamp__()
        logid = timestamp + "_" + str(randint(1, 100000))

        data = {"timestamp": timestamp,
                "timestamp_end": None,
                "event": "start",
                "type": "build",
                # "sub_type": "",
                "logid": logid,
                "dl_uri": kwargs.get("dl_uri", None),
                "dl_uris": kwargs.get("dl_uris", None),
                "payload": kwargs.get("payload", None),
                "platform": kwargs.get("platform", None),
                "architecture": kwargs.get("architecture", None),
                "lhost": kwargs.get("lhost", None),
                "lport": kwargs.get("lport", None),
                "filename": kwargs.get("filename", None),
                "encoding": kwargs.get("encoding", None),
                "encoded_filename": kwargs.get("encoded_filename", None),
                "sRDI_conversion": kwargs.get("sRDI_conversion", False),
                "for_step": kwargs.get("for_step", None),
                "comment": kwargs.get("comment", None),
                }
        self.__add_to_log__(data)

        return logid

    def stop_build(self, **kwargs: dict) -> None:
        """ Mark the end of a tool building/compilation process

        :param source: source of the attack. Attack IP
        :param target: Target machine of the attack
        :param attack_name: Name of the attack. From plugin
        :param ttp: TTP of the attack. From plugin
        """

        data = {"timestamp": self.__get_timestamp__(),
                "event": "stop",
                "type": "build",
                # "sub_type": "",
                "logid": kwargs.get("logid", None)
                }
        self.__add_to_log__(data)

    def start_metasploit_attack(self, source: str, target: str, metasploit_command: str, ttp: str = None, **kwargs: dict) -> str:
        """ Mark the start of a Metasploit based attack

        :param source: source of the attack. Attack IP
        :param target: Target machine of the attack
        :param metasploit_command: The command to metasploit
        :param ttp: TTP of the attack. From plugin
        :returns: logid
        """

        timestamp = self.__get_timestamp__()
        logid = timestamp + "_" + str(randint(1, 100000))

        cframe = currentframe()
        default_sourcefile = ""
        if cframe is not None:
            if cframe.f_back is not None:
                default_sourcefile = getsourcefile(cframe.f_back) or ""

        default_sourceline = -1
        if cframe is not None:
            if cframe.f_back is not None:
                default_sourceline = cframe.f_back.f_lineno

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
                "result": None,
                "sourcefile": kwargs.get("sourcefile", default_sourcefile),
                "sourceline": kwargs.get("sourceline", default_sourceline)
                }
        self.__add_to_log__(data)

        return logid

    def stop_metasploit_attack(self, source: str, target: str, metasploit_command: str, ttp: str = None, **kwargs: None) -> None:
        """ Mark the start of a Metasploit based attack

        :param source: source of the attack. Attack IP
        :param target: Target machine of the attack
        :param metasploit_command: The command to metasploit
        :param ttp: TTP of the attack. From plugin
        """

        data = {"timestamp": self.__get_timestamp__(),
                "event": "stop",
                "type": "attack",
                "sub_type": "metasploit",
                "source": source,
                "target": target,
                "metasploit_command": metasploit_command,
                "hunting_tag": __mitre_fix_ttp__(ttp),
                "logid": kwargs.get("logid", None),
                "result": kwargs.get("result", None)
                }
        self.__add_to_log__(data)

    def start_attack_plugin(self, source: str, target: str, plugin_name: str, ttp: str = None) -> str:
        """ Mark the start of an attack plugin

        :param source: source of the attack. Attack IP
        :param target: Target machine of the attack
        :param plugin_name: Name of the plugin
        :param ttp: TTP of the attack. From plugin
        :returns: logid
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

    def stop_attack_plugin(self, source: str, target: str, plugin_name: str, **kwargs: dict) -> None:
        """ Mark the end of an attack plugin

        :param source: source of the attack. Attack IP
        :param target: Target machine of the attack
        :param plugin_name: Name of the plugin
        :param logid: logid of the corresponding start command
        :param kwargs: *ttp*, *logid*
        """

        tag: Optional[str] = None
        if kwargs.get("ttp", None) is not None:
            tag = str(kwargs.get("ttp", None))

        data = {"timestamp": self.__get_timestamp__(),
                "event": "stop",
                "type": "attack",
                "sub_type": "attack_plugin",
                "source": source,
                "target": target,
                "plugin_name": plugin_name,
                "hunting_tag": __mitre_fix_ttp__(tag),
                "logid": kwargs.get("logid", None)
                }
        self.__add_to_log__(data)

    def write_json(self, filename: str) -> None:
        """ Write the json data for this log

        :param filename: Name of the json file
        """
        with open(filename, "wt") as fh:
            json.dump(self.get_dict(), fh)

    def post_process(self) -> None:
        """ Post process the data before using it """

        for entry in self.log:
            if entry["event"] == "stop" and "logid" in entry and entry["logid"] is not None:
                # Search for matching start event and add timestamp
                logid = entry["logid"]
                for replace_entry in self.log:
                    if replace_entry["event"] == "start" and "logid" in replace_entry and replace_entry["logid"] == logid:
                        # Found matching start event. Updating it
                        replace_entry["timestamp_end"] = entry["timestamp"]
                        if "result" in entry:
                            replace_entry["result"] = entry["result"]

    def get_dict(self) -> dict:
        """ Return logged data in dict format """

        res = {"boilerplate": {"log_format_major_version": 1,  # Changes on changes that breaks readers (items are modified or deleted)
                               "log_format_minor_version": 1   # Changes even if just new data is added
                               },
               "system_overview": self.machines,
               "attack_log": self.log
               }

        return res

    def add_machine_info(self, machine_info: dict) -> None:
        """ Adds a dict with machine info. One machine per call of this method """
        self.machines.append(machine_info)

    # TODO: doc_start_environment

    # TODO: doc_describe_attack

    # TODO: doc_attack_step

    # TODO: Return full doc

    def vprint(self, text: str, verbosity: int) -> None:
        """ verbosity based stdout printing

        0: Errors only
        1: Main colored information
        2: Detailed progress information
        3: Debug logs, data dumps, everything

        :param text: The text to print
        :param verbosity: the verbosity level the text has.
        """

        if verbosity <= self.verbosity:
            print(text)
