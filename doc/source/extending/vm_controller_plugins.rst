*********************
VM Controller plugins
*********************

The experiment being run handles the machines. As there can be several VM controllers being used this is handled by the plugin layer as well. Those machines can be target or attack machines.

A VM plugin handles several things:

* vm creation/destruction
* vm starting/stopping

VM controller plugins can use SSH as a mixin class. This is implemented in *ssh_features.py* and reduces code duplication. In certain cases (for example if SSH needs some extra features) you can extend or replace methods from there. SSH handles:

* connecting to the VM and running commands there
* Copying files from and to the VM



Usage
=====

To create a new plugin, start a sub-folder in plugins. The python file in there must contain a class that inherits from *MachineryPlugin*.

There is an example plugin *vagrant_plugin.py* that you can use as template.

Boilerplate
-----------

The boilerplate contains some basics:

* name: a unique name, also used in the config yaml file to reference this plugin
* description. A human readable description for this plugin.
* required_files: A list. If you ship files with your plugin, listing them here will cause them to be installed on plugin init.

Some relevant methods are

process_config
--------------

The configuration for this machine is a sub-section in the experiment config. As the different machinery systems might require special handling, you can parse the config in this section and add your own processing or defaults

get_state
---------

Get the machines state. The class MachineStates contains potential return values

get_ip
------

Get the ip of the machine. If the machine is registered at the system resolver (/etc/hosts, dns, ...) a machine name would also be a valid response. As long as the network layer can reach it, everything is fine.

The plugin class
================

The machine class can also be very essential if you write attack plugins. Those have access to the kali attack and one or more targets. And those are Machinery objects.
For a full list of methods read on:

.. autoclass:: plugins.base.machinery.MachineryPlugin
   :members: