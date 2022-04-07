*********
Extending
*********

I recommend to start contributing code by using the plugin system. But beyond that there is much more you can do.


Code
====

Core modules create the system. Find them in the *app* folder

* experimentcontrol: Control experiments. This is the central control for everything
* calderaapi_2: Direct REST Api to caldera 2.*  (deprecated)
* calderaapi_4: Direct REST Api to caldera 4.*  (Caldera 4 is alpha)
* calderacontrol: Remote control for Caldera with convenience methods
* metasploit: Metasploit control. Simplifies the basic attack step to make them usable from plugins
* machinecontrol: Create/start and stop VMs. Will call the machinery plugin
* pluginmanager: Plugin manager tasks. Has methods to verify plugin quality as well
* config: Reading and processing configuration files
* config_verifier: Verifyies the configuration
* attack_log: Logging attack steps and output to stdio
* doc_generator: Generates human readable documents from attack logs


--------------
CalderaControl
--------------

Class for Caldera communication

.. autoclass:: app.calderacontrol.CalderaControl
    :members:
    :member-order: bysource
    :show-inheritance:

----------
Metasploit
----------

Class for Metasploit automation

.. autoclass:: app.metasploit.Metasploit
    :members:
    :member-order: bysource
    :show-inheritance:

-----------------
MetasploitInstant
-----------------

Extends. In addition to the communication features from the superclass Metasploit it simplifies basic commands.

.. autoclass:: app.metasploit.MetasploitInstant
    :members:
    :member-order: bysource
    :show-inheritance:

--------
MSFVenom
--------

Class for MSFVenom automation

.. autoclass:: app.metasploit.MSFVenom
    :members:
    :member-order: bysource
    :show-inheritance:

--------------
MachineControl
--------------

Class controlling a machine

.. autoclass:: app.machinecontrol.Machine
    :members:
    :member-order: bysource
    :show-inheritance:

-----------------
ExperimentControl
-----------------

Class controlling the experiment

.. autoclass:: app.experimentcontrol.Experiment
    :members:
    :member-order: bysource
    :show-inheritance:

------
Config
------

Internal configuration handling. There are two classes. One for the whole experiment configuration. The second one for machine specific configuration.

.. autoclass:: app.config.ExperimentConfig
    :members:
    :member-order: bysource
    :show-inheritance:

.. autoclass:: app.config.MachineConfig
    :members:
    :member-order: bysource
    :show-inheritance:

-------------
PluginManager
-------------

Managing plugins

.. autoclass:: app.pluginmanager.PluginManager
    :members:
    :member-order: bysource
    :show-inheritance:

---------
AttackLog
---------

Attack specific logging

.. autoclass:: app.attack_log.AttackLog
    :members:
    :member-order: bysource
    :show-inheritance: