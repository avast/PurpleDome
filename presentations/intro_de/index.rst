================
PurpleDome intro
================

.. This toctree is only to link examples.

.. toctree::
   :glob:
   :hidden:



Was ist das Problem
===================

Komplexe Malware greift in mehreren Schritten an. Die letzten können ohne Malware Dateien auskommen.

Betrifft es mich ?
------------------

* Wenn man ein Unternehmens Netzwerk unterhält: Ja
* Nach einer ersten Infektion und automatischer Systemübersicht kann ein Malware Operator dazugerufen werden

.. Ab dem Schritt ist es dann file less

Schützt mich AV ?
=================

Moderne AV Software hat nicht nur Dateierkennung, sondern auch Verhaltenserkennung

Manchmal ist die beworben. Aber eine Minimalvariante sollte eigentlich immer dabei sein.

Das wäre verantwortlich für den AV Schutz

Funktioniert das gut ?
----------------------

Die Verhaltens-Komponente ist recht komplex zu entwickeln

* Verschiedene OS Versionen
* Performance
* Stabilität
* Sehr viele verschiedenen Verhalten denkbar


Ist das blöd, wenn file-less zunimmt ?
--------------------------------------

* Mit Dateien zu hantieren ist einfacher
* QA und Development ist ohne Malware Dateien komplizierter


PurpleDome macht File-less Angriff handhabbarer
===============================================

Wir brauchen das...

* Zum Entwickeln der Sensoren
* Zum Entwickeln der Logik
* Zum Testen der Sensoren


Purple Dome: Wie funktioniert es ?
==================================

Purple Dome ist eine vollautomatisierte Simulations Umgebung, in der man die File-less Angriffe nachvollziehen kann.

Aufsetzen der Ziele
-------------------

Virtuelle Maschinen mit dem Ziel OS werden aufgesetzt. So können wir unsere Sensoren mit verschiedenen OS Versionen testen.

Aufsetzen des Angreifers
------------------------

Aktuell nutzen wir Kali Linux. Dort haben wir:

* Metasploit
* Caldera
* Command line tools (nmap...)

Aufsetzen der Sensoren
----------------------

Sensoren werden automatisch auf den Zielen installiert. Ab jetzt wird aufgezeichnet

Durchführen der Angriffe
------------------------

Welche Angriffe durchgeführt werden bestimmt das Skript

Sammeln der Sensor Daten
------------------------

Daten aller Sensoren werden gesammelt. Zusammen mit einem Log der Angriffe.

Erstellen einer Beschreibung
----------------------------

Zur einfachen Übersicht wird ein lesbares Dokument des Angriffs als PDF erstellt

Wem bringt PurpleDome sonst noch was ?
======================================

Schulungen
----------

Wir planen Schulungsprogramme basierend auf PD. Wird gerade evaluiert von einer Hochschule

Trainings
---------

Blue vs Red Team trainings und erzeugen von Übungsdaten

CTF
---

Capture the Flags können auf PurpleDome basieren

Wo kann ich PurpleDome kaufen ?
===============================

Gar nicht. Ist kostenlos und Open Source

https://github.com/avast/PurpleDome