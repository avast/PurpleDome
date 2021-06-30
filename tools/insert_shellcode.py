#!/usr/bin/env python3

# Inserts multi line shellcode into a C-file with a placeholder shellcode. Overwriting the placeholder
#


import re
import argparse


def replace(args):
    """ Replace a specified placeholder part in a file with the shellcode in the shellcode file

    :param original_file:
    :param placeholder_pattern:
    :param shellcode_file:
    :param out_file:
    :return:
    """

    if args.variant == 1:
        original_file = args.original_file
        placeholder_pattern = args.placeholder_pattern
        shellcode_file = args.shellcode_file
        out_file = args.out_file

        with open(shellcode_file, "rt") as fh:
            replacement = fh.read()

        with open(original_file, "rt") as fh:
            original = fh.read()

        s = re.split(placeholder_pattern, original, maxsplit=1, flags=re.S)
        print(s[0], replacement, s[1])

        with open(out_file, "wt") as fh:
            fh.write(s[0])
            fh.write(replacement)
            fh.write(s[1])

    # TODO Add other variants


def create_parser():
    """ Creates the parser for the command line arguments"""

    parser = argparse.ArgumentParser("A tool to patch a shellcode into a C source file")

    parser.set_defaults(func=replace)
    parser.set_defaults(placeholder_pattern=r'unsigned char \w*\[\] =.{0,1}"\\x\d\d[^;]*".{0,1};')
    parser.add_argument('--original_file', default="../tests/data/insert_shellcode/babymetal.cpp", help="The original C code with a shellcode to replace")
    parser.add_argument('--shellcode_file', default="../tests/data/insert_shellcode/shellcode.c", help="The shellcode C snippet to insert into the original file")
    parser.add_argument('--out_file', default="patched.c", help="The resulting patched file")
    parser.add_argument('--variant', default=1, type=int, help="Modification variant. 1 will add a metasploit generated snippet into a header file. 2 will generate a header file out of a 'xxd -i' generated script")
    # parser.add_argument('--varname', default=None, help="The name for the shellcode variable")

    return parser


if __name__ == "__main__":
    arguments = create_parser().parse_args()
    arguments.func(arguments)
    # replace("../tests/data/insert_shellcode/babymetal.cpp", r'unsigned char \w*\[\] =.{0,1}"\\x\d\d[^;]*".{0,1};', "../tests/data/insert_shellcode/shellcode.c", "result.txt")
