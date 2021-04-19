Plugin reasoning and planning. To be deleted later.

Which parts to make into plugins
================================

* Everything that could be contributed by external people
* Very specialized features

At the moment those are:

* kali attacks
* sensors
* vm_controllers
* post_processors


Parts of a plugin
=================

* Plugin specific configuration
* The plugin python code
* Additional files and tools to be used by the plugin

Therefore: We need a specific folder for every plugin

We want out own plugins plus external plugins to throw in. So we will have a default folder for plugins (ours) and additional folders with names chosen by external people. Plugins must be searched in those folders. 

Picking and loading plugins
===========================

* the experiment.yaml config specifies the plugins to use

Found plugin interfaces
=======================

https://github.com/ironfroggy/straight.plugin
https://github.com/tibonihoo/yapsy  ( -: not maintained anymore, sourceforge)
https://github.com/pytest-dev/pluggy/ ( -: not maintained anymore; +: used by tox and similar)

