#!/usr/bin/env python3

# A plugin to control already running vms

from plugins.base.machinery import MachineryPlugin
from plugins.base.ssh_features import SSHFeatures


class MachineryNoState(SSHFeatures, MachineryPlugin):

    # Boilerplate
    name = "machinery_no_state"
    description = "A plugin to handle already running machines. The machine will not be started/stopped by this plugin"

    required_files = []    # Files shipped with the plugin which are needed by the machine. Will be copied to the share

    def __init__(self):
        super().__init__()
        self.plugin_path = __file__
        self.vagrantfilepath = None
        self.vagrantfile = None

    def create(self, reboot=True):
        """ Create a machine

        @param reboot: Reboot the VM during installation. Required if you want to install software
        """
        return

    def up(self):
        """ Start a machine, create it if it does not exist """
        return

    def halt(self):
        """ Halt a machine """
        return

    def destroy(self):
        """ Destroy a machine """
        return

    def get_ip(self):
        """ Return the machine ip """

        return self.config.vm_ip()
