=========================================
Purple Dome - Kein Schwein greift mich an
=========================================

.. This toctree is only to link examples.

.. toctree::
   :glob:
   :hidden:

Spoiler
=======

Es geht um ein neues Tool, das Angriffe simuliert, damit man seine Verteidigungs-Technologie mal in Aktion sehen kann.

Ich
===

* Thorsten Sick
* Erfahrener Entwickler einiger Angriffs Analyse Tools und MW Erkennungs Technologien
* u.a. viele Beiträge zur Cuckoo Sandbox

Origin story
============

Purple Dome ist für unsere Security Firma ein weiteres Tool, um unsere eigenen Produkte zu stress testen. Es ging ca. 1 Jahr Entwicklungszeit da rein.


Da hat man mal richtig in security investiert ...
=================================================

Die Firma hat jetzt:

* SIEM (Security Information and Event Management)
* ein SOC (Security Operation Center) Team
* eine CISO (Chief Information Security Officer)

aber....

Was ist jetzt das Problem ?
===========================

Niemand weiss ob alles funktioniert oder wie die Logs eines Angriffs aussehen....

Mehr Probleme
-------------

...Oder ob die Sensoren mit dem OS Update noch tun wie erwartet...

Noch mehr Probleme
---------------l---

...Oder ob die Logs dann minimal anders aussehen und die Regexe nicht greifen...

Sehr viel mehr Probleme
-----------------------

...Oder ob die selbstgeschriebenen Erkennungsregeln überhaupt was erkennen...

Denn: Kein Schwein greift mich an !
===================================

Früher war mehr EICAR (test-virus Datei). Damit stupst man seine File-Erkennung und schaut ob die noch lebt.

Heute ist mehr file-less
========================

* In-memory Exploits
* Admin tools (LOLBINs)
* harmlose Programme, die aber vulnerabel sind.

Das kann man mit dem EICAR test file nicht mehr so komfortabel nachbilden

In-memory Exploits
------------------

Wenn man als Angreifer ein System hacked, das nur einen Datei scanner hat, kommt man unbemerkt durch, solange man keine Datei anlegt

LOLBins
-------

Living-off-the-land binaries. Also zum Angriff nehmen was eh schon als Tools rumliegt. Fällt weniger auf.

Vulnerable programme
--------------------

Signierte aber veraltete und verwundbare Treiber sind da ein Klassiker. Die schaffen dem Angreifer Systemrechte.

EICAR test file für Behaviour
-----------------------------

Es gibt einige Scripte, die um Dinge auf dem Rechner anrichten, um Behaviour Detection zu testen.
Sie haben aber eher schwankende Qualität und nicht unbedingt Aussagekraft

Behaviour und AV
----------------

Schon seit vielen Jahren hat jede ernst zu nehmende AV Software eine Behaviour Komponente

Leroy Jenkins: Metasploit vs. Production environment
====================================================

Jetzt kann man selbst mit Metasploit und Mimikatz seine eigene Produktionsumgebung angreifen und schauen, was passiert. Ist dann halt kacke.

Lösung
======

Das Open Source Projekt Purple Dome kann eine in VM simulierte Umgebung von Target Maschinen hochziehen und diese dann gescripted angreifen.

Kann nix passieren
------------------

Da alles in der simulierten Umgebung läuft, kann nix passieren

Lieber trotzdem vom Firmen Netz trennen.

Alles wird aufgezeichnet !
==========================

Sensoren auf den Targets oder im Netz zeichnen den Angriff dann auf


PurpleDome macht File-less Angriff handhabbarer
===============================================

Wir brauchen das...

* Zum Entwickeln der Sensoren
* Zum Entwickeln der Logik
* Zum Testen der Sensoren (unter leicht modifizierten Umständen)

Was kann das ?
==============

Aktuell als Beispiele vorhanden sind:

Angriffe
========

* Metasploit
* Kali command line
* Caldera

Metasploit
----------

* Metasploit kann per implant oder exploit auf das Target kommen
* Es baut danach eine Verbindung zum Attacker auf
* und kann das System auf verschiedene Arten (meist Windows API) beeinflussen

Caldera
-------

* Caldera benötigt implants
* Es baut eine Verbindung zum Attacker auf
* Es beeinflusst das System vor allem über Kommandozeilen Befehle (powershell, shell)

Kali
----

Die aktuell verwendeten Kali tools sind Netzwerk zentriert und dienen vor allem dazu, im Purple Dome Kontext Netzwerkprotokolle zu füllen

(hydra, nmap)

Mimikatz
--------

* Wird im Rahmen von Metasploit eingesetzt
* Extrahiert Credentials aus dem Speicher des Targets
* Bei realen Angriffen oft ein Standard-Bestandteil

Cobalt
------

* Ähnlich wie Metasploit
* Wird stark von Malware Angriffen genutzt
* Benötigt eine Lizenz
* Ist (noch) nicht implementiert in Purple Dome

Sensoren
========

* Logstash/filebeat

Virtuelle Maschinen
===================

* Vagrant
* standalone VirtualBox

Vulnerabilities
===============

* RDP
* Schwache User Passwörter

Anwendung
=========

Ein gut automatisierbares Tool mit commandline und config files

Commandline
-----------

.. revealjs-code-block:: console

   ./experiment_control.py run --configfile hello_world.yaml

Dann ein paar Minuten warten

Config
------

.. revealjs-code-block:: yaml
   :linenos:
   :data-line-numbers: 1|3|6|8

    caldera_attacks:
        linux:
            - "bd527b63-9f9e-46e0-9816-b8434d2b8989"
        windows:

    plugin_based_attacks:
        linux:
            - hydra

Targets
-------

Erzeugt mittels Vagrant oder als bestehende VM

Ergebnisse eines Purple Dome Laufs
==================================

Was raus kommt:

* sehr viele Sensor Logs
* Angriffs log
* und ein PDF Dokument für die Manager

Manager lesbares PDF - Übersicht
--------------------------------

Ein PDF zum entspannt lesen

-

.. revealjs-section::
    :data-background-image: _static/pdf_contents.png
    :data-background-size: contain


Manager PDF - Angriffsdetails
-----------------------------

Mit Details


_

.. revealjs-section::
    :data-background-image: _static/pdf_details.png
    :data-background-size: contain

Angriffs Log
------------

Ein Auszug

.. revealjs-code-block:: json
   :linenos:
   :data-line-numbers: 1,2|3,4|5|6,7|8,9,10,11,12,13|14

    "timestamp": "12:10:09.006964",
    "timestamp_end": "12:15:23.064067",
    "type": "attack",
    "sub_type": "caldera",
    "source": "http://192.168.178.126:8888/",
    "target_paw": "target3",
    "target_group": "red_linux",
    "ability_id": "bd527b63-9f9e-46e0-9816-b8434d2b8989",
    "hunting_tag": "MITRE_T1033",
    "name": "Current User",
    "description": "Obtain user from current session",
    "tactics": "System Owner/User Discovery",
    "tactics_id": "T1033",
    "result": [ "vagrant" ]


Sensor Log (Filebeat)
---------------------

Hydra Angriff

.. revealjs-code-block:: json
   :linenos:
   :data-line-numbers: 1|2,3|4|5,6,7,8

     {"@timestamp":"2022-04-07T10:18:37.907Z",
     "message":"Apr  7 10:18:37 target3 sshd[3113]:
     Failed password for invalid user nonexistend_user_1 from 192.168.178.126 port 44924 ssh2",
     "host":{"hostname":"target3"},},
     {"@timestamp":"2022-04-07T10:18:38.907Z",
     "message":"Apr  7 10:18:38 target3 sshd[3113]:
     Failed password for invalid user nonexistend_user_1 from 192.168.178.126 port 44924 ssh2",
     "host":{"hostname":"target3"},}


Purple Dome: Was im Hintergrund geschieht
=========================================

Nach dem Start von der Kommandozeile startet die vollautomatisierte Simulations Umgebung


Aufsetzen der Ziele
===================

Virtuelle Maschinen mit dem Ziel OS werden aufgesetzt. So können wir unsere Sensoren mit verschiedenen OS Versionen testen.

Starten der Maschinen
=====================

Targets und Attacker werden gestartet

Vulnerabilities nach Wunsch
===========================

Damit die Angriffe auch etwas Schaden hinterlassen, kann man per Plugins auch erst mal Vulnerabilities auf den Targets installieren.

Aufsetzen der Sensoren
======================

Sensoren werden automatisch auf den Zielen installiert. Ab jetzt wird aufgezeichnet

Welche Sensoren auf den Targets laufen kann man per config und Plugin definieren

Durchführen der Angriffe
========================

Welche Angriffe durchgeführt werden bestimmt das Skript

* Caldera
* Metasploit
* Kali tools

Sammeln der Sensor Daten
========================

Daten aller Sensoren werden gesammelt. Zusammen mit einem Log der Angriffe.

Wem bringt PurpleDome sonst noch was ?
======================================

Erste Ideen kam schon an:

Schulungen
----------

Security Schulungen basierend auf Purple Dome. Besonders im Bereich Forensik

Trainings
---------

Blue vs Red Team Trainings und Erzeugen von Übungsdaten

CTF
---

Capture the Flag Herausforderungen können auf Purple Dome basieren.
Dafür muß aber das Threat Modell angepasst werden.

Mehr Ideen bitte !
------------------

Das war sicher noch nicht alles

Erweiterbarkeit dank Plugins
============================

Viel Funktionalität ist als Plugin implementiert

* Angriffe
* Vulnerabilities
* Integration von Sensoren in die Targets
* Unterstützte VMs

Beispiel Sensor: Linux Filebeat
===============================

Boilerplate
-----------

.. revealjs-code-block:: python
   :linenos:
   :data-line-numbers: 1|2|3|4,5,6

    class LinuxFilebeatPlugin(SensorPlugin):
        name = "linux_filebeat"
        description = "Linux filebeat plugin"
        required_files = ["filebeat.conf",
                          "filebeat.yml",
                          ]

Install
-------

.. revealjs-code-block:: python
   :linenos:
   :data-line-numbers: 1|3,4

    def prime(self):
        fb_file = "filebeat-7.15.2-amd64.deb"
        self.run_cmd(f"curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/{fb_file}")
        self.run_cmd(f"sudo dpkg -i {fb_file}")

Start
-----

.. revealjs-code-block:: python
   :linenos:
   :data-line-numbers: 1|2,3

    def start(self):
        self.run_cmd("sudo filebeat modules enable system iptables")
        self.run_cmd("sudo filebeat setup --pipelines --modules iptables,system,")

Collect
-------

.. revealjs-code-block:: python
   :linenos:
   :data-line-numbers: 1|2,3|4

    def collect(self, path):
        dst = os.path.join(path, "filebeat.json")
        self.get_from_machine("/tmp/filebeat_collection.json", dst)
        return [dst]

Weitere potentielle Sensoren
============================

Nicht alle sind bereits Bestandteil des Open Source projekts, mit ihnen habe ich aber "gespielt" oder werde es noch:

* EBPF (system API monitor)
* Frida (process API monitor)
* OSQuery (system stats)
* Sysmon (von MS, auch für Linux)
* Volatility (memory forensics)

Fragen ?
========

Mastodon: @thorsi@chaos.social

https://github.com/avast/PurpleDome


Bitte forken. Jetzt.

Danke
=====

Vielen Dank fürs zuhören. Und jetzt: abschalten
