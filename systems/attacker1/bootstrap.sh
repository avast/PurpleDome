#!/bin/bash


# Bootstrap the new VM
#
#

echo "Bootstrapping attacker1"

# Update system
apt update
cd ~
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
apt -y install golang sphinx-common
#apt -y upgrade

#apt -y install apt-transport-https
#apt -y install openssh-server
#apt -y install whois # for mkpasswd

ip addr show eth1 | grep "inet\b" | awk '{print $2}' | cut -d/ -f1 > /vagrant/attacker1/ip4.txt

# reboot
