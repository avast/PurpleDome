#!/usr/bin/env python3

""" Use logic to detect an attack in sensor logs. This is a PROTOTYPE !!!! """

# TODO: Move essential parts to app folder as soon as it is obvious what is required. Maybe even add the code to existing plugins (sensor plugins ?) or create a new plugin type. Mybe ship that with the sensor in the same folder.

import argparse
import json
import re
from pprint import pprint
from datetime import datetime
from collections import defaultdict

DEFAULT_SENSOR_LOG = "loot/2022_01_07___18_36_21/target3/sensors/linux_filebeat/filebeat.json"


class Detector():
    """
    An experimental prototype to play with detection and display of events. This code should later be part of plugins.
    But until I know where this is going we have this prototype
    """

    def __init__(self, args):

        self.processed_data = []

        as_text = "["

        # Filebeat jsons are not valid jsons and have to be fixed
        with open(args.sensor_log, "rt") as fh:
            new = fh.read()
            new = new.replace("}{", "},{")
            as_text += new
        as_text += "]"
        self.data = json.loads(as_text)

    def detect(self, bucket_size=10, limit=20):
        """ detect

        """

        regex = r"^(?P<date>\w*\W*\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}) (?P<target>\w*) (?P<process>\w*)\[(?P<pid>\d*)\]: Failed password for invalid user (?P<user>\w*) from (?P<attacker>\S*) port (?P<attacker_port>\d*)"

        detected = set()

        self.processed_data = []
        histogram = defaultdict(lambda: 0)
        for entry in self.data:
            if "Failed password" in entry["message"]:
                res = re.match(regex, entry["message"])
                if res:
                    data = res.groupdict()

                    year = entry['@timestamp'].split("-")[0]
                    pdate = datetime.strptime(f"{year} {data['date']}", "%Y %b %d %H:%M:%S")
                    data["timestamp_short"] = int(pdate.timestamp())
                    data["timestamp"] = pdate.timestamp()
                    data["detections"] = []
                    self.processed_data.append(data)
                    histogram[data["timestamp_short"] // bucket_size] += 1

        # detect password brute forcing
        for akey, value in histogram.items():
            if value > limit:
                print(akey)
                for processed in self.processed_data:
                    if processed["timestamp_short"] // bucket_size == akey:
                        processed["detections"].append("pwd_bruteforce")
                        detected.add("pwd_bruteforce")

        pprint(self.processed_data)
        pprint(histogram)
        return detected

    def sequence_diagram(self):
        """ Creates a sequence diagram based on processed data (call detect first). Use plantuml to process it: https://plantuml.com/de/sequence-diagram"""
        # For pdw_bruteforce
        res = "@startuml\n"
        for entry in self.processed_data:
            if "pwd_bruteforce" in entry["detections"]:
                res += f"{entry['attacker']} -> {entry['target']}: to {entry['process']} as {entry['user']}\n"
        res += "@enduml\n"

        print(res)


def create_parser():
    """ Creates the parser for the command line arguments"""
    parser = argparse.ArgumentParser("Detects attacks in logs. Can also create diagrams for the part of the logs indicating the attack")

    parser.add_argument("--sensor_log", default=DEFAULT_SENSOR_LOG, help="The sensor log to detect in")
    # parser.add_argument("--outfile", default="tools/human_readable_documentation/source/contents.rst", help="The default output file")

    return parser


if __name__ == "__main__":
    arguments = create_parser().parse_args()
    detector = Detector(arguments)
    if len(detector.detect()) > 0:
        detector.sequence_diagram()
