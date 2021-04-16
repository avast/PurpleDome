===============
Windows targets
===============

Windows Vagrant boxes need a special setup. They have to be created from a running windows machine.

Windows Box
-----------

If you use Vagrant you need a vagrant box first. It is a base image the vm will be based on.

The base vm must be running in VirtualBox !

Bash::

    vagrant package --base 'Windows 10 x64'

In this example the running Virtual Box VM named 'Windows 10 x64'

Adding the box in bash::

    vagrant box add --name windows10_64 "file:///home/ts/vagrantboxes/win10_64/package.box"

After that it can be used under this name in a Vagrantfile.

Setting up Windows for Purple Dome
----------------------------------

* Mount the vagrant share to X: (at least my scripts expect it) *net use x:\\vboxsvr\share*
* Create a batch file in C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup to automatically start *caldera_agent.bat* in the vagrant share for this machine. This ensures that the caldera agent can be started in reboot
* Install OpenSSH on the windows target (https://docs.microsoft.com/de-de/windows-server/administration/openssh/openssh_install_firstuse  and https://docs.microsoft.com/de-de/windows-server/administration/openssh/openssh_keymanagement)

Some SSH hints (powershell):

Powershell::

    Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
    Start-Service sshd
    Set-Service -Name sshd -StartupType 'Automatic'
    Install-Module -Force OpenSSHUtils -Scope AllUsers



To create a user key in a private user folder call (as user) Powershell::

    ssh-keygen

This can be used for remote login

To be able to log into the Windows box, *c:\users\PurpleDome\.ssh\authorized_keys* needs to be created. Add the public key there.

For admin users, the file is *C:\ProgramData\ssh\administrators_authorized_keys*

Copy your public key into that (open file in administrator notepad, copy&paste)

The file needs special permissions. Powershell::

    $acl = Get-Acl C:\ProgramData\ssh\administrators_authorized_keys
    $acl.SetAccessRuleProtection($true, $false)
    $administratorsRule = New-Object system.security.accesscontrol.filesystemaccessrule("Administrators","FullControl","Allow")
    $systemRule = New-Object system.security.accesscontrol.filesystemaccessrule("SYSTEM","FullControl","Allow")
    $acl.SetAccessRule($administratorsRule)
    $acl.SetAccessRule($systemRule)
    $acl | Set-Acl

See: https://www.concurrency.com/blog/may-2019/key-based-authentication-for-openssh-on-windows

https://github.com/PowerShell/Win32-OpenSSH/wiki/Troubleshooting-Steps

To connect from linux call bash::

    ssh -o "IdentitiesOnly=yes" -i ~/.ssh/id_rsa.3  -v  PURPLEDOME@192.168.178.189

(Capital letters for user name !)
* The parameters enforce the use of a specific key. You can also drop that into the ssh config

Footnote: WinRM failed. I tried. The python code does not support ssh-style "disown". Vagrant files needed a special configuration-and sometimes failed connecting to the windows host properly. Base problem was that it does not properly support empty passwords (not on python, anyway) - and I used them for auto-login. Because some windows versions are a bit tricky with auto-login settings as they should be. Windows 10 is mutating here like hell.
