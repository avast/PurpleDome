#!/usr/bin/env python3

""" Logger for the attack side. Output must be flexible, because we want to be able to feed it into many different processes. From ML to analysts """

import json
import datetime


def __get_timestamp__():
    return datetime.datetime.now().strftime("%H:%M:%S.%f")


def __mitre_fix_ttp__(ttp):
    """ enforce some systematic naming scheme for MITRE TTPs """

    if ttp is None:
        return ""

    if ttp.startswith("MITRE_"):
        return ttp
    else:
        return "MITRE_" + ttp


class AttackLog():
    """ A specific logger class to log the progress of the attack steps """

    def __init__(self, verbosity=0):
        """

        @param verbosity: verbosity setting from 0 to 3 for stdout printing
        """
        self.log = []
        self.verbosity = verbosity

    def start_caldera_attack(self, source, paw, group, ability_id, ttp=None, name=None, description=None):  # pylint: disable=too-many-arguments
        """ Mark the start of a caldera attack

        @param source: source of the attack. Attack IP
        @param paw: Caldera paw of the targets being attacked
        @param group: Caldera group of the targets being attacked
        @param ability_id: Caldera ability id of the attack
        @param ttp: TTP of the attack (as stated by Caldera internal settings)
        @param name: Name of the attack. Data source is Caldera internal settings
        @param description: Descirption of the attack. Caldera is the source
        """

        data = {"timestamp": __get_timestamp__(),
                "event": "start",
                "type": "attack",
                "sub-type": "caldera",
                "source": source,
                "target_paw": paw,
                "target_group": group,
                "ability_id": ability_id,
                "hunting_tag": __mitre_fix_ttp__(ttp),
                "name": name or "",
                "description": description or ""
                }

        self.log.append(data)

    # TODO: Add parameter
    # TODO: Add config
    # TODO: Add results

    def stop_caldera_attack(self, source, paw, group, ability_id, ttp=None, name=None, description=None):  # pylint: disable=too-many-arguments
        """ Mark the end of a caldera attack

        @param source: source of the attack. Attack IP
        @param paw: Caldera oaw of the targets being attacked
        @param group: Caldera group of the targets being attacked
        @param ability_id: Caldera ability id of the attack
        @param ttp: TTP of the attack (as stated by Caldera internal settings)
        @param name: Name of the attack. Data source is Caldera internal settings
        @param description: Descirption of the attack. Caldera is the source
        """

        data = {"timestamp": __get_timestamp__(),
                "event": "stop",
                "type": "attack",
                "sub-type": "caldera",
                "source": source,
                "target_paw": paw,
                "target_group": group,
                "ability_id": ability_id,
                "hunting_tag": __mitre_fix_ttp__(ttp),
                "name": name or "",
                "description": description or ""
                }
        self.log.append(data)

    def start_kali_attack(self, source, target, attack_name, ttp=None):
        """ Mark the start of a Kali based attack

        @param source: source of the attack. Attack IP
        @param target: Target machine of the attack
        @param attack_name: Name of the attack. From plugin
        @param ttp: TTP of the attack. From plugin
        """

        data = {"timestamp": __get_timestamp__(),
                "event": "start",
                "type": "attack",
                "sub-type": "kali",
                "source": source,
                "target": target,
                "kali_name": attack_name,
                "hunting_tag": __mitre_fix_ttp__(ttp),
                }
        self.log.append(data)

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

        data = {"timestamp": __get_timestamp__(),
                "event": "stop",
                "type": "attack",
                "sub-type": "kali",
                "source": source,
                "target": target,
                "kali_name": attack_name,
                "hunting_tag": __mitre_fix_ttp__(ttp),
                }
        self.log.append(data)

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
