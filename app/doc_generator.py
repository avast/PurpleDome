#!/usr/bin/env python3

""" Generate human readable document describing the attack based on an attack log """

import json
import os
from typing import Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape


class DocGenerator():
    """ Generates human readable docs from attack logs """

    def __init__(self) -> None:
        self.outfile: Optional[str] = None

    def generate(self, jfile: str, outfile: str = "tools/human_readable_documentation/source/contents.rst") -> None:
        """ Generates human readable documentation out of a template.

        @param jfile: json attack log created by PurpleDome as data source
        @param outfile: rst file to write. Can be compiled into pdf using sphinx
        """

        self.outfile = outfile

        env = Environment(
            loader=FileSystemLoader("templates", encoding='utf-8', followlinks=False),
            autoescape=select_autoescape(),
            trim_blocks=True,
            # lstrip_blocks=True
        )
        template = env.get_template("attack_description.rst")

        with open(jfile) as fh:
            attack = json.load(fh)

        rendered = template.render(events=attack["attack_log"], systems=attack["system_overview"], boilerplate=attack["boilerplate"])
        print(rendered)

        with open(outfile, "wt") as fh:
            fh.write(rendered)

    def compile_documentation(self) -> None:
        """ Compiles the documentation using make """

        os.system("cd tools/human_readable_documentation ; make html; make latexpdf ")

    def get_outfile_paths(self) -> list[str]:
        """ Returns the path of the output file written """

        return ["tools/human_readable_documentation/build/latex/purpledomesimulation.pdf"]
