#!/usr/bin/env python3

# A standalon document generator. Takes an attack log and generates a doc using templates. Functionality will later be merged into PurpleDome

import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
# from pprint import pprint


def generate(jfile, outfile):
    env = Environment(
        loader=FileSystemLoader("templates", encoding='utf-8', followlinks=False),
        autoescape=select_autoescape(),
        trim_blocks=True,
        # lstrip_blocks=True
    )
    template = env.get_template("attack_description.rst")

    with open(jfile) as fh:
        events = json.load(fh)

    rendered = template.render(events=events)
    print(rendered)

    with open(outfile, "wt") as fh:
        fh.write(rendered)


if __name__ == "__main__":
    # generate("loot/2021_07_19___16_28_45/attack.json", "tools/human_readable_documentation/contents.rst")  # Working example for a short run
    # generate("loot/2021_07_20___08_26_33/attack.json", "tools/human_readable_documentation/contents.rst")  # FIN 7 #1
    # generate("loot/2021_07_20___10_07_36/attack.json", "tools/human_readable_documentation/contents.rst")  # FIN 7 #2 The one Fabrizio got
    # generate("loot/2021_07_28___12_09_00/attack.json",
    #         "tools/human_readable_documentation/contents.rst")  # FIN 7 The last minute locally generated thing

    #  generate("loot/2021_08_30___14_40_23/attack.json",
    #          "tools/human_readable_documentation/contents.rst")  # FIN 7 With genereated files added
    #  generate("removeme/loot/2021_09_07___08_59_42/attack.json",
    #         "tools/human_readable_documentation/source/contents.rst")  # FIN 7 first run on environment
    generate("loot/2021_09_07___16_20_48/attack.json",
             "tools/human_readable_documentation/source/contents.rst")  # FIN 7 locally with extended data  (older: loot/2021_09_07___14_38_14)


    # generate("loot/2021_07_19___15_10_45/attack.json", "tools/human_readable_documentation/contents.rst")
    # generate("removeme.json", "tools/human_readable_documentation/contents.rst")
