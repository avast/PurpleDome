# FIN7 adversary emulation

https://github.com/center-for-threat-informed-defense/adversary_emulation_library/tree/master/fin7/Emulation_Plan

# Required files

It needs some external files to work. Please download them and put them in this folder

STEP 5:
https://github.com/center-for-threat-informed-defense/adversary_emulation_library/blob/master/fin7/Resources/Step5/samcat.exe
https://github.com/center-for-threat-informed-defense/adversary_emulation_library/blob/master/fin7/Resources/Step5/uac-samcats.ps1

# Machines

See: https://github.com/center-for-threat-informed-defense/adversary_emulation_library/blob/master/fin7/Emulation_Plan/Scenario_1/Infrastructure.md

## 1 hotelmanager

Initial infected machine

Windows 10, Build 18363

User dir: C:\Users\kmitnick.hospitality\AppData\Local\

Tools will be installed on this machine (mimikatz) and could be intercepted by the AV. if you do not want this, de-activate the AV or add exceptions

Required for infection:

* RTF
* VBA
* MSHTA
* winword
* verclsid https://redcanary.com/blog/verclsid-exe-threat-detection/
* tasksched

5 minutes waiting time !

## 2 itadmin

Next hacked machine. Lateral movement there through stolen credentials

Windows 10, Build 18363

## 3 accounting

Hast the valuables

Windows 10, 18363

installed:
* AccountingIQ.exe


## hoteldc

Windows Server 2k19 - Build 17763

Attacker is never traversing to it

## Decisions

* We will be using Scenario 1.
* SQLRat will be replaced by Caldera
* Parts requiring user interaction are skipped. Maybe added later
