import unittest
from app.pluginmanager import PluginManager
from app.attack_log import AttackLog

from plugins.base.sensor import SensorPlugin
from plugins.base.attack import AttackPlugin
from plugins.base.vulnerability_plugin import VulnerabilityPlugin
from plugins.base.machinery import MachineryPlugin

# https://docs.python.org/3/library/unittest.html


class TestMachineControl(unittest.TestCase):

    def setUp(self) -> None:
        self.attack_logger = AttackLog(0)

    def test_basic_pluginmanager_init(self):
        """ just a simple init """
        p = PluginManager(self.attack_logger)
        self.assertIsNotNone(p)

    def test_basic_pluginmanager_get_plugins_empty(self):
        """ just a simple getting plugins with empty directory """
        p = PluginManager(self.attack_logger, "tests/plugins/none")
        self.assertEqual(p.get_plugins(AttackPlugin), [])

    def test_basic_pluginmanager_get_caldera_plugin(self):
        """ just a simple getting the one caldera plugin """
        p = PluginManager(self.attack_logger, "tests/plugins/caldera/caldera_ok.py")
        plugins = p.get_plugins(AttackPlugin)
        self.assertEqual(plugins[0].name, "caldera_autostart_1")
        self.assertEqual(len(plugins), 1)

    def test_basic_pluginmanager_count_caldera_plugin(self):
        """ counting caldera requirements """
        p = PluginManager(self.attack_logger, "tests/plugins/caldera/caldera_ok.py")
        plugins = p.count_caldera_requirements(AttackPlugin, None)
        self.assertEqual(plugins, 1)

    def test_basic_pluginmanager_count_metasploit_plugin(self):
        """ counting caldera requirements """
        p = PluginManager(self.attack_logger, "tests/plugins/caldera/caldera_ok.py")
        plugins = p.count_metasploit_requirements(AttackPlugin, None)
        self.assertEqual(plugins, 0)

    def test_basic_pluginmanager_count_metasploit_plugin_2(self):
        """ counting metasploit requirements """
        p = PluginManager(self.attack_logger, "tests/plugins/metasploit/metasploit_ok.py")
        plugins = p.count_metasploit_requirements(AttackPlugin, None)
        self.assertEqual(plugins, 1)

    def test_basic_pluginmanager_check_ok(self):
        """ basic check for a plugin, ok """
        p = PluginManager(self.attack_logger, "tests/plugins/metasploit/metasploit_ok.py")
        plugins = p.get_plugins(AttackPlugin)
        c = p.check(plugins[0])
        self.assertEqual(c, [])

    def test_basic_pluginmanager_check_sensor_plugin_ok(self):
        """ just a simple getting the one sensor plugin """
        p = PluginManager(self.attack_logger, "tests/plugins/sensor/sensor_ok/*.py")
        plugins = p.get_plugins(SensorPlugin)
        c = p.check(plugins[0])
        self.assertEqual(c, [])

    def test_basic_pluginmanager_check_sensor_plugin_missing_collect(self):
        """ a sensor plugin with missing collect should throw an error on check"""
        p = PluginManager(self.attack_logger, "tests/plugins/sensor/missing_collect/*.py")
        plugins = p.get_plugins(SensorPlugin)
        c = p.check(plugins[0])
        self.assertRegex(c[0], "Method 'collect' not implemented in missing_collect in .*")

    def test_basic_pluginmanager_pick_sensor_plugin_by_name(self):
        """ get a plugin by name """
        p = PluginManager(self.attack_logger, "tests/plugins/sensor/two_sensors/*/*.py")
        plugins = p.get_plugins(SensorPlugin, ["pick_me"])
        self.assertEqual(len(plugins), 1)
        self.assertEqual(plugins[0].get_name(), "pick_me")

    def test_basic_pluginmanager_pick_sensor_plugin_by_name_2(self):
        """ get two plugins by name """
        p = PluginManager(self.attack_logger, "tests/plugins/sensor/two_sensors/*/*.py")
        plugins = p.get_plugins(SensorPlugin, ["pick_me", "ignore_me"])
        self.assertEqual(len(plugins), 2)

    def test_basic_pluginmanager_pick_sensor_plugin_by_name_3(self):
        """ not finding any plugin by name """
        p = PluginManager(self.attack_logger, "tests/plugins/sensor/two_sensors/*/*.py")
        plugins = p.get_plugins(SensorPlugin, ["fail"])
        self.assertEqual(len(plugins), 0)

    def test_basic_pluginmanager_check_attack_plugin_missing_run(self):
        """ a attack plugin with missing run should throw an error on check"""
        p = PluginManager(self.attack_logger, "tests/plugins/attack/missing_run/*.py")
        plugins = p.get_plugins(AttackPlugin)
        c = p.check(plugins[0])
        self.assertRegex(c[0], "Method 'run' not implemented in missing_run in .*")

    def test_basic_pluginmanager_check_vulnerability_plugin_ok(self):
        """ a vulnerability plugin ok on check"""
        p = PluginManager(self.attack_logger, "tests/plugins/vulnerabilities/ok/*.py")
        plugins = p.get_plugins(VulnerabilityPlugin)
        c = p.check(plugins[0])
        self.assertEqual(len(c), 0)

    def test_basic_pluginmanager_check_vulnerability_plugin_missing_start(self):
        """ a vulnerability plugin with missing start should throw an error on check"""
        p = PluginManager(self.attack_logger, "tests/plugins/vulnerabilities/no_start/*.py")
        plugins = p.get_plugins(VulnerabilityPlugin)
        c = p.check(plugins[0])
        self.assertRegex(c[0], "Method 'start' not implemented in missing_start in .*")

    def test_basic_pluginmanager_check_vulnerability_plugin_missing_stop(self):
        """ a vulnerability plugin with missing stop should throw an error on check"""
        p = PluginManager(self.attack_logger, "tests/plugins/vulnerabilities/no_stop/*.py")
        plugins = p.get_plugins(VulnerabilityPlugin)
        c = p.check(plugins[0])
        self.assertRegex(c[0], "Method 'stop' not implemented in missing_stop in .*")

    def test_basic_pluginmanager_check_machinery_plugin_ok(self):
        """ a machinery plugin ok on check"""
        p = PluginManager(self.attack_logger, "tests/plugins/machinery/ok/*.py")
        plugins = p.get_plugins(MachineryPlugin)
        c = p.check(plugins[0])
        self.assertEqual(len(c), 0)

    def test_basic_pluginmanager_check_machinery_plugin_missing_up(self):
        """ a machinery plugin with missing up should throw an error on check"""
        p = PluginManager(self.attack_logger, "tests/plugins/machinery/no_up/*.py")
        plugins = p.get_plugins(MachineryPlugin)
        c = p.check(plugins[0])
        self.assertRegex(c[0], "Method 'up' not implemented in machinery_no_up in .*")

    def test_basic_pluginmanager_check_machinery_plugin_missing_state(self):
        """ a machinery plugin with missing get_state should throw an error on check"""
        p = PluginManager(self.attack_logger, "tests/plugins/machinery/no_state/*.py")
        plugins = p.get_plugins(MachineryPlugin)
        c = p.check(plugins[0])
        self.assertRegex(c[0], "Method 'get_state' not implemented in machinery_no_state in .*")

    def test_basic_pluginmanager_check_machinery_plugin_missing_ip(self):
        """ a machinery plugin with missing get_ip should throw an error on check"""
        p = PluginManager(self.attack_logger, "tests/plugins/machinery/no_ip/*.py")
        plugins = p.get_plugins(MachineryPlugin)
        c = p.check(plugins[0])
        self.assertEqual(len(c), 1)
        self.assertRegex(c[0], "Method 'get_ip' not implemented in machinery_no_ip in .*")

    def test_basic_pluginmanager_check_machinery_plugin_missing_halt(self):
        """ a machinery plugin with missing halt should throw an error on check"""
        p = PluginManager(self.attack_logger, "tests/plugins/machinery/no_halt/*.py")
        plugins = p.get_plugins(MachineryPlugin)
        c = p.check(plugins[0])
        self.assertEqual(len(c), 1)
        self.assertRegex(c[0], "Method 'halt' not implemented in machinery_no_halt in .*")

    def test_basic_pluginmanager_check_machinery_plugin_missing_destroyt(self):
        """ a machinery plugin with missing destroy should throw an error on check"""
        p = PluginManager(self.attack_logger, "tests/plugins/machinery/no_destroy/*.py")
        plugins = p.get_plugins(MachineryPlugin)
        c = p.check(plugins[0])
        self.assertEqual(len(c), 1)
        self.assertRegex(c[0], "Method 'destroy' not implemented in machinery_no_destroy in .*")

    def test_basic_pluginmanager_check_machinery_plugin_missing_create(self):
        """ a machinery plugin with missing create should throw an error on check"""
        p = PluginManager(self.attack_logger, "tests/plugins/machinery/no_create/*.py")
        plugins = p.get_plugins(MachineryPlugin)
        c = p.check(plugins[0])
        self.assertEqual(len(c), 1)
        self.assertRegex(c[0], "Method 'create' not implemented in machinery_no_create in .*")

    def test_basic_pluginmanager_check_basics_plugin_missing_description(self):
        """ a plugin with missing description should throw an error on check"""
        p = PluginManager(self.attack_logger, "tests/plugins/basics/no_description/*.py")
        plugins = p.get_plugins(AttackPlugin)
        c = p.check(plugins[0])
        self.assertEqual(len(c), 1)
        self.assertRegex(c[0], "No description in plugin: metasploit_no_description in .*")

    def test_basic_pluginmanager_check_basics_plugin_missing_name(self):
        """ a plugin with missing name should throw an error on check"""
        p = PluginManager(self.attack_logger, "tests/plugins/basics/no_name/*.py")
        plugins = p.get_plugins(AttackPlugin)
        c = p.check(plugins[0])
        self.assertEqual(len(c), 1)
        self.assertRegex(c[0], "No name for plugin: in .*")

    def test_basic_pluginmanager_check_vul_plugin_missing_ttp(self):
        """ a vulnerability plugin with missing name should throw an error on check"""
        p = PluginManager(self.attack_logger, "tests/plugins/basics/vul_no_ttp/*.py")
        plugins = p.get_plugins(VulnerabilityPlugin)
        c = p.check(plugins[0])
        self.assertEqual(len(c), 1)
        self.assertRegex(c[0], "Vulnerability plugins need a valid ttp number \\(either T1234, T1234.222 or ...\\)  vulnerability_ok uses None in .*")

    def test_basic_pluginmanager_check_ttp_is_none(self):
        """ ttp check with NONE"""
        p = PluginManager(self.attack_logger, "tests/plugins/basics/vul_no_ttp/*.py")
        self.assertEqual(p.is_ttp_wrong(None), True)

    def test_basic_pluginmanager_check_ttp_is_short_ttp(self):
        """ ttp check with T1234 """
        p = PluginManager(self.attack_logger, "tests/plugins/basics/vul_no_ttp/*.py")
        self.assertEqual(p.is_ttp_wrong("T1234"), False)

    def test_basic_pluginmanager_check_ttp_is_detailed_ttp(self):
        """ ttp check with T1234.123 """
        p = PluginManager(self.attack_logger, "tests/plugins/basics/vul_no_ttp/*.py")
        self.assertEqual(p.is_ttp_wrong("T1234.123"), False)

    def test_basic_pluginmanager_check_ttp_is_unknown_ttp(self):
        """ ttp check with ??? """
        p = PluginManager(self.attack_logger, "tests/plugins/basics/vul_no_ttp/*.py")
        self.assertEqual(p.is_ttp_wrong("???"), False)

    def test_basic_pluginmanager_check_ttp_is_multiple(self):
        """ ttp check with ??? """
        p = PluginManager(self.attack_logger, "tests/plugins/basics/vul_no_ttp/*.py")
        self.assertEqual(p.is_ttp_wrong("multiple"), False)

    def test_basic_pluginmanager_check_ttp_is_wrong_ttp(self):
        """ ttp check with something else """
        p = PluginManager(self.attack_logger, "tests/plugins/basics/vul_no_ttp/*.py")
        self.assertEqual(p.is_ttp_wrong("this is not gonna work"), True)

    def test_basic_pluginmanager_check_attack_plugin_missing_ttp(self):
        """ a attack plugin with missing name should throw an error on check"""
        p = PluginManager(self.attack_logger, "tests/plugins/basics/attack_no_ttp/*.py")
        plugins = p.get_plugins(AttackPlugin)
        c = p.check(plugins[0])
        self.assertEqual(len(c), 1)
        self.assertRegex(c[0], "Attack plugins need a valid ttp number \\(either T1234, T1234.222 or ...\\)  no TTP uses None in .*")
