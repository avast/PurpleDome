import unittest
from unittest.mock import patch, call
from app.calderacontrol import CalderaControl
from simplejson.errors import JSONDecodeError
from app.exceptions import CalderaError
from app.attack_log import AttackLog

# https://docs.python.org/3/library/unittest.html


class TestExample(unittest.TestCase):

    def setUp(self) -> None:
        self.attack_logger = AttackLog(0)
        self.cc = CalderaControl("https://localhost", attack_logger=self.attack_logger, apikey="123")

    def tearDown(self) -> None:
        pass

    # List links sends the right commands and post
    def test_list_links(self):
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.list_links("asd")
        mock_method.assert_called_once_with({"index": "link", "op_id": "asd"})

    # List links gets an Exception and does not handle it (as expected)
    def test_list_links_with_exception(self):
        with self.assertRaises(JSONDecodeError):
            with patch.object(self.cc, "__contact_server__", side_effect=JSONDecodeError("foo", "bar", 2)):
                self.cc.list_links("asd")

    # list results sends the right commands and post
    def test_list_results(self):
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.list_results("asd")
        mock_method.assert_called_once_with({"index": "result", "link_id": "asd"})

    # List results gets an Exception and does not handle it (as expected)
    def test_list_results_with_exception(self):
        with self.assertRaises(JSONDecodeError):
            with patch.object(self.cc, "__contact_server__", side_effect=JSONDecodeError("foo", "bar", 2)):
                self.cc.list_results("asd")

    # list_operations
    def test_list_operations(self):
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.list_operations()
        mock_method.assert_called_once_with({"index": "operations"})

    # list operations gets the expected exception
    def test_list_operations_with_exception(self):
        with self.assertRaises(JSONDecodeError):
            with patch.object(self.cc, "__contact_server__", side_effect=JSONDecodeError("foo", "bar", 2)):
                self.cc.list_operations()

    # list_abilities
    def test_list_abilities(self):
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.list_abilities()
        mock_method.assert_called_once_with({"index": "abilities"})

    # list abilities gets the expected exception
    def test_list_abilities_with_exception(self):
        with self.assertRaises(JSONDecodeError):
            with patch.object(self.cc, "__contact_server__", side_effect=JSONDecodeError("foo", "bar", 2)):
                self.cc.list_abilities()

    # list_agents
    def test_list_agents(self):
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.list_agents()
        mock_method.assert_called_once_with({"index": "agents"})

    # list agents gets the expected exception
    def test_list_agents_with_exception(self):
        with self.assertRaises(JSONDecodeError):
            with patch.object(self.cc, "__contact_server__", side_effect=JSONDecodeError("foo", "bar", 2)):
                self.cc.list_agents()

    # list_adversaries
    def test_list_adversaries(self):
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.list_adversaries()
        mock_method.assert_called_once_with({"index": "adversaries"})

    # list adversaries gets the expected exception
    def test_list_adversaries_with_exception(self):
        with self.assertRaises(JSONDecodeError):
            with patch.object(self.cc, "__contact_server__", side_effect=JSONDecodeError("foo", "bar", 2)):
                self.cc.list_adversaries()

    # list_objectives
    def test_list_objectives(self):
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.list_objectives()
        mock_method.assert_called_once_with({"index": "objectives"})

    # list objectives gets the expected exception
    def test_list_objectives_with_exception(self):
        with self.assertRaises(JSONDecodeError):
            with patch.object(self.cc, "__contact_server__", side_effect=JSONDecodeError("foo", "bar", 2)):
                self.cc.list_objectives()

    # Get operation (working)
    def test_get_operation(self):
        a = {"name": "bar", "bar": "baz"}
        with patch.object(self.cc, "list_operations", return_value=[a, {"name": "zigg", "bar": "baz"}]):
            op = self.cc.get_operation("bar")
        self.assertEqual(op, a)

    # Get operation (no matching name)
    def test_get_operation_not_available(self):
        a = {"name": "bar", "bar": "baz"}
        with patch.object(self.cc, "list_operations", return_value=[a, {"name": "zigg", "bar": "baz"}]):
            op = self.cc.get_operation("baaaaar")
        self.assertEqual(op, None)

    # get_adversary
    def test_get_adversary(self):
        a = {"name": "bar", "bar": "baz"}
        with patch.object(self.cc, "list_adversaries", return_value=[a, {"name": "zigg", "bar": "baz"}]):
            op = self.cc.get_adversary("bar")
        self.assertEqual(op, a)

    # get_adversary (no matching name)
    def test_get_adversary_not_available(self):
        a = {"name": "bar", "bar": "baz"}
        with patch.object(self.cc, "list_adversaries", return_value=[a, {"name": "zigg", "bar": "baz"}]):
            op = self.cc.get_adversary("baaaar")
        self.assertEqual(op, None)

    # get_objective
    def test_get_objective(self):
        a = {"name": "bar", "bar": "baz"}
        with patch.object(self.cc, "list_objectives", return_value=[a, {"name": "zigg", "bar": "baz"}]):
            op = self.cc.get_objective("bar")
        self.assertEqual(op, a)

    # get_objective (no matching name)
    def test_get_objective_not_available(self):
        a = {"name": "bar", "bar": "baz"}
        with patch.object(self.cc, "list_objectives", return_value=[a, {"name": "zigg", "bar": "baz"}]):
            op = self.cc.get_objective("baaaar")
        self.assertEqual(op, None)

    # get_ability
    def test_get_ability(self):
        a = {"ability_id": "bar", "bar": "baz"}
        with patch.object(self.cc, "list_abilities", return_value=[a, {"ability_id": "zigg", "bar": "baz"}]):
            op = self.cc.get_ability("bar")
        self.assertEqual(op, [a])

    # get_ability (no matching name)
    def test_get_ability_not_available(self):
        a = {"ability_id": "bar", "bar": "baz"}
        with patch.object(self.cc, "list_abilities", return_value=[a, {"ability_id": "zigg", "bar": "baz"}]):
            op = self.cc.get_ability("baaaar")
        self.assertEqual(op, [])

    # get_operation_by_id
    def test_get_operation_by_id(self):
        opid = "FooBar"
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.get_operation_by_id(opid)
        mock_method.assert_called_once_with({"index": "operations", "id": opid})

    # get_operation_by_id gets the expected exception
    def test_get_operation_by_id_with_exception(self):
        with self.assertRaises(JSONDecodeError):
            with patch.object(self.cc, "__contact_server__", side_effect=JSONDecodeError("foo", "bar", 2)):
                self.cc.get_result_by_id("FooBar")

    # get_result_by_id
    def test_get_result_by_id(self):
        opid = "FooBar"
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.get_result_by_id(opid)
        mock_method.assert_called_once_with({"index": "result", "link_id": opid})

    # get_result_by_id gets the expected exception
    def test_get_result_by_id_with_exception(self):
        with self.assertRaises(JSONDecodeError):
            with patch.object(self.cc, "__contact_server__", side_effect=JSONDecodeError("foo", "bar", 2)):
                self.cc.get_result_by_id("FooBar")

    # get_linkid
    def test_get_linkid(self):
        paw = "FooBar"
        ability_id = "AID"

        alink = {"paw": paw,
                 "ability": {"ability_id": ability_id},
                 "id": "Getme"}

        op = [{"chain": [alink]}]

        with patch.object(self.cc, "get_operation_by_id", return_value=op):
            res = self.cc.get_linkid("Foo", paw, ability_id)
        self.assertEqual(res, "Getme")

    # get missing link id
    def test_get_linkid_missing(self):
        paw = "FooBar"
        ability_id = "AID"

        alink = {"paw": paw,
                 "ability": {"ability_id": ability_id},
                 "id": "Getme"}

        op = [{"chain": [alink]}]

        with patch.object(self.cc, "get_operation_by_id", return_value=op):
            res = self.cc.get_linkid("Foo", "Bar", ability_id)
        self.assertEqual(res, None)

    # view_operation_report
    def test_view_operation_report(self):
        opid = "FooBar"
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.view_operation_report(opid)
        mock_method.assert_called_once_with({"index": "operation_report", "op_id": opid, "agent_output": 1})

    # get_result_by_id gets the expected exception
    def test_view_operation_report_with_exception(self):
        with self.assertRaises(JSONDecodeError):
            with patch.object(self.cc, "__contact_server__", side_effect=JSONDecodeError("foo", "bar", 2)):
                self.cc.view_operation_report("FooBar")

    # view_operation_output
    def test_view_operation_output(self):
        opid = "OPID_123"
        paw = "PAW_123"
        ability_id = "AID_123"
        or_ret = {"steps": {paw: {"steps": [{"ability_id": ability_id, "output": "red"}]}}}
        with patch.object(self.cc, "view_operation_report", return_value=or_ret):
            res = self.cc.view_operation_output(opid, paw, ability_id)
        self.assertEqual(res, "red")

    # view_operation_output paw missing
    def test_view_operation_output_paw_missing(self):
        opid = "OPID_123"
        paw = "PAW_123"
        ability_id = "AID_123"
        or_ret = {"steps": {paw: {"steps": [{"ability_id": ability_id, "output": "red"}]}}}
        with self.assertRaises(CalderaError):
            with patch.object(self.cc, "view_operation_report", return_value=or_ret):
                self.cc.view_operation_output(opid, "missing", ability_id)

    # view_operation_output ability_id missing
    def test_view_operation_output_ability_id_missing(self):
        opid = "OPID_123"
        paw = "PAW_123"
        ability_id = "AID_123"
        or_ret = {"steps": {paw: {"steps": [{"ability_id": ability_id, "output": "red"}]}}}
        with patch.object(self.cc, "view_operation_report", return_value=or_ret):
            res = self.cc.view_operation_output(opid, paw, "missing")
        self.assertEqual(res, None)

    # add_operation
    def test_add_operation(self):
        name = "test_name"
        state = "test_state"
        group = "test_group"
        advid = "test_id"

        exp1 = {"index": "sources",
                "name": "source_test_name",
                "rules": [],
                "relationships": [],
                "facts": []
                }
        exp2 = {"index": "sources",
                "name": "source_name"
                }
        exp3 = {"index": "operations",
                "name": name,
                "state": state,
                "autonomous": 1,
                'obfuscator': 'plain-text',
                'auto_close': '1',
                'jitter': '4/8',
                'source': 'source_test_name',
                'visibility': '50',
                "group": group,
                "planner": "atomic",
                "adversary_id": advid,
                }
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.add_operation(name, advid, group, state)
        # mock_method.assert_called_once_with(exp, method="put")
        mock_method.assert_has_calls([call(exp1, method="put"), call(exp2), call(exp3, method="put")])

    # add_operation defaults
    def test_add_operation_defaults(self):
        name = "test_name"
        advid = "test_id"

        exp1 = {"index": "sources",
                "name": "source_test_name",
                "rules": [],
                "relationships": [],
                "facts": []
                }
        exp2 = {"index": "sources",
                "name": "source_name"
                }
        exp3 = {"index": "operations",
                "name": name,
                "state": "running",  # default
                "autonomous": 1,
                'obfuscator': 'plain-text',
                'auto_close': '1',
                'jitter': '4/8',
                'source': 'source_test_name',
                'visibility': '50',
                "group": "red",  # default
                "planner": "atomic",
                "adversary_id": advid,
                }
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.add_operation(name, advid)
        mock_method.assert_has_calls([call(exp1, method="put"), call(exp2), call(exp3, method="put")])

    # add_adversary
    def test_add_adversary(self):
        name = "test_name"
        ability = "test_ability"
        description = "test_descritption"

        exp = {"index": "adversaries",
               "name": name,
               "description": description,
               "atomic_ordering": [{"id": ability}],
               #
               "objective": '495a9828-cab1-44dd-a0ca-66e58177d8cc'  # default objective
               }
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.add_adversary(name, ability, description)
        mock_method.assert_called_once_with(exp, method="put")

    def test_add_adversary_default(self):
        name = "test_name"
        ability = "test_ability"

        exp = {"index": "adversaries",
               "name": name,
               "description": "created automatically",
               "atomic_ordering": [{"id": ability}],
               #
               "objective": '495a9828-cab1-44dd-a0ca-66e58177d8cc'  # default objective
               }
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.add_adversary(name, ability)
        mock_method.assert_called_once_with(exp, method="put")

    # execute_ability
    def test_execute_ability(self):
        paw = "test_paw"
        ability_id = "test_ability"
        obfuscator = "plain-text"

        exp = {"paw": paw,
               "ability_id": ability_id,
               "obfuscator": obfuscator,
               "facts": []}
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.execute_ability(paw, ability_id, obfuscator)
        mock_method.assert_called_once_with(exp, rest_path="plugin/access/exploit_ex")

    def test_execute_ability_default(self):
        paw = "test_paw"
        ability_id = "test_ability"

        exp = {"paw": paw,
               "ability_id": ability_id,
               "obfuscator": "plain-text",
               "facts": []}
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.execute_ability(paw, ability_id)
        mock_method.assert_called_once_with(exp, rest_path="plugin/access/exploit_ex")

    # execute_operation
    def test_execute_operation(self):
        operation_id = "test_opid"
        state = "paused"

        exp = {"index": "operation",
               "op_id": operation_id,
               "state": state}
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.execute_operation(operation_id, state)
        mock_method.assert_called_once_with(exp)

    # not supported state
    def test_execute_operation_not_supported(self):
        operation_id = "test_opid"
        state = "not supported"

        with self.assertRaises(ValueError):
            with patch.object(self.cc, "__contact_server__", return_value=None):
                self.cc.execute_operation(operation_id, state)

    def test_execute_operation_default(self):
        operation_id = "test_opid"

        exp = {"index": "operation",
               "op_id": operation_id,
               "state": "running"  # default
               }
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.execute_operation(operation_id)
        mock_method.assert_called_once_with(exp)

    # delete_operation
    def test_delete_operation(self):
        opid = "test_opid"

        exp = {"index": "operations",
               "id": opid}
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.delete_operation(opid)
        mock_method.assert_called_once_with(exp, method="delete")

    # delete_adversary
    def test_delete_adversary(self):
        adid = "test_adid"

        exp = {"index": "adversaries",
               "adversary_id": [{"adversary_id": adid}]}
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.delete_adversary(adid)
        mock_method.assert_called_once_with(exp, method="delete")

    # is_operation_finished
    def test_is_operation_finished_true(self):
        opdata = [{"state": "finished", "chain": [{"status": 0}]}]
        opid = "does not matter"

        with patch.object(self.cc, "get_operation_by_id", return_value=opdata):
            res = self.cc.is_operation_finished(opid)
        self.assertEqual(res, True)

    def test_is_operation_finished_false(self):
        opdata = [{"state": "running", "chain": [{"status": 1}]}]
        opid = "does not matter"

        with patch.object(self.cc, "get_operation_by_id", return_value=opdata):
            res = self.cc.is_operation_finished(opid)
        self.assertEqual(res, False)

    def test_is_operation_finished_exception(self):
        opdata = [{"chain": [{"statusa": 1}]}]
        opid = "does not matter"

        with self.assertRaises(CalderaError):
            with patch.object(self.cc, "get_operation_by_id", return_value=opdata):
                self.cc.is_operation_finished(opid)

    def test_is_operation_finished_exception2(self):
        opdata = []
        opid = "does not matter"

        with self.assertRaises(CalderaError):
            with patch.object(self.cc, "get_operation_by_id", return_value=opdata):
                self.cc.is_operation_finished(opid)

    # TODO attack (lots of complexity !)

    # TODO test fetch_client

    # TODO test __contact_server__


if __name__ == '__main__':
    unittest.main()
