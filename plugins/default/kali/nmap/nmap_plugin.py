#!/usr/bin/env python3

# A plugin to nmap targets

from plugins.base.attack import AttackPlugin


# TODO All scan patterns need explicit logging into the attack log !
# TODO: Add config for subnet range for ping sweeps
# TODO: Add IP exclusion --exclude ip,ip,ip to not accidentially scan non-targets
# TODO: host discovery Ping scan: -sn
# TODO: host discovery PE ICMP echo
# TODO: host discovery PP ICMP timestamp
# TODO: host discovery PM ICMP netmask request
# TODO: host discovery PS: SYN host discovery
# TODO: host discovery PA: ACK host discovery
# TODO: host discovery PU: UDP host discovery
# TODO: host discovery PR: ARP ping
# TODO: host discovery -PO1: ICMP ping
# TODO: host discovery -PO2: IGMP ping
# TODO: --traceroute in addition to host discovery
# TODO: -R <ip> reverse DNS. Needs a DNS in the big picture. No idea if valuable
# TODO: host discovery reverse DNS resolution
# TODO OS identification
# TODO service discovery
# TODO stealth scans
# TODO firewall evasion
# TODO service fingerprinting
# TODO udp scans   -sU
# TODO TCP SYN scan: -sS
# TODO TCP connect scan: -sT
# TODO port scan without prior ping (this is to avoid triggering firewall logic): -Pn
# TODO: -O OS detection
# TODO: -sV service version detection
# TODO -sS syn scan, stealthy
# TODO -sT tcp connect scan - needs no special permissions
# TODO. -p- scan all ports
# TODO: -p <range> scan port rance
# TODO: -sS -A (aggressive scanning, will also connect to services, run script and detect vulnerabilities like anonymous FTP accounts)
# TODO: --reason: Additional info. I do not think the web traffic will change. So I do not think this is important
# TODO: -F fast scan (fewer ports than default scan)
# TODO: -oX -oG output as XML or grepable. If we want to process the results that could be handy
# TODO: -sN NULL scan, no bits are set
# TODO: -sF FIN scan: FIN bit is set
# TODO: -sX Xmas scan: FIN, PSH and URG flag set
# TODO firewall evasion : -sS and -f for fragmented. old tech. But good for basic NDS tests

# TODO: -sC will execute default LUA scripts. Can be very noisy
# TODO: --script "ftp-*" -p 21      will execute ftp scripts. Can also be very noisy

# TODO spoof mac: --spoof-mac with 0, Apple, Dell, Cisco or fake MAC the first parameters in this list will generate random mac


# TODO: Verify it worked: Use timing settings: -T0-T5 (paranoid, sneaky, polite, default, aggressive, insane). --min-parallelism 100 (for crashes) and use --scan-delay 10s or similar
# By that: crash sensors (most aggressive) or be under the detection threshold

# TODO Verify decoy scan: -D RND:5 to generate 5 decoys

class NmapPlugin(AttackPlugin):

    # Boilerplate
    name = "nmap"
    description = "Nmap scan the target"
    ttp = "T1595"
    references = ["https://attack.mitre.org/techniques/T1595/"]

    required_files = []    # Files shipped with the plugin which are needed by the kali tool. Will be copied to the kali share

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__

    def run(self, targets):
        """ Run the command

        @param targets: A list of targets, ip addresses will do
        """

        res = ""

        pg = self.get_attacker_playground()

        cmd = f"cd {pg};"

        for t in targets:
            cmd += f"nmap {t};"

        res += self.attacker_run_cmd(cmd) or ""

        return res
