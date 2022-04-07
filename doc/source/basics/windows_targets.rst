===============
Windows targets
===============

Windows Vagrant boxes need a special setup. Create them from a running windows machine.

Windows Box
-----------

If you use Vagrant you need a vagrant box first. Base the vm on this image.

The base vm must be running in VirtualBox when taking the snapshot. To do so, use::


    vagrant package --base 'Windows 10 x64'

In this example the running Virtual Box VM named 'Windows 10 x64'

Adding the box in bash::

    vagrant box add --name windows10_64 "file:///home/ts/vagrantboxes/win10_64/package.box"

After that it can be used under this name in a Vagrantfile.

Setting up Windows for Purple Dome
----------------------------------

* Install OpenSSH on the windows target (https://docs.microsoft.com/de-de/windows-server/administration/openssh/openssh_install_firstuse  and https://docs.microsoft.com/de-de/windows-server/administration/openssh/openssh_keymanagement)

Some SSH hints (powershell):

Powershell::

    Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
    Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
    Start-Service sshd
    Set-Service -Name sshd -StartupType 'Automatic'
    Install-Module -Force OpenSSHUtils -Scope AllUsers



To create a user key in a private user folder call (as user) Powershell::

    ssh-keygen

Use this for remote login

To be able to log into the Windows box, create *c:\users\PurpleDome\.ssh\authorized_keys*. Add the public key there.

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

Footnote: WinRM failed.

SCP from and to Windows
-----------------------

Just use the user's home folder as "entry folder" and do::

    scp win10:my_logs.zip .

Reduces the hassle with slashes.