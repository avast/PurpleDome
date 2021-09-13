#!/usr/bin/env python3

# A document generator module.

import json
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

class DocGenerator():
    """ Generates human readable docs from attack logs """

    def __init__(self):
        self.outfile = None

    def generate(self, jfile, outfile="tools/human_readable_documentation/source/contents.rst"):

        self.outfile = outfile

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

    def compile_documentation(self):
        """ Compiles the documentation using make """

        os.system("cd tools/human_readable_documentation ; make html; make latexpdf ")

    def get_outfile_paths(self):
        """ Returns the path of the output file written """

        return ["tools/human_readable_documentation/build/latex/purpledomesimulation.pdf"]
