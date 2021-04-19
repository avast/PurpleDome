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

# Install Elastic search debian repo

wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -
echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | tee /etc/apt/sources.list.d/elastic-7.x.list
apt update

# Install Logstash
apt -y install default-jre
apt -y install logstash

# Install filebeat
apt -y install filebeat
# Configure logstash as output
cp /vagrant/target1/config/filebeat.yml /etc/filebeat/filebeat.yml
cp /vagrant/target1/config/caldera_agent.service /etc/systemd/system/

# Config logstash
cp /vagrant/target1/logstash_conf/*.conf /etc/logstash/conf.d
rm /vagrant/target1/logstash/filebeat.json
touch /vagrant/target1/logstash/filebeat.json
chmod o+w /vagrant/target1/logstash/filebeat.json

# Start Logstash and filebeat
filebeat modules enable system,iptables
filebeat setup --pipelines --modules iptables,system,
systemctl start logstash.service
systemctl enable filebeat
systemctl enable logstash.service

# Run logstash manually for debugging:
# https://www.elastic.co/guide/en/logstash/current/running-logstash-command-line.html
# /usr/share/logstash/bin/logstash --node-name debug -f /etc/logstash/conf.d/ --log.level debug --config.debug

# To test conf files:
# /usr/share/logstash/bin/logstash  -f /etc/logstash/conf.d/ -t

# Start Caldera agent service
# ln -s /vagrant/target1/config/caldera_agent.service /etc/systemd/system
# chmod 666 /etc/systemd/system
# systemctl enable caldera_agent.service
# systemctl start caldera_agent.service


ip addr show enp0s8 | grep "inet\b" | awk '{print $2}' | cut -d/ -f1 > /vagrant/target3/ip4.txt

# reboot
