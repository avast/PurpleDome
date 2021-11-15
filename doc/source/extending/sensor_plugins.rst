**************
Sensor plugins
**************

To experiment with different sensors installed on the targets there is the sensor plugin. It contains a plugin class that **MUST** be based on the *SensorPlugin* class.

The main goal of PurpleDome is to study sensor technology, which data they can collect and how to create an accurate picture of what happens during an attack. So this can be one of the most important plugin classes to extend.

Usage
=====

To create a new plugin, start a sub-folder in plugins. The python file in there must contain a class that inherits from *SensorPlugin*.

If the plugin is activated for a specific machine specific methods will be called to interact with the target:

* prime: Easly installation steps, can trigger a reboot of the machine by returning True
* install: Normal, simple installation. No reboot
* start: Start the sensor
* stop: Stop the sensor
* collect: Collect results

Boilerplate
-----------

The boilerplate contains some basics:

* name: a unique name, also used in the config yaml file to reference this plugin
* description. A human readable description for this plugin.
* required_files: A list. If you ship files with your plugin, listing them here will cause them to be installed on plugin init by creating a copy in the share.

Additionally you can set *self.debugit* to True. This will run the sensor on execution in gdb and make the call blocking. So you can debug your sensor.


The sensor plugin class
=======================

.. autoclass:: plugins.base.sensor.SensorPlugin
   :members:
