*********************
VM Controller plugins
*********************

The experiment being run handles the machines. Those machines can be targets or attacker machines. Different types of machine controllers are covered by plugins of the type "MachineryPlugin".
a
A VM plugin handles several things:

* vm creation/destruction
* vm starting/stopping

VM controller plugins can use SSH as a mixin class - implemented in *ssh_features.py* and reduces code duplication. In certain cases (for example if SSH needs some extra features) you can extend or replace methods from there. SSH handles:

* connecting to the VM and running commands there
* Copying files from and to the VM



Usage
=====

To create a new plugin, start a sub-folder in plugins. The python file in there must contain a class that inherits from *MachineryPlugin*.

Use the example plugin *vagrant_plugin.py*  as template.

Boilerplate
-----------

The boilerplate contains some basics:

* name: a unique name, also used in the config yaml file to reference this plugin
* description. A human readable description for this plugin.
* required_files: A list. If you ship files with your plugin, listing them here will install them on plugin init.


Two sets of commands to be implemented for machines

Basic handling:

* up
* create
* halt
* destroy
* get_state
* get_ip

Communication:

* connect
* remote_run
* disconnect
* put
* get

The communication commands are already implemented in *ssh_features.py* and you can use them they way the vagrant_plugin.py does. At least as long as you want to use SSH to communicate (recommended !).


The machinery plugin
====================

For a full list of methods read on:

.. autoclass:: plugins.base.machinery.MachineryPlugin
    :members:
    :member-order: bysource
    :show-inheritance:


The SSH mixin
=============

.. autoclass:: plugins.base.ssh_features.SSHFeatures
    :members:
    :member-order: bysource
    :show-inheritance:
