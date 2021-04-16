=======
Learned
=======

Mistakes made/lessons learned
-----------------------------

* Caldera server needs golang installed: *sudo apt  install golang-go*
* WinRM ist NOT the way to go. Better use OpenSSH for Windows.

Decisions
---------

* Plugins and other things that are relevant for University coop are published here: https://github.com/avast
* Purple Dome Core is internal
* Caldera bugs and similar can and should be fixed in the core project
* What has been named "Victim" so far is better named "Target"
* Running it with Windows VMs is essential. Also install AV
    * It is possible that Vagrant + Windows has issues. In that case: Build Windows VMs and create Snapshots. This is why we need a better VM control lib.
    * MSDN license is ordered
    * We will control the attacks. So we can run this without VMCloak
* Avast seems to be moving those things to AWS. So be ready to move the project there as well.
