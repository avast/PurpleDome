#!/bin/bash


# Bootstrap the new VM
#
#

# Update system
apt update
apt -y upgrade

apt -y install apt-transport-https
apt -y install openssh-server
apt -y install whois # for mkpasswd
apt -y install libprotobuf-dev
apt -y install libbpf-dev
apt -y install gdb


# Add vulnerable user
# mkpasswd -m sha-512    # To calc the passwd
# This is in the debian package "whois"

# user with password "test"
# useradd -m -p '$6$bc4k4Tq2.1GW$0ysyuxyfyds2JkfVEf9xHy39MhpS.hhnAo4sBLprNfIHqcpaa9GJseRJJsrq0cSOWwYlOPrdHQNHp10E1ekO81' -s /bin/bash test

# user with password "passw0rd"
# useradd -m -p '$6$q5PAnDI5K0uv$hMGMJQleeS9F2yLOiHXs2PxZHEmV.ook8jyWILzDGDxSTJmTTZSe.QgLVrnuwiyAl5PFJVARkMsSnPICSndJR1' -s /bin/bash password


apt -y update
apt -y upgrade


ip addr show enp0s8 | grep "inet\b" | awk '{print $2}' | cut -d/ -f1 > /vagrant/target3/ip4.txt

# reboot
