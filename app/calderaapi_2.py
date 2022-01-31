#!/usr/bin/env python3
""" Direct API to the caldera server. Not abstract simplification methods. Compatible with Caldera 2.8.1 """

import json
import requests
import simplejson


class CalderaAPI:
    """ API to Caldera 2.8.1 """

    def __init__(self, server: str, attack_logger, config=None, apikey=None):
        """

        @param server: Caldera server url/ip
        @param attack_logger: The attack logger to use
        @param config: The configuration
        """
        # print(server)
        self.url = server if server.endswith("/") else server + "/"
        self.attack_logger = attack_logger

        self.config = config

        if self.config:
            self.apikey = self.config.caldera_apikey()
        else:
            self.apikey = apikey

    def __contact_server__(self, payload, rest_path: str = "api/rest", method: str = "post"):
        """

        @param payload: payload as dict to send to the server
        @param rest_path: specific path for this rest api
        @param method: http method to use
        """
        url = self.url + rest_path
        header = {"KEY": self.apikey,
                  "Content-Type": "application/json"}
        if method.lower() == "post":
            request = requests.post(url, headers=header, data=json.dumps(payload))
        elif method.lower() == "put":
            request = requests.put(url, headers=header, data=json.dumps(payload))
        elif method.lower() == "get":
            request = requests.get(url, headers=header, data=json.dumps(payload))
        elif method.lower() == "delete":
            request = requests.delete(url, headers=header, data=json.dumps(payload))
        else:
            raise ValueError
        try:
            res = request.json()
        except simplejson.errors.JSONDecodeError as exception:  # type: ignore
            print("!!! Error !!!!")
            print(payload)
            print(request.text)
            print("!!! Error !!!!")
            raise exception

        return res

    def list_operations(self):
        """ Return operations """

        payload = {"index": "operations"}
        return self.__contact_server__(payload)

    def list_abilities(self):
        """ Return all ablilities """
        # curl -H 'KEY: ADMIN123' http://192.168.178.102:8888/api/rest -H 'Content-Type: application/json' -d '{"index":"abilities"}'

        payload = {"index": "abilities"}
        return self.__contact_server__(payload)

    def list_agents(self):
        """ List running agents

        """
        # TODO: Add filters for specific platforms/executors  :  , platform_filter=None, executor_filter=None as parameters
        # curl -H 'KEY: ADMIN123' http://192.168.178.102:8888/api/rest -H 'Content-Type: application/json' -d '{"index":"agents"}'
        payload = {"index": "agents"}

        agents = self.__contact_server__(payload)
        return agents

    def list_sources(self):
        """ List stored facts

        """
        # TODO: Add filters for specific platforms/executors  :  , platform_filter=None, executor_filter=None as parameters
        # curl -H 'KEY: ADMIN123' http://192.168.178.102:8888/api/rest -H 'Content-Type: application/json' -d '{"index":"agents"}'
        payload = {"index": "sources"}

        facts = self.__contact_server__(payload)
        return facts

    def list_adversaries(self):
        """ List registered adversaries """
        # curl -H 'KEY: ADMIN123' http://192.168.178.102:8888/api/rest -H 'Content-Type: application/json' -d '{"index":"adversaries"}'
        payload = {"index": "adversaries"}
        return self.__contact_server__(payload)

    def list_objectives(self):
        """ List registered objectives """
        # curl -H 'KEY: ADMIN123' http://192.168.178.102:8888/api/rest -H 'Content-Type: application/json' -d '{"index":"objectives"}'
        payload = {"index": "objectives"}
        return self.__contact_server__(payload)

    def add_sources(self, name: str, parameters):
        """ Adds a data source and seeds it with facts """

        payload = {"index": "sources",
                   "name": name,
                   # "id": "123456-1234-1234-1234-12345678",
                   "rules": [],
                   "relationships": []
                   }

        facts = []
        if parameters is not None:
            for key, value in parameters.items():
                facts.append({"trait": key, "value": value})

        # TODO: We need something better than a dict here as payload to have strong typing
        payload["facts"] = facts  # type: ignore

        print(payload)
        return self.__contact_server__(payload, method="put")

    def add_operation(self, **kwargs):
        """ Adds a new operation

        @param name: Name of the operation
        @param advid: Adversary id
        @param group: agent group to attack
        @param state: state to initially set
        @param obfuscator: obfuscator to use for the attack
        @param jitter: jitter to use for the attack
        @param parameters: parameters to pass to the ability
        """

        # name: str, advid: str, group: str = "red", state: str = "running", obfuscator: str = "plain-text", jitter: str = '4/8', parameters=None
        name: str = kwargs.get("name")
        advid: str = kwargs.get("adversary_id")
        group: str = kwargs.get("group", "red")
        state: str = kwargs.get("state", "running")
        obfuscator: str = kwargs.get("obfuscator", "plain-text")
        jitter: str = kwargs.get("jitter", "4/8")
        parameters = kwargs.get("parameters", None)

        # Add operation: curl -X PUT -H "KEY:$KEY" http://127.0.0.1:8888/api/rest -d '{"index":"operations","name":"testoperation1"}'
        # observed from GUI sniffing: PUT {'name': 'schnuffel2', 'group': 'red', 'adversary_id': '0f4c3c67-845e-49a0-927e-90ed33c044e0', 'state': 'running', 'planner': 'atomic', 'autonomous': '1', 'obfuscator': 'plain-text', 'auto_close': '1', 'jitter': '4/8', 'source': 'Alice Filters', 'visibility': '50'}

        sources_name = "source_" + name
        self.add_sources(sources_name, parameters)

        # To verify:
        # print(self.get_source(sources_name))

        payload = {"index": "operations",
                   "name": name,
                   "state": state,
                   "autonomous": 1,
                   'obfuscator': obfuscator,
                   'auto_close': '1',
                   'jitter': jitter,
                   'source': sources_name,
                   'visibility': '50',
                   "group": group,
                   #
                   "planner": "atomic",
                   "adversary_id": advid,
                   }

        return self.__contact_server__(payload, method="put")

    def view_operation_report(self, opid: str):
        """ views the operation report

        @param opid: Operation id to look for
        """

        # let postData = selectedOperationId ? {'index':'operation_report', 'op_id': selectedOperationId, 'agent_output': Number(agentOutput)} : null;
        # checking it (from snifffing protocol at the server): POST {'id': 539687}
        payload = {"index": "operation_report",
                   "op_id": opid,
                   'agent_output': 1
                   }
        return self.__contact_server__(payload)

    def set_operation_state(self, operation_id: str, state: str = "running"):
        """ Executes an operation on a server

        @param operation_id: The operation to modify
        @param state: The state to set this operation into
        """

        # TODO: Change state of an operation: curl -X POST -H "KEY:ADMIN123" http://localhost:8888/api/rest -d '{"index":"operation", "op_id":123, "state":"finished"}'
        # curl -X POST -H "KEY:ADMIN123" http://localhost:8888/api/rest -d '{"index":"operation", "op_id":123, "state":"finished"}'

        if state not in ["running", "finished", "paused", "run_one_link", "cleanup"]:
            raise ValueError

        payload = {"index": "operation",
                   "op_id": operation_id,
                   "state": state}
        return self.__contact_server__(payload)

    def add_adversary(self, name: str, ability: str, description: str = "created automatically"):
        """ Adds a new adversary

        @param name: Name of the adversary
        @param ability: One ability for this adversary
        @param description: Description of this adversary
        """

        # Add operation: curl -X PUT -H "KEY:$KEY" http://127.0.0.1:8888/api/rest -d '{"index":"operations","name":"testoperation1"}'

        # Sniffed from gui:
        # Rest core: PUT adversaries {'name': 'removeme', 'description': 'description', 'atomic_ordering': [{'id': 'bd527b63-9f9e-46e0-9816-b8434d2b8989'}], 'id': '558932cb-3ac6-43d2-b821-2db0fa8ad469', 'objective': ''}
        # Returns: [{'name': 'removeme', 'adversary_id': '558932cb-3ac6-43d2-b821-2db0fa8ad469', 'description': 'description', 'tags': [], 'atomic_ordering': ['bd527b63-9f9e-46e0-9816-b8434d2b8989'], 'objective': '495a9828-cab1-44dd-a0ca-66e58177d8cc'}]

        payload = {"index": "adversaries",
                   "name": name,
                   "description": description,
                   "atomic_ordering": [{"id": ability}],
                   #
                   "objective": '495a9828-cab1-44dd-a0ca-66e58177d8cc'  # default objective
                   # "objective": ''
                   }
        return self.__contact_server__(payload, method="put")

    # curl -X DELETE http://localhost:8888/api/rest -d '{"index":"operations","id":"$operation_id"}'
    def delete_operation(self, opid: str):
        """ Delete operation by id

        @param opid: Operation id
        """
        payload = {"index": "operations",
                   "id": opid}
        return self.__contact_server__(payload, method="delete")

    def delete_adversary(self, adid: str):
        """ Delete adversary by id

        @param adid: Adversary id
        """
        payload = {"index": "adversaries",
                   "adversary_id": [{"adversary_id": adid}]}
        return self.__contact_server__(payload, method="delete")

    def delete_agent(self, paw: str):
        """ Delete a specific agent from the kali db. implant may still be running and reconnect

        @param paw: The Id of the agent to delete
        """
        payload = {"index": "adversaries",
                   "paw": paw}
        return self.__contact_server__(payload, method="delete")

    def kill_agent(self, paw: str):
        """ Send a message to an agent to kill itself

        @param paw: The Id of the agent to delete
        """

        payload = {"index": "agents",
                   "paw": paw,
                   "watchdog": 1,
                   "sleep_min": 3,
                   "sleep_max": 3}

        return self.__contact_server__(payload, method="put")
