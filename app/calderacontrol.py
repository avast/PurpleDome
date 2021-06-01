#!/usr/bin/env python3

""" Remote control a caldera server """

import json
import os
import time

import requests
import simplejson

from app.exceptions import CalderaError
from app.interface_sfx import CommandlineColors
from app.attack_log import AttackLog
from pprint import pprint, pformat


# TODO: Ability deserves an own class.
# TODO: Support Stealth settings: "plain-text obfuscation","base64 obfuscation","base64jumble obfuscation","caesar cipher obfuscation","base64noPadding obfuscation","steganography obfuscation"
# TODO: Support Jitter (min/max)
# TODO: Support all Caldera agents: "Sandcat (GoLang)","Elasticat (Blue Python/ Elasticsearch)","Manx (Reverse Shell TCP)","Ragdoll (Python/HTML)"

class CalderaControl():
    """ Remote control Caldera through REST api """

    def __init__(self, server, attack_logger, config=None, apikey=None):
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

    def fetch_client(self, platform="windows", file="sandcat.go", target_dir=".", extension=""):
        """ Downloads the appropriate Caldera client

        @param platform: Platform to download the agent for
        @param file: file to download from caldera. This defines the agent type
        @param target_dir: directory to drop the new file into
        @param extension: File extension to add to the downloaded file
        """
        header = {"platform": platform,
                  "file": file}
        fullurl = self.url + "file/download"
        request = requests.get(fullurl, headers=header)
        filename = request.headers["FILENAME"] + extension
        open(os.path.join(target_dir, filename), "wb").write(request.content)
        # print(r.headers)
        return filename

    def __contact_server__(self, payload, rest_path="api/rest", method="post"):
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
        except simplejson.errors.JSONDecodeError as exception:
            print("!!! Error !!!!")
            print(payload)
            print(request.text)
            print("!!! Error !!!!")
            raise exception

        return res

    #  ############## List
    def list_links(self, opid):
        """ List links associated with an operation

        @param opid: operation id to list links for
        """

        payload = {"index": "link",
                   "op_id": opid}
        return self.__contact_server__(payload)

    def list_results(self, linkid):
        """ List results for a link

        @param linkid: ID of the link
        """

        payload = {"index": "result",
                   "link_id": linkid}
        return self.__contact_server__(payload)

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

    def list_sources_for_name(self, name):
        """ List facts in a source pool with a specific name """

        for i in self.list_sources():
            if i["name"] == name:
                return i
        return None

    def list_facts_for_name(self, name):
        """ Pretty format for facts

        @param name: Name of the source ot look into
        """

        source = self.list_sources_for_name(name)

        if source is None:
            return {}

        res = {}
        for i in source["facts"]:
            res[i["trait"]] = {"value": i["value"],
                               "technique_id": i["technique_id"],
                               "collected_by": i["collected_by"]
                               }
        return res

    def list_paws_of_running_agents(self):
        """ Returns a list of all paws of running agents """
        return [i["paw"] for i in self.list_agents()]

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

    #  ######### Get one specific item

    def get_operation(self, name):
        """ Gets an operation by name

        @param name: Name of the operation to look for
        """

        for operation in self.list_operations():
            if operation["name"] == name:
                return operation
        return None

    def get_adversary(self, name):
        """ Gets a specific adversary by name

        @param name: Name to look for
        """
        for adversary in self.list_adversaries():
            if adversary["name"] == name:
                return adversary
        return None

    def get_objective(self, name):
        """ Returns an objective with a given name

        @param name: Name to filter for
        """
        for objective in self.list_objectives():
            if objective["name"] == name:
                return objective
        return None

    #  ######### Get by id

    def get_source(self, source_name):

        payload = {"index": "sources",
                   "name": source_name}
        return self.__contact_server__(payload)

    def get_ability(self, abid):
        """" Return an ability by id

        @param abid: Ability id
        """

        res = []

        for ability in self.list_abilities():
            if ability["ability_id"] == abid:
                res.append(ability)
        return res

    def does_ability_support_platform(self, abid: str, platform: str) -> bool:
        """ Checks if an ability supports a specific os

        @param abid: ability id.
        @param platform: os string to match for
        """

        # caldera knows the os-es "windows", "linux" and "darwin"

        for ability in self.get_ability(abid):
            if ability["platform"] == platform:
                return True
        return False

    def get_operation_by_id(self, op_id):
        """ Get operation by id

        @param op_id: Operation id
        """
        payload = {"index": "operations",
                   "id": op_id}
        return self.__contact_server__(payload)

    def get_result_by_id(self, linkid):
        """ Get the result from a link id

        @param linkid: link id
        """
        payload = {"index": "result",
                   "link_id": linkid}
        return self.__contact_server__(payload)

    def get_linkid(self, op_id, paw, ability_id):
        """ Get the id of a link identified by paw and ability_id

        @param op_id: Operation id
        @param paw: Paw of the agent
        @param ability_id: Ability id to filter for
        """
        operation = self.get_operation_by_id(op_id)

        # print("Check for: {} {}".format(paw, ability_id))
        for alink in operation[0]["chain"]:
            # print("Lookup: PAW: {} Ability: {}".format(alink["paw"], alink["ability"]["ability_id"]))
            # print("In: " + str(alink))
            if alink["paw"] == paw and alink["ability"]["ability_id"] == ability_id:
                return alink["id"]

        return None

    #  ######### View

    def view_operation_report(self, opid):
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

    def view_operation_output(self, opid, paw, ability_id):
        """ Gets the output of an executed ability

        @param opid: Id of the operation to look for
        @param paw: Paw of the agent to look up
        @param ability_id: if of the ability to extract the output from
        """
        orep = self.view_operation_report(opid)

        if paw not in orep["steps"]:
            print("Broken operation report:")
            pprint(orep)
            print(f"Could not find {paw} in {orep['steps']}")
            raise CalderaError
        # print("oprep: " + str(orep))
        for a_step in orep["steps"][paw]["steps"]:
            if a_step["ability_id"] == ability_id:
                try:
                    return a_step["output"]
                except KeyError as exception:
                    raise CalderaError from exception
        # print(f"Did not find ability {ability_id} in caldera operation output")
        return None

    #  ######### Add

    def add_sources(self, name, parameters):
        """ Adds a data source and seeds it with facts """

        payload = {"index": "sources",
                   "name": name,
                   # "id": "123456-1234-1234-1234-12345678",
                   "rules": [],
                   "relationships": []
                   }

        facts = []
        if parameters is not None:
            for k, v in parameters.items():
                facts.append({"trait": k, "value": v})
        payload["facts"] = facts

        print(payload)
        return self.__contact_server__(payload, method="put")

    def add_operation(self, name, advid, group="red", state="running", obfuscator="plain-text", jitter='4/8', parameters=None):
        """ Adds a new operation

        @param name: Name of the operation
        @param advid: Adversary id
        @param group: agent group to attack
        @param state: state to initially set
        @param obfuscator: obfuscator to use for the attack
        @param jitter: jitter to use for the attack
        @param parameters: parameters to pass to the ability
        """

        # Add operation: curl -X PUT -H "KEY:$KEY" http://127.0.0.1:8888/api/rest -d '{"index":"operations","name":"testoperation1"}'
        # observed from GUI sniffing: PUT {'name': 'schnuffel2', 'group': 'red', 'adversary_id': '0f4c3c67-845e-49a0-927e-90ed33c044e0', 'state': 'running', 'planner': 'atomic', 'autonomous': '1', 'obfuscator': 'plain-text', 'auto_close': '1', 'jitter': '4/8', 'source': 'Alice Filters', 'visibility': '50'}

        sources_name = "source_" + name
        self.add_sources(sources_name, parameters)

        print("Got:")
        print(self.get_source("source_name"))

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

    def add_adversary(self, name, ability, description="created automatically"):
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

    #  ######### Execute

    # TODO View the abilities a given agent could execute. curl -H "key:$API_KEY" -X POST localhost:8888/plugin/access/abilities -d '{"paw":"$PAW"}'

    def execute_ability(self, paw, ability_id, obfuscator="plain-text", parameters=None):
        """ Executes an ability on a target. This happens outside of the scop of an operation. You will get no result of the ability back

        @param paw: Paw of the target
        @param ability_id: ability to execute
        @param obfuscator: Obfuscator to use
        @param parameters: parameters to pass to the ability
        """

        # curl -H "key:ADMIN123" -X POST localhost:8888/plugin/access/exploit -d '{"paw":"$PAW","ability_id":"$ABILITY_ID"}'```
        # You can optionally POST an obfuscator and/or a facts dictionary with key/value pairs to fill in any variables the chosen ability requires.
        # {"paw":"$PAW","ability_id":"$ABILITY_ID","obfuscator":"base64","facts":[{"trait":"username","value":"admin"},{"trait":"password", "value":"123"}]}
        payload = {"paw": paw,
                   "ability_id": ability_id,
                   "obfuscator": obfuscator}

        facts = []
        if parameters is not None:
            for k, v in parameters.items():
                facts.append({"trait": k, "value": v})
        payload["facts"] = facts

        print(payload)

        return self.__contact_server__(payload, rest_path="plugin/access/exploit_ex")

    def execute_operation(self, operation_id, state="running"):
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

    #  ######### Delete

    # curl -X DELETE http://localhost:8888/api/rest -d '{"index":"operations","id":"$operation_id"}'
    def delete_operation(self, opid):
        """ Delete operation by id

        @param opid: Operation id
        """
        payload = {"index": "operations",
                   "id": opid}
        return self.__contact_server__(payload, method="delete")

    def delete_adversary(self, adid):
        """ Delete adversary by id

        @param adid: Adversary id
        """
        payload = {"index": "adversaries",
                   "adversary_id": [{"adversary_id": adid}]}
        return self.__contact_server__(payload, method="delete")

    def delete_agent(self, paw):
        """ Delete a specific agent from the kali db. implant may still be running and reconnect

        @param paw: The Id of the agent to delete
        """
        payload = {"index": "adversaries",
                   "paw": paw}
        return self.__contact_server__(payload, method="delete")

    def kill_agent(self, paw):
        """ Send a message to an agent to kill itself

        @param paw: The Id of the agent to delete
        """

        payload = {"index": "agents",
                   "paw": paw,
                   "watchdog": 1,
                   "sleep_min": 3,
                   "sleep_max": 3}

        return self.__contact_server__(payload, method="put")

    def delete_all_agents(self):
        """ Delete all agents from kali db """

        agents = self.list_paws_of_running_agents()
        for paw in agents:
            self.delete_agent(paw)

    def kill_all_agents(self):
        """ Send a message to all agent to kill itself """

        agents = self.list_paws_of_running_agents()
        for paw in agents:
            self.kill_agent(paw)

    #  ######### File access

    # TODO: Get uploaded files

    #  Link, chain and stuff

    def is_operation_finished(self, opid, debug=False):
        """ Checks if an operation finished - finished is not necessary successful !

        @param opid: Operation id to check
        @param debug: Additional debug output
        """
        # An operation can run several Abilities vs several targets (agents). Each one is a link in the chain (see opperation report).
        # Those links can have the states:
        #         return dict(HIGH_VIZ=-5,
        #                     UNTRUSTED=-4,
        #                     EXECUTE=-3,
        #                     DISCARD=-2,
        #                     PAUSE=-1)
        # Plus: 0 as "finished"
        #

        operation = self.get_operation_by_id(opid)
        if debug:
            print(f"Operation data {operation}")
        try:
            # print(operation[0]["state"])
            if operation[0]["state"] == "finished":
                return True
        except KeyError as exception:
            raise CalderaError from exception
        except IndexError as exception:
            raise CalderaError from exception

        return False

    def is_operation_finished_multi(self, opid):
        """ Checks if an operation finished - finished is not necessary successful ! On several targets.

        All links (~ abilities) on all targets must have the status 0 for this to be True.

        @param opid: Operation id to check
        """
        # An operation can run several Abilities vs several targets (agents). Each one is a link in the chain (see opperation report).
        # Those links can have the states:
        #         return dict(HIGH_VIZ=-5,
        #                     UNTRUSTED=-4,
        #                     EXECUTE=-3,
        #                     DISCARD=-2,
        #                     PAUSE=-1)
        # Plus: 0 as "finished"
        #

        operation = self.get_operation_by_id(opid)
        # print(f"Operation data {operation}")
        try:
            for host_group in operation[0]["host_group"]:
                for alink in host_group["links"]:
                    if alink["status"] != 0:
                        return False
        except Exception as exception:
            raise CalderaError from exception
        return True

    #  ######## All inclusive methods

    def attack(self, attack_logger: AttackLog = None, paw="kickme", ability_id="bd527b63-9f9e-46e0-9816-b8434d2b8989", group="red", target_platform=None, parameters = None):
        """ Attacks a system and returns results

        @param attack_logger: An attack logger class to log attacks with
        @param paw: Paw to attack
        @param group: Group to attack. Paw must be in the group
        @param ability_id: Ability to run against the target
        @param target_platform: Platform of the target machine. Optional. Used for quick-outs
        @param parameters: Dict containing key-values of parameters to pass to the ability

        @:return : True if the attack was executed. False if it was not. For example the target os is not supported by this attack
        """

        # Tested obfuscators (with sandcat):
        # plain-text: worked
        # base64:  (invalid input on sandcat)
        # base64jumble: ?
        # caesar: failed
        # base64noPadding: worked
        # steganopgraphy: ?
        obfuscator = self.config.get_caldera_obfuscator()
        jitter = self.config.get_caldera_jitter()

        adversary_name = "generated_adv__" + str(time.time())
        operation_name = "testoperation__" + str(time.time())

        if target_platform:
            # Check if an ability does support the platform of the target:
            if not self.does_ability_support_platform(ability_id, target_platform):
                self.attack_logger.vprint(
                    f"{CommandlineColors.FAIL}Platform {target_platform} not supported by {ability_id}{CommandlineColors.ENDC}",
                    1)
                return False

        self.add_adversary(adversary_name, ability_id)
        adid = self.get_adversary(adversary_name)["adversary_id"]

        if attack_logger:
            attack_logger.start_caldera_attack(source=self.url,
                                               paw=paw,
                                               group=group,
                                               ability_id=ability_id,
                                               ttp=self.get_ability(ability_id)[0]["technique_id"],
                                               name=self.get_ability(ability_id)[0]["name"],
                                               description=self.get_ability(ability_id)[0]["description"],
                                               obfuscator=obfuscator,
                                               jitter=jitter
                                               )

        #  ##### Create / Run Operation

        self.attack_logger.vprint(f"New adversary generated. ID: {adid}, ability: {ability_id} group: {group}", 2)
        res = self.add_operation(operation_name,
                                 advid=adid,
                                 group=group,
                                 obfuscator=obfuscator,
                                 jitter=jitter,
                                 parameters=parameters
                                 )
        self.attack_logger.vprint(pformat(res), 3)

        opid = self.get_operation(operation_name)["id"]
        self.attack_logger.vprint("New operation created. OpID: " + str(opid), 3)

        self.execute_operation(opid)
        self.attack_logger.vprint("Execute operation", 3)
        retries = 30
        ability_name = self.get_ability(ability_id)[0]["name"]
        ability_description = self.get_ability(ability_id)[0]["description"]
        self.attack_logger.vprint(f"{CommandlineColors.OKBLUE}Executed attack operation{CommandlineColors.ENDC}", 1)
        self.attack_logger.vprint(f"{CommandlineColors.BACKGROUND_BLUE} PAW: {paw} Group: {group} Ability: {ability_id}  {CommandlineColors.ENDC}", 1)
        self.attack_logger.vprint(f"{CommandlineColors.BACKGROUND_BLUE} {ability_name}: {ability_description}  {CommandlineColors.ENDC}", 1)
        while not self.is_operation_finished(opid) and retries > 0:
            self.attack_logger.vprint(f".... waiting for Caldera to finish {retries}", 2)
            time.sleep(10)
            retries -= 1
            if retries <= 0:
                self.attack_logger.vprint(f"{CommandlineColors.FAIL}Ran into retry timeout waiting for attack to finish{CommandlineColors.ENDC}", 1)

        # TODO: Handle outout from several clients

        retries = 5
        output = None
        while retries > 0:
            try:
                retries -= 1
                time.sleep(10)
                output = self.view_operation_output(opid, paw, ability_id)
                self.attack_logger.vprint(f".... getting Caldera output {retries}", 2)
                if output:
                    break
            except CalderaError:
                pass

        if output is None:
            output = str(self.get_operation_by_id(opid))
            self.attack_logger.vprint(f"{CommandlineColors.FAIL}Failed getting operation data. We just have: {output} from get_operation_by_id{CommandlineColors.ENDC}", 0)
        else:
            outp = str(output)
            self.attack_logger.vprint(f"{CommandlineColors.BACKGROUND_GREEN} Output: {outp} {CommandlineColors.ENDC}", 2)
            pprint(output)

        self.attack_logger.vprint(self.list_facts_for_name("source_"+operation_name), 2)

        #  ######## Cleanup
        self.execute_operation(opid, "cleanup")
        self.delete_adversary(adid)
        self.delete_operation(opid)
        if attack_logger:
            attack_logger.stop_caldera_attack(source=self.url,
                                              paw=paw,
                                              group=group,
                                              ability_id=ability_id,
                                              ttp=self.get_ability(ability_id)[0]["technique_id"],
                                              name=self.get_ability(ability_id)[0]["name"],
                                              description=self.get_ability(ability_id)[0]["description"],
                                              obfuscator=obfuscator,
                                              jitter=jitter
                                              )
        return True

    def pretty_print_ability(self, abi):
        """ Pretty pritns an ability

        @param abi: A ability dict
        """

        print("""
        TTP: {technique_id}
        Technique name: {technique_name}
        Tactic: {tactic}
        Name: {name}
        ID: {ability_id}
        Description: {description}
        Platform: {platform}/{executor}

        """.format(**abi))
