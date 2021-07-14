#!/usr/bin/env python3

""" Logger for the attack side. Output must be flexible, because we want to be able to feed it into many different processes. From ML to analysts """

import json
import datetime


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

    def start_caldera_attack(self, source, paw, group, ability_id, ttp=None, name=None, description=None, obfuscator="default", jitter="default"):  # pylint: disable=too-many-arguments
        """ Mark the start of a caldera attack

        @param source: source of the attack. Attack IP
        @param paw: Caldera paw of the targets being attacked
        @param group: Caldera group of the targets being attacked
        @param ability_id: Caldera ability id of the attack
        @param ttp: TTP of the attack (as stated by Caldera internal settings)
        @param name: Name of the attack. Data source is Caldera internal settings
        @param description: Descirption of the attack. Caldera is the source
        @param obfuscator: C&C obfuscator being used
        @param jitter: Jitter being used
        """

        data = {"timestamp": self.__get_timestamp__(),
                "event": "start",
                "type": "attack",
                "sub-type": "caldera",
                "source": source,
                "target_paw": paw,
                "target_group": group,
                "ability_id": ability_id,
                "hunting_tag": __mitre_fix_ttp__(ttp),
                "name": name or "",
                "description": description or "",
                "obfuscator": obfuscator,
                "jitter": jitter
                }

        self.__add_to_log__(data)

    # TODO: Add parameter
    # TODO: Add config
    # TODO: Add results

    def stop_caldera_attack(self, source, paw, group, ability_id, ttp=None, name=None, description=None, obfuscator="default", jitter="default"):  # pylint: disable=too-many-arguments
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
                "sub-type": "caldera",
                "source": source,
                "target_paw": paw,
                "target_group": group,
                "ability_id": ability_id,
                "hunting_tag": __mitre_fix_ttp__(ttp),
                "name": name or "",
                "description": description or "",
                "obfuscator": obfuscator,
                "jitter": jitter
                }
        self.__add_to_log__(data)

    def start_file_write(self, source, target, file_name):
        """ Mark the start of a file being written to the target (payload !)

        @param source: source of the attack. Attack IP (empty if written from controller)
        @param target: Target machine of the attack
        @param file_name: Name of the file being written
        """

        data = {"timestamp": self.__get_timestamp__(),
                "event": "start",
                "type": "dropping_file",
                "sub-type": "by PurpleDome",
                "source": source,
                "target": target,
                "file_name": file_name
                }
        self.__add_to_log__(data)

    def stop_file_write(self, source, target, file_name):
        """ Mark the stop of a file being written to the target (payload !)

        @param source: source of the attack. Attack IP (empty if written from controller)
        @param target: Target machine of the attack
        @param attack_name: Name of the attack. From plugin
        @param file_name: Name of the file being written
        """

        data = {"timestamp": self.__get_timestamp__(),
                "event": "stop",
                "type": "dropping_file",
                "sub-type": "by PurpleDome",
                "source": source,
                "target": target,
                "file_name": file_name
                }
        self.__add_to_log__(data)

    def start_execute_payload(self, source, target, command):
        """ Mark the start of a payload being executed

        @param source: source of the attack. Attack IP (empty if written from controller)
        @param target: Target machine of the attack
        @param command: Name of the file being written
        """

        data = {"timestamp": self.__get_timestamp__(),
                "event": "start",
                "type": "execute_payload",
                "sub-type": "by PurpleDome",
                "source": source,
                "target": target,
                "command": command
                }
        self.__add_to_log__(data)

    def stop_execute_payload(self, source, target, command):
        """ Mark the stop of a payload being executed

        @param source: source of the attack. Attack IP (empty if written from controller)
        @param target: Target machine of the attack
        @param command: Name of the attack. From plugin
        @param file_name: Name of the file being written
        """

        data = {"timestamp": self.__get_timestamp__(),
                "event": "stop",
                "type": "execute_payload",
                "sub-type": "by PurpleDome",
                "source": source,
                "target": target,
                "command": command
                }
        self.__add_to_log__(data)

    def start_kali_attack(self, source, target, attack_name, ttp=None):
        """ Mark the start of a Kali based attack

        @param source: source of the attack. Attack IP
        @param target: Target machine of the attack
        @param attack_name: Name of the attack. From plugin
        @param ttp: TTP of the attack. From plugin
        """

        data = {"timestamp": self.__get_timestamp__(),
                "event": "start",
                "type": "attack",
                "sub-type": "kali",
                "source": source,
                "target": target,
                "kali_name": attack_name,
                "hunting_tag": __mitre_fix_ttp__(ttp),
                }
        self.__add_to_log__(data)

    # TODO: Add parameter
    # TODO: Add config
    # TODO: Add results

    def stop_kali_attack(self, source, target, attack_name, ttp=None):
        """ Mark the end of a Kali based attack

        @param source: source of the attack. Attack IP
        @param target: Target machine of the attack
        @param attack_name: Name of the attack. From plugin
        @param ttp: TTP of the attack. From plugin
        """

        data = {"timestamp": self.__get_timestamp__(),
                "event": "stop",
                "type": "attack",
                "sub-type": "kali",
                "source": source,
                "target": target,
                "kali_name": attack_name,
                "hunting_tag": __mitre_fix_ttp__(ttp),
                }
        self.__add_to_log__(data)

    def start_metasploit_attack(self, source, target, metasploit_command, ttp=None):
        """ Mark the start of a Metasploit based attack

        @param source: source of the attack. Attack IP
        @param target: Target machine of the attack
        @param metasploit_command: The command to metasploit
        @param ttp: TTP of the attack. From plugin
        """

        data = {"timestamp": self.__get_timestamp__(),
                "event": "start",
                "type": "attack",
                "sub-type": "metasploit",
                "source": source,
                "target": target,
                "metasploit_command": metasploit_command,
                "hunting_tag": __mitre_fix_ttp__(ttp),
                }
        self.__add_to_log__(data)

    def stop_metasploit_attack(self, source, target, metasploit_command, ttp=None):
        """ Mark the start of a Metasploit based attack

        @param source: source of the attack. Attack IP
        @param target: Target machine of the attack
        @param metasploit_command: The command to metasploit
        @param ttp: TTP of the attack. From plugin
        """

        data = {"timestamp": self.__get_timestamp__(),
                "event": "stop",
                "type": "attack",
                "sub-type": "metasploit",
                "source": source,
                "target": target,
                "metasploit_command": metasploit_command,
                "hunting_tag": __mitre_fix_ttp__(ttp),
                }
        self.__add_to_log__(data)

    def start_attack_plugin(self, source, target, plugin_name, ttp=None):
        """ Mark the start of an attack plugin

        @param source: source of the attack. Attack IP
        @param target: Target machine of the attack
        @param plugin_name: Name of the plugin
        @param ttp: TTP of the attack. From plugin
        """

        data = {"timestamp": self.__get_timestamp__(),
                "event": "start",
                "type": "attack",
                "sub-type": "attack_plugin",
                "source": source,
                "target": target,
                "plugin_name": plugin_name,
                "hunting_tag": __mitre_fix_ttp__(ttp),
                }
        self.__add_to_log__(data)

    # TODO: Add parameter
    # TODO: Add config
    # TODO: Add results

    def stop_attack_plugin(self, source, target, plugin_name, ttp=None):
        """ Mark the end of an attack plugin

        @param source: source of the attack. Attack IP
        @param target: Target machine of the attack
        @param plugin_name: Name of the plugin
        @param ttp: TTP of the attack. From plugin
        """

        data = {"timestamp": self.__get_timestamp__(),
                "event": "stop",
                "type": "attack",
                "sub-type": "attack_plugin",
                "source": source,
                "target": target,
                "plugin_name": plugin_name,
                "hunting_tag": __mitre_fix_ttp__(ttp),
                }
        self.__add_to_log__(data)

    def write_json(self, filename):
        """ Write the json data for this log

        @param filename: Name of the json file
        """
        with open(filename, "wt") as fh:
            json.dump(self.get_dict(), fh)

    def get_dict(self):
        """ Return logged data in dict format """

        return self.log

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
