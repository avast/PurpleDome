===
CLI
===

There are three command line tools that offer a simple interface to PurpleDome.

The central one is Experiment control where you start your experiments:

.. asciinema:: ./../asciinema/experiment_control.cast
    :speed: 2

Experiment control
==================

Experiment control is the core tool to run an experiment. It accepts a yaml config file and runs the experiments in there. The configuration file defines the system to be used (together with a Vagrant file being referenced there) and the attacks to run.

.. argparse::
    :filename: ../experiment_control.py
    :func: create_parser
    :prog: ./experiment_control.py

Plugin manager
==============

List available plugins or a specific plugin config

.. argparse::
    :filename: ../plugin_manager.py
    :func: create_parser
    :prog: ./plugin_manager.py

Caldera control
===============

Directly control a caldera server. You will need a running caldera server to connect to. This plugin is handy to list available attacks and find the attack IDs matching specific TTP-IDs.

.. argparse::
    :filename: ../caldera_control.py
    :func: create_parser
    :prog: ./caldera_control.py

Machine control
===============

Directly control the machines

.. argparse::
    :filename: ../machine_control.py
    :func: create_parser
    :prog: ./machine_control.py

