*********
Extending
*********

Modules
=======

Several core module create the system.

* CalderaControl: remote control for Caldera using the Caldera REST API
* Metasploit: Metasploit control
* MachineControl: Create/start and stop VMs
* ExperimentControl: Control experiments. Will internally use the modules already mentioned
* PluginManager: Plugin manager tasks
* MachineConfig / ExperimentConfig: Reading and processing configuration files
* AttackLog: Logging attack steps and output to stdio


--------------
CalderaControl
--------------

Class for Caldera communication

.. autoclass:: app.calderacontrol.CalderaControl
   :members:

----------
MetaSploit
----------

Class for Metasploit automation

.. autoclass:: app.metasploit.Metasploit
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