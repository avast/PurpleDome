**************
Attack plugins
**************


Attack features of PurpleDome can be extended using a plugin system. Those attack plugins can start Caldera ttacks, run Kali command line tools ir use Metasploit.

An example plugin is in the file *hydra_plugin.py*. It contains a plugin class that **MUST** be based on the *AttackPlugin* class.

::

    Important: We want to improve defense in this project. Adding any attack must be done with this goal. To guarantee that:

    * Only add attacks that are already ITW
    * Link to blog posts describing this attack
    * Maybe already drop some ideas how to detect and block
    * Or even add code to detect and block it

Usage
=====

To create a new plugin, start a sub-folder in plugins. The python file in there must contain a class that inherits from *AttackPlugin*.

There is an example plugin *hydra.py* that you can use as template.

Boilerplate
-----------

The boilerplate contains some basics:

* name: a unique name, also used in the config yaml file to reference this plugin
* description: A human readable description for this plugin.
* ttp: The TTP number of this kali attack. See https://attack.mitre.org/
* references. A list of urls to blog posts or similar describing the attack
* required_files: A list. If you ship files with your plugin, listing them here will cause them to be installed on plugin init.

Method: process_config
----------------------

This class processes the plugin specific configuration. The *config* parameter will contain the plugin specific part of the yaml config file. You job will be to parse it, offer sane defaults and store the parsed config in *self.conf[]*.

Method: command
---------------

Creates a command that can be run on the kali machine as command. Parameters and configs you can use:

* targets: a list of ip addresses of potential targets
* config: special config for this call
* self.sysconf: global plugin configuration. Like the path to the kali share (internal or external)
* self.conf: The configuration you created in the *process_config* method

Method: run
-----------

This will run the command line created by the method *command* on the kali attacker.

Configuration
-------------

If you are using the plugin, you **must** have a config section for this kali plugin in the configuration. Even if it is empty.

The plugin class
================

.. autoclass:: plugins.base.attack.AttackPlugin
   :members: