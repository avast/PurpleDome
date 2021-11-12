*********
Extending
*********

Modules
=======

Several core module create the system. They are in the *app* folder

* experimentcontrol: Control experiments. This is the central control for everything
* calderacontrol: remote control for Caldera using the Caldera REST API
* metasploit: Metasploit control. Simplifies the basic attack step so they can be used from plugins
* machinecontrol: Create/start and stop VMs. Will call the machinery plugin
* pluginmanager: Plugin manager tasks. Has methods to verify plugin quality as well
* config: Reading and processing configuration files
* attacklog: Logging attack steps and output to stdio
* doc_generator: Generates human readable documents from attack logs


--------------
CalderaControl
--------------

Class for Caldera communication

.. autoclass:: app.calderacontrol.CalderaControl
   :members:

----------
Metasploit
----------

Class for Metasploit automation

.. autoclass:: app.metasploit.Metasploit
   :members:

-----------------
MetasploitInstant
-----------------

Extends. In addition to the communication features from the superclass Metasploit it simplifies basic commands.

.. autoclass:: app.metasploit.MetasploitInstant
   :members:

--------
MSFVenom
--------

Class for MSFVenom automation

.. autoclass:: app.metasploit.MSFVenom
   :members:

--------------
MachineControl
--------------

Class controlling a machine

.. autoclass:: app.machinecontrol.Machine
   :members:

-----------------
ExperimentControl
-----------------

Class controlling the experiment

.. autoclass:: app.experimentcontrol.Experiment
   :members:

------
Config
------

Internal configuration handling. Currently there are two classes. One for the whole experiment configuration. The second one for machine specific configuration.

.. autoclass:: app.config.ExperimentConfig
   :members:

.. autoclass:: app.config.MachineConfig
   :members:

-------------
PluginManager
-------------

Managing plugins

.. autoclass:: app.pluginmanager.PluginManager
   :members:

---------
AttackLog
---------

Attack specific logging

.. autoclass:: app.attack_log.AttackLog
   :members: