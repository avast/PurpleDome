#!/usr/bin/env python3

""" Remote control a caldera server """

import os
import time

from pprint import pprint, pformat
from typing import Optional
import requests

from app.exceptions import CalderaError, ConfigurationError
from app.interface_sfx import CommandlineColors

# from app.calderaapi_2 import CalderaAPI
from app.calderaapi_4 import CalderaAPI, Operation, Source, Adversary, Objective, Ability


# TODO: Ability deserves an own class.
# TODO: Support all Caldera agents: "Sandcat (GoLang)","Elasticat (Blue Python/ Elasticsearch)","Manx (Reverse Shell TCP)","Ragdoll (Python/HTML)"

class CalderaControl(CalderaAPI):
    """ Remote control Caldera through REST api """

    def fetch_client(self, platform: str = "windows", file: str = "sandcat.go", target_dir: str = ".", extension: str = "") -> str:
        """ Downloads the appropriate Caldera client

        :param platform: Platform to download the agent for
        :param file: file to download from caldera. This defines the agent type
        :param target_dir: directory to drop the new file into
        :param extension: File extension to add to the downloaded file
        :returns: filename of the client
        """
        header = {"platform": platform,
                  "file": file}
        fullurl = self.url + "file/download"
        request = requests.get(fullurl, headers=header)
        filename = request.headers["FILENAME"] + extension
        with open(os.path.join(target_dir, filename), "wb") as fh:
            fh.write(request.content)
        # print(r.headers)
        return filename

    def list_sources_for_name(self, name: str) -> Optional[Source]:
        """ List facts in a source pool with a specific name

        :param name: The name of the source pool
        :returns: The source data or None
        """

        for i in self.list_sources():
            if i.get("name") == name:
                return i
        return None

    def list_facts_for_name(self, name: str) -> dict:
        """ Pretty format for facts

        :param name: Name of the source ot look into
        :returns: A pretty dict with facts
        """

        source = self.list_sources_for_name(name)

        if source is None:
            return {}

        res = {}
        if source is not None:
            facts = source.get("facts")
            if facts is not None:
                for fact in facts:
                    res[fact.get("trait")] = {"value": fact.get("value"),
                                              "technique_id": fact.get("technique_id"),
                                              "collected_by": fact.get("collected_by")
                                              }
        return res

    def list_paws_of_running_agents(self) -> list[str]:
        """ Returns a list of all paws of running agents

        :returns: A list of running agents (or better: the list of their paws)
        """
        return [i.get("paw") for i in self.list_agents()]    # 2.8.1 version
        # return [i.paw for i in self.list_agents()]  # 4* version

    #  ######### Get one specific item
    def get_operation(self, name: str) -> Optional[Operation]:
        """ Gets an operation by name

        :param name: Name of the operation to look for
        :returns: The operation as dict
        """

        for operation in self.list_operations():
            if operation.get("name") == name:
                return operation
        return None

    def get_adversary(self, name: str) -> Optional[Adversary]:
        """ Gets a specific adversary by name

        :param name: Name to look for
        :returns: The adversary as dict
        """
        for adversary in self.list_adversaries():
            if adversary.get("name") == name:
                return adversary
        return None

    def get_objective(self, name: str) -> Optional[Objective]:
        """ Returns an objective with a given name

        :param name: Name to filter for
        :returns: The objective as dict
        """
        for objective in self.list_objectives():
            if objective.get("name") == name:
                return objective
        return None

    def get_ability(self, abid: str) -> list[Ability]:
        """ Return an ability by id

        :param abid: Ability id
        :returns: a list of abilities
        """

        res = []

        print(f"Number of abilities: {len(self.list_abilities())}")

        with open("debug_removeme.txt", "wt") as fh:
            fh.write(pformat(self.list_abilities()))

        for ability in self.list_abilities():
            if ability.get("ability_id", None) == abid or ability.get("auto_generated_guid", None) == abid:
                res.append(ability)
        return res

    def does_ability_support_platform(self, abid: str, platform: str) -> bool:
        """ Checks if an ability supports a specific os

        :param abid: ability id.
        :param platform: os string to match for
        :returns: True if platform is supported
        """

        # caldera knows the os-es "windows", "linux" and "darwin"

        abilities = self.get_ability(abid)

        for ability in abilities:
            if ability.get("platform") == platform:
                return True
            if platform in ability.get("supported_platforms", []):
                return True
            if platform in ability.get("platforms", []):
                return True
            executors = ability.get("executors")   # For Caldera 4.*
            if executors is not None:
                for executor in executors:
                    if executor.get("platform") == platform:
                        return True
        print(self.get_ability(abid))
        return False

    def get_operation_by_id(self, op_id: str) -> list[Operation]:
        """ Get operation by id

        :param op_id: Operation id
        :returns: a list of operations matching the id
        """
        operations = self.list_operations()

        if operations is not None:
            for an_operation in operations:
                if an_operation.get("id") == op_id:
                    return [an_operation]
        return []

    def get_linkid(self, op_id: str, paw: str, ability_id: str) -> Optional[dict]:
        """ Get the id of a link identified by paw and ability_id

        :param op_id: Operation id
        :param paw: Paw of the agent
        :param ability_id: Ability id to filter for
        :returns: The ability
        """
        operation = self.get_operation_by_id(op_id)

        # print("Check for: {} {}".format(paw, ability_id))
        if len(operation) == 0:
            return None
        if operation[0].chain is None:
            return None
        for alink in operation[0].chain:
            # print("Lookup: PAW: {} Ability: {}".format(alink["paw"], alink["ability"]["ability_id"]))
            # print("In: " + str(alink))
            if alink.paw == paw and alink.ability.ability_id == ability_id:
                return alink.id

        return None

    #  ######### View

    def view_operation_output(self, opid: str, paw: str, ability_id: str) -> Optional[dict]:
        """ Gets the output of an executed ability

        :param opid: Id of the operation to look for
        :param paw: Paw of the agent to look up
        :param ability_id: if of the ability to extract the output from
        :returns: The output
        """
        orep = self.view_operation_report(opid)

        # print(orep)
        if paw not in orep["steps"]:
            print("Broken operation report:")
            pprint(orep)
            print(f"Could not find {paw} in {orep['steps']}")
            raise CalderaError
        # print("oprep: " + str(orep))
        for a_step in orep.get("steps").get(paw).get("steps"):  # type: ignore
            if a_step.get("ability_id") == ability_id:
                try:
                    return a_step.get("output")
                except KeyError as exception:
                    raise CalderaError from exception
        # print(f"Did not find ability {ability_id} in caldera operation output")
        return None

    #  ######### Delete

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

    def is_operation_finished(self, opid: str, debug: bool = False) -> bool:
        """ Checks if an operation finished - finished is not necessary successful !

        :param opid: Operation id to check
        :param debug: Additional debug output
        :returns: True if the operation is finished
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

        # TODO: Maybe try to get the report and continue until we have it. Could be done in addition.

        operation = self.get_operation_by_id(opid)
        if debug:
            print(f"Operation data {operation}")
        try:
            # print(operation[0]["state"])
            if operation[0].get("state") == "finished":
                return True
        except KeyError as exception:
            raise CalderaError from exception
        except IndexError as exception:
            raise CalderaError from exception

        return False

    def is_operation_finished_multi(self, opid: str) -> bool:
        """ Checks if an operation finished - finished is not necessary successful ! On several targets.

        All links (~ abilities) on all targets must have the status 0 for this to be True.

        :param opid: Operation id to check
        :returns: True if the operation is finished
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

        operation: list[Operation] = self.get_operation_by_id(opid)
        # print(f"Operation data {operation}")
        try:
            for host_group in operation[0].host_group:
                for alink in host_group.links:
                    if alink.status != 0:
                        return False
        except Exception as exception:
            raise CalderaError from exception
        return True

    #  ######## All inclusive methods

    def attack(self, paw: str = "kickme", ability_id: str = "bd527b63-9f9e-46e0-9816-b8434d2b8989",
               group: str = "red", target_platform: Optional[str] = None, parameters: Optional[dict] = None, **kwargs) -> bool:
        """ Attacks a system and returns results

        :param paw: Paw to attack
        :param group: Group to attack. Paw must be in the group
        :param ability_id: Ability to run against the target
        :param target_platform: Platform of the target machine. Optional. Used for quick-outs
        :param parameters: Dict containing key-values of parameters to pass to the ability

        :returns: True if the attack was executed. False if it was not. For example the target os is not supported by this attack
        """

        # Tested obfuscators (with sandcat):
        # plain-text: worked
        # base64:  (invalid input on sandcat)
        # base64jumble: ?
        # caesar: failed
        # base64noPadding: worked
        # steganopgraphy: ?
        if self.config is None:
            raise ConfigurationError("No Config")
        obfuscator: str = self.config.get_caldera_obfuscator()
        jitter: str = self.config.get_caldera_jitter()

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
        adversary = self.get_adversary(adversary_name)
        if adversary is None:
            raise CalderaError("Could not get adversary")
        adid = adversary.get("adversary_id", None)
        if adid is None:
            raise CalderaError("Could not get adversary by id")

        logid = self.attack_logger.start_caldera_attack(source=self.url,
                                                        paw=paw,
                                                        group=group,
                                                        ability_id=ability_id,
                                                        ttp=self.get_ability(ability_id)[0].get("technique_id"),
                                                        name=self.get_ability(ability_id)[0].get("name"),
                                                        description=self.get_ability(ability_id)[0].get("description"),
                                                        obfuscator=obfuscator,
                                                        jitter=jitter,
                                                        **kwargs
                                                        )

        #  ##### Create / Run Operation

        self.attack_logger.vprint(f"New adversary generated. ID: {adid}, ability: {ability_id} group: {group}", 2)
        res = self.add_operation(name=operation_name,
                                 adversary_id=adid,
                                 group=group,
                                 obfuscator=obfuscator,
                                 jitter=jitter,
                                 parameters=parameters
                                 )
        self.attack_logger.vprint(pformat(res), 3)

        operation = self.get_operation(operation_name)
        if operation is None:
            raise CalderaError("Was not able to get operation")
        opid = operation.get("id")
        if opid is None:
            raise CalderaError("Was not able to get operation. Broken ID")
        self.attack_logger.vprint("New operation created. OpID: " + str(opid), 3)

        self.set_operation_state(opid)
        self.attack_logger.vprint("Execute operation", 3)
        retries = 30
        ability_name = self.get_ability(ability_id)[0].get("name")
        ability_description = self.get_ability(ability_id)[0].get("description")
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

        outp = ""

        if output is None:
            outp = str(self.get_operation_by_id(opid))
            self.attack_logger.vprint(f"{CommandlineColors.FAIL}Failed getting operation data. We just have: {outp} from get_operation_by_id{CommandlineColors.ENDC}", 0)
        else:
            outp = str(output)
            self.attack_logger.vprint(f"{CommandlineColors.BACKGROUND_GREEN} Output: {outp} {CommandlineColors.ENDC}", 2)
            pprint(output)

        self.attack_logger.vprint(str(self.list_facts_for_name("source_" + operation_name)), 2)

        #  ######## Cleanup
        self.set_operation_state(opid, "cleanup")
        self.delete_adversary(adid)
        self.delete_operation(opid)
        self.attack_logger.stop_caldera_attack(source=self.url,
                                               paw=paw,
                                               group=group,
                                               ability_id=ability_id,
                                               ttp=self.get_ability(ability_id)[0].get("technique_id"),
                                               name=self.get_ability(ability_id)[0].get("name"),
                                               description=self.get_ability(ability_id)[0].get("description"),
                                               obfuscator=obfuscator,
                                               jitter=jitter,
                                               logid=logid,
                                               result=[outp]
                                               )
        return True

    def pretty_print_ability(self, abi):
        """ Pretty pritns an ability

        :param abi: A ability dict
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
