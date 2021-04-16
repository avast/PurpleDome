*********************
VM Controller plugins
*********************

The experiment being run handles the machines. As there can be several VM controllers being used this is handled by the plugin layer as well. Those machines can be target or attack machines.

A VM plugin handles several things:

* vm creation/destruction
* vm starting/stopping
* connecting to the VM (ssh or similar) and running commands there
* Copy files from and to the VM



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

Method: process_config
----------------------

The configuration for this machine is a sub-section in the experiment config. As the different machinery systems might require special handling, you can parse the config in this section and add your own processing or defaults

Method: create
--------------

Creates the machine (for systems like vagrant that build a machine out of a config file)

Method: up
----------

Starts the machine

Method: halt
------------

Stops the machine

Method: destroy
---------------

Remove the machine from disk. Only smart if you can re-create it with *create*

Method: connect
---------------

Create a connection to this machine to run shell commands or copy files

Method: remote_run
------------------

Execute a command on the running machine

Method: put
-----------

Copy a file to the machine

Method: get
-----------

Get a file from the machine

Method: disconnect
------------------

Disconnect the command channel from the  vm

Method: get_state
-----------------

Get the machines state. The class MachineStates contains potential return values

Method: get_ip
--------------

Get the ip of the machine. If the machine is registered at the system resolver (/etc/hosts, dns, ...) a machine name would also be a valid response. As long as the network layer can reach it, everything is fine.

The plugin class
================

.. autoclass:: plugins.base.machinery.MachineryPlugin
   :members: