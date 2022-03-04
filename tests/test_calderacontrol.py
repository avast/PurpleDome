import unittest
from unittest.mock import patch, call
from app.calderacontrol import CalderaControl
from simplejson.errors import JSONDecodeError  # type: ignore
from app.exceptions import CalderaError
from app.attack_log import AttackLog
import pydantic
from dotmap import DotMap  # type: ignore

# https://docs.python.org/3/library/unittest.html


class TestExample(unittest.TestCase):

    def setUp(self) -> None:
        self.attack_logger = AttackLog(0)
        self.cc = CalderaControl("https://localhost", attack_logger=self.attack_logger, apikey="123")

    def tearDown(self) -> None:
        pass

    # list_operations
    def test_list_operations(self):
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            try:
                self.cc.list_operations()
            except pydantic.error_wrappers.ValidationError:
                pass
        mock_method.assert_called_once_with(None, method='get', rest_path='api/v2/operations')

    # list operations gets the expected exception
    def test_list_operations_with_exception(self):
        with self.assertRaises(JSONDecodeError):
            with patch.object(self.cc, "__contact_server__", side_effect=JSONDecodeError("foo", "bar", 2)):
                self.cc.list_operations()

    # list_abilities
    def test_list_abilities(self):
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            try:
                self.cc.list_abilities()
            except pydantic.error_wrappers.ValidationError:
                pass
        mock_method.assert_called_once_with(None, method='get', rest_path='api/v2/abilities')

    # list abilities gets the expected exception
    def test_list_abilities_with_exception(self):
        with self.assertRaises(JSONDecodeError):
            with patch.object(self.cc, "__contact_server__", side_effect=JSONDecodeError("foo", "bar", 2)):
                self.cc.list_abilities()

    # list_agents
    def test_list_agents(self):
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            try:
                self.cc.list_agents()
            except pydantic.error_wrappers.ValidationError:
                pass
        mock_method.assert_called_once_with(None, method='get', rest_path='api/v2/agents')

    # list agents gets the expected exception
    def test_list_agents_with_exception(self):
        with self.assertRaises(JSONDecodeError):
            with patch.object(self.cc, "__contact_server__", side_effect=JSONDecodeError("foo", "bar", 2)):
                self.cc.list_agents()

    # list_adversaries
    def test_list_adversaries(self):
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            try:
                self.cc.list_adversaries()
            except pydantic.error_wrappers.ValidationError:
                pass
        mock_method.assert_called_once_with(None, method='get', rest_path='api/v2/adversaries')

    # list adversaries gets the expected exception
    def test_list_adversaries_with_exception(self):
        with self.assertRaises(JSONDecodeError):
            with patch.object(self.cc, "__contact_server__", side_effect=JSONDecodeError("foo", "bar", 2)):
                self.cc.list_adversaries()

    # list_objectives
    def test_list_objectives(self):
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            try:
                self.cc.list_objectives()
            except pydantic.error_wrappers.ValidationError:
                pass
        mock_method.assert_called_once_with(None, method='get', rest_path='api/v2/objectives')

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
            try:
                self.cc.get_operation_by_id(opid)
            except pydantic.error_wrappers.ValidationError:
                pass
        mock_method.assert_called_once_with(None, method='get', rest_path='api/v2/operations')

    # get_linkid
    def test_get_linkid(self):
        paw = "FooBar"
        ability_id = "AID"

        alink = {"paw": paw,
                 "ability": {"ability_id": ability_id},
                 "id": "Getme"}

        op = [DotMap({"chain": [alink]})]

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

        op = [DotMap({"chain": [alink]})]

        with patch.object(self.cc, "get_operation_by_id", return_value=op):
            res = self.cc.get_linkid("Foo", "Bar", ability_id)
        self.assertEqual(res, None)

    # view_operation_report
    def test_view_operation_report(self):
        opid = "FooBar"
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.view_operation_report(opid)
        mock_method.assert_called_once_with({"enable_agent_output": True}, method="post", rest_path="api/v2/operations/FooBar/report")

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

        exp1 = {'name': 'test_name', 'group': 'test_group', 'adversary': {'adversary_id': None}, 'auto_close': False, 'state': 'test_state', 'autonomous': 1, 'planner': {'id': 'atomic'}, 'source': {'id': 'basic'}, 'use_learning_parsers': True, 'obfuscator': 'plain-text', 'jitter': '4/8', 'visibility': '51'}

        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            try:
                self.cc.add_operation(name=name,
                                      advid=advid,
                                      group=group,
                                      state=state)
            except pydantic.error_wrappers.ValidationError:
                pass
        mock_method.assert_has_calls([call(exp1, method='post', rest_path='api/v2/operations')])

    # add_operation defaults
    def test_add_operation_defaults(self):
        name = "test_name"
        advid = "test_id"

        exp1 = {'name': 'test_name', 'group': '', 'adversary': {'adversary_id': None}, 'auto_close': False, 'state': 'running', 'autonomous': 1, 'planner': {'id': 'atomic'}, 'source': {'id': 'basic'}, 'use_learning_parsers': True, 'obfuscator': 'plain-text', 'jitter': '4/8', 'visibility': '51'}

        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            try:
                self.cc.add_operation(name=name,
                                      advid=advid)
            except pydantic.error_wrappers.ValidationError:
                pass
        mock_method.assert_has_calls([call(exp1, method='post', rest_path='api/v2/operations')])

    # add_adversary
    def test_add_adversary(self):
        name = "test_name"
        ability = "test_ability"
        description = "test_descritption"

        # Caldera 4
        exp_4 = {
            "name": name,
            "description": description,
            "atomic_ordering": ["test_ability"],
            #
            "objective": '495a9828-cab1-44dd-a0ca-66e58177d8cc'  # default objective
        }
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.add_adversary(name, ability, description)
        mock_method.assert_called_once_with(exp_4, method="post", rest_path="api/v2/adversaries")

    def test_add_adversary_default(self):
        name = "test_name"
        ability = "test_ability"

        # Caldera 4
        exp_4 = {
            "name": name,
            "description": "created automatically",
            "atomic_ordering": ["test_ability"],
            #
            "objective": '495a9828-cab1-44dd-a0ca-66e58177d8cc'  # default objective
        }
        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.add_adversary(name, ability)
        mock_method.assert_called_once_with(exp_4, method="post", rest_path="api/v2/adversaries")

    # set_operation_state
    def test_set_operation_state(self):
        operation_id = "test_opid"
        state = "paused"

        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.set_operation_state(operation_id, state)
        mock_method.assert_called_once_with({'state': 'paused'}, method='patch', rest_path='api/v2/operations/test_opid')

    # not supported state
    def test_set_operation_state_not_supported(self):
        operation_id = "test_opid"
        state = "not supported"

        with self.assertRaises(ValueError):
            with patch.object(self.cc, "__contact_server__", return_value=None):
                self.cc.set_operation_state(operation_id, state)

    def test_set_operation_state_default(self):
        operation_id = "test_opid"

        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.set_operation_state(operation_id)
        mock_method.assert_called_once_with({'state': 'running'}, method='patch', rest_path='api/v2/operations/test_opid')

    # delete_operation
    def test_delete_operation(self):
        opid = "test_opid"

        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.delete_operation(opid)
        mock_method.assert_called_once_with({}, method="delete", rest_path="api/v2/operations/test_opid")

    # delete_adversary
    def test_delete_adversary(self):
        adid = "test_adid"

        with patch.object(self.cc, "__contact_server__", return_value=None) as mock_method:
            self.cc.delete_adversary(adid)
        mock_method.assert_called_once_with(None, method="delete", rest_path="api/v2/adversaries/test_adid")

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
