**************
Sensor plugins
**************

To experiment with different sensors installed on the targets there is the sensor plugin. It contains a plugin class that **MUST** be based on the *SensorPlugin* class.

The main goal of PurpleDome is to study sensor technology: what data can be collected and how to create an accurate picture of what happens during an attack. This can be one of the most important plugin classes to extend.

Usage
=====

To create a new plugin, start a sub-folder in plugins. The python file in there must contain a class that inherits from *SensorPlugin*.

If the plugin is activated for a specific machine specific methods will be called to interact with the target:

* start: Start the sensor
* stop: Stop the sensor
* collect: Collect results

Boilerplate
-----------

The boilerplate contains some basics:

* name: a unique name, also used in the config yaml file to reference this plugin
* description. A human readable description for this plugin.
* required_files: A list. If you ship files with your plugin, listing them here will cause them to be installed on plugin init by creating a copy in the share.

In addition to that you can set *self.debugit* to True. This will run the sensor on execution in gdb and make the call blocking. this way you can debug your sensor.

Method: collect
---------------

This is the essential method you will have to implement. It will collect the data produced by the sensor and make it available for storage in the zip-results

Method: start
-------------

Also an important method. Called before the attack to start the sensor. You will have to implement this. *But* if your collect method just collects log files from the system you can also skip that.

Method: stop
------------

Will stop the sensor just prior to calling collect. This is not required in all possible scenarios.

The sensor plugin class
=======================

.. autoclass:: plugins.base.sensor.SensorPlugin
    :members:
    :member-order: bysource
    :show-inheritance:

