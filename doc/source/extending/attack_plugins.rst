**************
Attack plugins
**************


Attack features of PurpleDome can be extended using a plugin system. Those attack plugins can start Caldera ttacks, run Kali command line tools ir use Metasploit.

An example plugin is in the file *hydra_plugin.py*. It contains a plugin class that **MUST** be based on the *AttackPlugin* class.

::

    Important: This projects goal is to improve defense. Adding any attack must be done with this goal. To guarantee that:

    * Only add attacks that are already in the wild
    * Link to blog posts describing this attack
    * Maybe already drop some ideas how to detect and block
    * Or even add code to detect and block it

Usage
=====

To create a new plugin, start a sub-folder in *plugins*. The python file in there must contain a class that inherits from *AttackPlugin*.

There is an example plugin *hydra.py* that you can use as template.

Boilerplate
-----------

The boilerplate contains some basics:

* name: a unique name, also used in the config yaml file to reference this plugin
* description: A human readable description for this plugin.
* ttp: The TTP number of this kali attack. See https://attack.mitre.org/
* references. A list of urls to blog posts or similar describing the attack
* required_files: A list. If you ship files with your plugin, listing them here will cause them to be installed on plugin init.
Better than using required_files is to use:
* required_files_attacker: required files to send to the attacker
* required_files_target: required files to send to the target


Method: run
-----------

This will run the attack.

* targets: a list of target machines. If you need the network address, use target[0].get_ip()

The plugin class
================

.. autoclass:: plugins.base.attack.AttackPlugin
   :members: