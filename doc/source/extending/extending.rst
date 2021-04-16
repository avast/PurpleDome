*********
Extending
*********

Modules
=======

Several core module create the system.

* CalderaControl: remote control for Caldera using the Caldera REST API
* MachineControl: Create/start and stop VMs
* ExperimentControl: Control experiments. Will internally use the modules already mentioned

.. sidebar:: Plugins

   There will be a plugin system soon. Until then the only way to extend
   PurpleDome is to modify the core source code. If it is not urgent, maybe better be patient and ask for a specific plugin interface.

--------------
CalderaControl
--------------

Class for Caldera communication

.. autoclass:: app.calderacontrol.CalderaControl
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
