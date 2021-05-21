#!/usr/bin/env python3

# Adversary emulation for FIN7

from plugins.base.attack import AttackPlugin
from app.interface_sfx import CommandlineColors



class FIN7Plugin(AttackPlugin):

    # Boilerplate
    name = "fin7_1"
    description = "A plugin simulating the FIN7 adversary"
    ttp = "multiple"
    references = ["https://github.com/center-for-threat-informed-defense/adversary_emulation_library/tree/master/fin7/Emulation_Plan/Scenario_1"]

    required_files_attacker = []    # Files shipped with the plugin which are needed by the kali tool. Will be copied to the kali share

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__

    def step1(self):
        self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Step 1: Initial Breach{CommandlineColors.ENDC}", 1)
        # TODOS: No idea if we can replicate that automated as those are manual tasks

        # RTF with VB payload (needs user interaction)
        # playoad executed by mshta
        # mshta build js payload
        # mshta copies wscript.exe to ADB156.exe
        # winword.exe spawns verclsid.exe
        # mshta uses taskschd.dll to create a task in 5 minutes


        self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}End Step 1: Initial Breach{CommandlineColors.ENDC}", 1)

    def step2(self):
        self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Step 2: Delayed Malware Execution{CommandlineColors.ENDC}", 1)

        # scheduled task spawns Adb156.exe via svchost https://attack.mitre.org/techniques/T1053/005/
        # Adb156.exe loads scrobj.dll and executes sql-rat.js via jscript https://attack.mitre.org/techniques/T1059/007/
        # Adb156.exe connects via MSSQL to attacker server
        # WMI quieries for network information and system information https://attack.mitre.org/techniques/T1016/ and https://attack.mitre.org/techniques/T1082/ (Caldera ?)

        self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}End Step 2: Delayed Malware Execution{CommandlineColors.ENDC}", 1)

    def step3(self):
        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 3: Target Assessment{CommandlineColors.ENDC}", 1)

        # WMI queries  https://attack.mitre.org/techniques/T1057/
        # execute net view from spawned cmd https://attack.mitre.org/techniques/T1135/
        # check for sandbox https://attack.mitre.org/techniques/T1497/
        # query username https://attack.mitre.org/techniques/T1497/
        # query computername https://attack.mitre.org/techniques/T1082/
        # load adsldp.dll and call dllGetClassObject() for the Windows Script Host ADSystemInfo Object COM object https://attack.mitre.org/techniques/T1082/
        # WMI query for System Network Configuration discovery https://attack.mitre.org/techniques/T1016/
        # System Info discovery https://attack.mitre.org/techniques/T1082/
        # CMD.exe->powershell.exe, start takeScreenshot.ps1 https://attack.mitre.org/techniques/T1113/
        # Upload that via MSSQL transaction https://attack.mitre.org/techniques/T1041/

        self.attack_logger.vprint(
            f"{CommandlineColors.OKGREEN}End Step 3: Target Assessment{CommandlineColors.ENDC}", 1)

    def step4(self):
        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 4: Staging Interactive Toolkit{CommandlineColors.ENDC}", 1)

        # Uploaded stager creates meterpreter shell (babymetal)
        # adb156.exe -> cmd.exe ->powershell.exe decodes embedded dll payload https://attack.mitre.org/techniques/T1059/003/ and https://attack.mitre.org/techniques/T1059/001/
        # powershell cmdlet Invoke-Expression executes decoded dll https://attack.mitre.org/techniques/T1140/
        # powershell.exe loads shellcode into memory (received from C2 server) https://attack.mitre.org/techniques/T1573/

        self.attack_logger.vprint(
            f"{CommandlineColors.OKGREEN}End Step 4: Staging Interactive Toolkit{CommandlineColors.ENDC}", 1)

    def step5(self):
        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 5: Escalate Privileges{CommandlineColors.ENDC}", 1)

        # This is meterpreter !

        # powershell -> CreateToolHelp32Snapshot() for process discovery (Caldera alternative ?) https://attack.mitre.org/techniques/T1057/
        # powershell download from C2 server: samcat.exe (mimikatz) https://attack.mitre.org/techniques/T1507/
        # execute uac-samcats.ps1 This: spawns a powershell from powershell -> samcat.exe as high integrity process https://attack.mitre.org/techniques/T1548/002/
        # samcat.exe: reads local credentials https://attack.mitre.org/techniques/T1003/001/
        # powershell: GetIpNetTable() doe ARP entries (Caldera ?) https://attack.mitre.org/techniques/T1016/
        # powershell: nslookup to query domain controler for ip from ARP (Caldera ?) https://attack.mitre.org/techniques/T1018/

        self.attack_logger.vprint(
            f"{CommandlineColors.OKGREEN}End Step 5: Escalate Privileges{CommandlineColors.ENDC}", 1)

    def step6(self):
        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 6: Expand Access{CommandlineColors.ENDC}", 1)

        # This is meterpreter !

        # powershell download: paexec.exe and hollow.exe https://attack.mitre.org/techniques/T1105/
        # spawn powershell through cmd
        # use password with paexec to move lateral to it admin host https://attack.mitre.org/techniques/T1021/002/
        # paexec  starts temorary windows service and executes hollow.exe https://attack.mitre.org/techniques/T1021/002/
        # hollow.exe spawns svchost and unmaps memory image https://attack.mitre.org/techniques/T1055/012/
        # svchost starts data exchange

        self.attack_logger.vprint(
            f"{CommandlineColors.OKGREEN}End Step 6: Expand Access{CommandlineColors.ENDC}", 1)

    def step7(self):
        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 7: Setup User Monitoring{CommandlineColors.ENDC}", 1)

        # This is meterpreter !
        # Emulating DLL hijacking functionality of BOOSTWRITE

        # Create BOOSTWRITE meterpreter handler
        # Create temporary HTTP server serving "B" as XOR Key
        # hollow.exe meterpreter session dowliads BOOSTWRITE.dll to srrstr.dll https://attack.mitre.org/techniques/T1105/
        # cmd.exe spawns svchost.exe -> executes SystemPropertiesAdvanced.exe which executes srrstr.dll
        # srrstr.dll spawns rundll32.exe which communicates to metasploit. New shell !

        # => Adversary gets a new shell

        self.attack_logger.vprint(
            f"{CommandlineColors.OKGREEN}End Step 7: Setup User Monitoring{CommandlineColors.ENDC}", 1)

    def step8(self):
        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 8: User Monitoring{CommandlineColors.ENDC}", 1)

        # This is meterpreter !

        # Meterpreter migrates toexplorer.exe (from svchost) https://attack.mitre.org/techniques/T1055/
        # screenspy for screen capture https://attack.mitre.org/techniques/T1113/
        # migrate session to mstsc.exe https://attack.mitre.org/techniques/T1056/001/
        # deploy keylogger https://attack.mitre.org/techniques/T1056/001/

        self.attack_logger.vprint(
            f"{CommandlineColors.OKGREEN}End Step 8: User Monitoring{CommandlineColors.ENDC}", 1)

    def step9(self):
        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 9: Setup Shim Persistence{CommandlineColors.ENDC}", 1)

        # This is meterpreter !

        # powershell.exe executes base64 encoded commands (Caldera ?)
        # Downloads dll329.dll and sdbE376
        # persistence: sdbinst.exe installs sdbE376.tmp for application shimming https://attack.mitre.org/techniques/T1546/011/

        self.attack_logger.vprint(
            f"{CommandlineColors.OKGREEN}End Step 9: Setup Shim Persistence{CommandlineColors.ENDC}", 1)

    def step10(self):
        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 10: Steal Payment Data{CommandlineColors.ENDC}", 1)

        # This is meterpreter !

        # Scenario target is the fake payment application AccountingIQ.exe

        # Machine is rebooted
        # shim dll329.dll is activated https://attack.mitre.org/techniques/T1546/011/
        # AccountingIQ injects into SyncHost.exe, rundll32.exe communicates to C2
        # debug.exe is downloaded from C2, does process discovery https://attack.mitre.org/techniques/T1105/
        # send 7za.exe to target. Zip stolen data, exfiltrate

        self.attack_logger.vprint(
            f"{CommandlineColors.OKGREEN}End Step 10: Steal Payment Data{CommandlineColors.ENDC}", 1)

    def run(self, targets):
        """ Run the command

        @param targets: A list of targets
        """

        # Set defaults if not present in config
        playground = self.attacker_machine_plugin.get_playground()

        # Generate command
        cmd = f"cd {playground};"
        cmd += "sudo apt -y install hydra;"
        for t in targets:
            for p in self.conf['protocols']:
                cmd += f"hydra -L {self.conf['userfile']}  -P {self.conf['pwdfile']} {p}://{t};"

        res = self.attacker_run_cmd(cmd) or ""

        return res
