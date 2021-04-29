=============
Configuration
=============

Configuration is contained in yaml files. The example shipped with the code is *experiment.yaml*.

To define the VMs there are also *Vagrantfiles* and associated scripts. The example shipped with the code is in the *systems* folder.

Machines
========

Machines (targets and attacker) are configured in *experiment.yaml*. There are different kinds of VM controllers and different communication interfaces. You will have to pick one and configure it.
If you use the VM controller "vagrant" you will also have to create a Vagrantfile and link to it's folder.


Vagrant machines
~~~~~~~~~~~~~~~~

* vagrantfilepath: Path where the vagrantfile is stored


Communication interfaces
------------------------

SSH
~~~

SSH is the default communication interfaces. For Linux machines it can use vagrant to establish communications (get the keyfile). For Windows - which needs OpenSSH installed - the configuration needs the proper keyfile specified.


Attacks
=======

caldera_attacks
---------------

Caldera attacks (called abilities) are identified by a unique ID. Some abilities are built to target several OS-es. But to be flexible with targeting the config has separate lists.

All Caldera abilities are available. But Purple Dome is still missing support for parameters and return values. This can restrict the available abilities at the moment.

kali_attacks
------------

Kali attacks are kali commandline tools run by a small piece of python code in Purple Dome. This is the reason why not all Kali functionality is available yet.

kali_conf
---------

All kali attacks can have a special configuration. The configuration is tool specific.

Config file
===========

.. autoyaml:: ../template.yaml

TBD
===

Some features are not implemented yet. They will be added to the config file later

* Terraform
* Separate attack script
* Azure
* Plugin infrastructure (which will change the configuration of plugins, maybe even require splitting and moving configuration around)

