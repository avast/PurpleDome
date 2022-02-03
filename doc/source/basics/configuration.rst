=============
Configuration
=============

Configuration is contained in yaml files. The example shipped with the code is *template.yaml*.

For your first experiments use *hello_world.yaml* which will run a simple attack on a simulated system.

To define the VMs there are also *Vagrantfiles* and associated scripts. The example shipped with the code is in the *systems* folder. Using Vagrant is optional.

Machines
========

Machines (targets and attacker) are configured in an experiment specific yaml file (default is: *experiment.yaml*). There are different kinds of VM controllers and different communication interfaces. You will have to pick one and configure it per machine.
If you use the VM controller "vagrant" you will also have to create a Vagrantfile and link to the folder containing it.

SSH
---

SSH is the default communication interfaces. If you use Linux and Vagrant Purple Dome can use vagrant to establish SSH communication. For Windows - which needs OpenSSH installed - the configuration needs the proper keyfile specified. And you will have to manually install SSH on the windows target.

Vulnerabilities
===============

You can install vulnerabilities and weaknesses in the targets to allow your attacks to succeed (and generating more data that way). Vulnerabilities are implemented as plugins and listed by name in each machine.

Sensors
=======

Sensors are all kinds of technology monitoring system events and collecting data required to detect an attack. Either while it happens or as a forensic experiment.

Each machine can have a list of sensors to run on it. In addition there is the global *sensor_conf* setting to configure the sensors.

Sensors are implemented as plugins.

Attacks
=======

caldera_attacks
---------------

Caldera attacks (called abilities) are identified by a unique ID. Some abilities are built to target several OS-es.

All Caldera abilities are available. As some will need parameters and PurpleDome does not offer the option to configure those in the YAML, some caldera attacks might not work without implementing a plugin.

In the YAML file you will find two sub-categories under caldera_attacks: linux and windows. There you just list the ids of the caldera attacks to run on those systems.

plugin_based_attacks
--------------------

Kali attacks are kali commandline tools run. Metasploit attacks are metasploit steps to run against the target. Both are executed by specific Purple Dome plugins. You can reference them by the plugin name.

In the YAML file you will find two sub-categories under plugin_based_attacks: linux and windows. There you just list the plugin names to run on those systems.

attack_conf
-----------

All plugin based attacks can use configuration. This is in plugin-name sub categories in here.

Example config file
===================

The example defines four machines:

* A kali attacker

And three targets

* target1 (an old Linux, Ubuntu managed)
* target2 (Vagrant managed Windows. Pre installed)
* target3 (Ubuntu 20.10, Created by Vagrant)

It also defines the pre-installed sensors and the vulnerabilities active on each machine.

Next it sets the attack configuration (nap time between attacks and similar) and specifies which attacks to run against which targets.

* plugin_based_attacks
* caldera_attacks

For the plugins it has plugin specific configuration in *sensor_conf* and *attack_conf*

.. autoyaml:: ../template.yaml


