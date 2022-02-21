import unittest
from unittest.mock import patch
from app.metasploit import Metasploit
from app.attack_log import AttackLog
from pymetasploit3.msfrpc import MsfRpcClient
import requests
from app.exceptions import ServerError
import time

# https://docs.python.org/3/library/unittest.html


class FakeAttacker():

    def __init__(self):
        pass

    def remote_run(self, cmd, disown):
        pass

    def get_ip(self):
        return "66.55.44.33"


class TestMetasploit(unittest.TestCase):

    def setUp(self) -> None:
        with patch.object(time, "sleep") as _:
            self.attack_logger = AttackLog(0)

    def test_basic_init(self):
        with patch.object(time, "sleep") as _:
            m = Metasploit("FooBar", self.attack_logger)
        self.assertEqual(m.password, "FooBar")
        self.assertEqual(m.attack_logger, self.attack_logger)

    def test_msfrpcd_cmd(self):
        attacker = FakeAttacker()
        with patch.object(time, "sleep") as _:
            m = Metasploit("FooBar", self.attack_logger, attacker=attacker, username="Pennywise")
        self.assertEqual(m.__msfrpcd_cmd__(), "killall msfrpcd; nohup msfrpcd -P FooBar -U Pennywise -S &")

    def test_get_client_simple(self):
        attacker = FakeAttacker()
        with patch.object(time, "sleep") as _:
            m = Metasploit("FooBar", self.attack_logger, attacker=attacker, username="Pennywise")
            m.client = "Foo"
            self.assertEqual(m.get_client(), "Foo")

    def test_get_client_success(self):
        attacker = FakeAttacker()
        with patch.object(time, "sleep") as _:
            m = Metasploit("FooBar", self.attack_logger, attacker=attacker, username="Pennywise")
            with patch.object(MsfRpcClient, "__init__", return_value=None) as mock_method:
                m.get_client()
        mock_method.assert_called_once_with("FooBar", attacker=attacker, username="Pennywise", server="66.55.44.33")

    def test_get_client_retries(self):
        attacker = FakeAttacker()
        with patch.object(time, "sleep") as _:
            m = Metasploit("FooBar", self.attack_logger, attacker=attacker, username="Pennywise")
            with self.assertRaises(ServerError):
                with patch.object(MsfRpcClient, "__init__", side_effect=requests.exceptions.ConnectionError()) as mock_method:
                    m.get_client()
            mock_method.assert_called_with("FooBar", attacker=attacker, username="Pennywise", server="66.55.44.33")
