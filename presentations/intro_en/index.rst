=================
Purple Dome intro
=================

.. This toctree is only to link examples.

.. toctree::
   :glob:
   :hidden:



The problem
===========

Complex malware attacks in stages. Especially the last ones can be file-less stages

Should I be concerned ?
-----------------------

If you are running a company network: yes

After initial opportunistic infection and system scanning the malware can call an operator

.. after the operator was called it is fileless

Will AV protect me?
===================

Modern AV Software does not only do file detection but also behaviour detection

Sometimes this is advertised. But even if it is not there will be a basic version shipped with your AV

For advanced attacks this is the module protecting you

Does this work well ?
---------------------

The behaviour component is a complex beast

* Different OS versions
* Performance
* Stability
* Lots of different behaviour patterns possible


Is file-less bad ?
------------------

* Dealing with files is simpler
* QA and Development is much harder without malware files


Purple Dome makes dealing with file-less malware simpler
========================================================

We need it to...

* Develop sensors
* Create the logic
* Test everything


Purple Dome: Internals
======================

Purple Dome is a fully automated simulation environment to experiment with sophisticated attacks

Spawning targets
----------------

VMS with the selected OS are initialised and started. That way we can experiment with different OS versions

Spawning the attacker
---------------------

Attacker VM is Kali Linux. It contains

* Metasploit
* Caldera
* Command line tools (nmap...)

Sensoren Setup
--------------

Sensors will be installed on the targets. Now we are recording the events

Running the attacks
--------------------

Attacks are run based on a script

Collecting sensor data
----------------------

Data from the sensors and the log of the attack itself are the result of the simulation

Creating a description
----------------------

For a quick overview it generates a human readable PDF document describing the attack

Other Purple Dome use cases
===========================

Seminars
----------

We are evaluating how to use PD for university seminars.

Trainings
---------

Blue vs Red Team trainings and creation of training data

CTF
---

Capture the Flags games can be based on PD

Buying Purple Dome
==================

It is not for sale. It is Open Source. Just fork it on Github:

https://github.com/avast/PurpleDome