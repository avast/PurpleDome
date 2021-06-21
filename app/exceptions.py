#!/usr/bin/env python3
""" A collection of shared exceptions """


class ServerError(Exception):
    """ An elemental server is not running """


class ConfigurationError(Exception):
    """ An elemental server is not running """


class PluginError(Exception):
    """ Some plugin core function is broken """


class CalderaError(Exception):
    """ Caldera is broken """


class NetworkError(Exception):
    """ Network connection (like ssh) can not be established """


class MetasploitError(Exception):
    """ Metasploit had an error """
