=============
Configuration
=============

Configuration is contained in yaml files. The example shipped with the code is *template.yaml*.

To define the VMs there are also *Vagrantfiles* and associated scripts. The example shipped with the code is in the *systems* folder. Using Vagrant is optional.

Machines
========

Machines (targets and attacker) are configured in *experiment.yaml* - the default config file. There are different kinds of VM controllers and different communication interfaces. You will have to pick one and configure it per machine.
If you use the VM controller "vagrant" you will also have to create a Vagrantfile and link to the folder containing it.

SSH
---

SSH is the default communication interfaces. If you use Linux and Vagrant Purple Dome can use vagrant to establish SSH communication. For Windows - which needs OpenSSH installed - the configuration needs the proper keyfile specified.


Attacks
=======

caldera_attacks
---------------

Caldera attacks (called abilities) are identified by a unique ID. Some abilities are built to target several OS-es.

All Caldera abilities are available. As some will need parameters and Caldera does not offer the option to configure those in the YAML, some caldera attacks might not work without implementing a plugin.

kali_attacks
------------

Kali attacks are kali commandline tools run. Those are executed by specific Purple Dome plugins. Only Kali tools dupported by a plugin are available. You can reference them by the plugin name.

kali_conf
---------

All kali attacks can have a special configuration. The configuration is attack tool specific.

Example config file
===================

.. autoyaml:: ../template.yaml


