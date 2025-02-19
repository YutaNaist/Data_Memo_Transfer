from __future__ import annotations
from typing import TYPE_CHECKING

import requests
import urllib3
import json
import random

if TYPE_CHECKING:
    from TyDocDataMemoTransfer import TyDocDataMemoTransfer
# except BaseException:
#     pass


class TyMessageSender:

    def __init__(self, strUrlBase: str, doc: TyDocDataMemoTransfer):
        self.doc = doc
        self._urlBase = strUrlBase
        self.commandList = [
            "Check_UsageID",
            "Finish_Experiment",
            "read_Use_Information_From_Shared_Excel",
            "Check_And_Get_Single_Proposal",
            "Get_Meta_Data",
            "Copy_From_Original_To_Share",
            "Start_Experiment",
        ]
        requests.packages.urllib3.disable_warnings(
            urllib3.exceptions.InsecureRequestWarning
        )
        self.session = requests.Session()
        self.session.verify = False
        # self.session.trust_env = False

    def updateUrlBase(self, strUrlBase: str):
        self._urlBase = strUrlBase
        # self.session

    def sendMessage(self, url: str, args: dict) -> dict:
        try:
            identifier = int(random.random() * 1000000000)
            json_data = json.dumps({"args": args, "identifier": identifier})
            headers = {"Content-type": "application/json"}
            message = f"Send Message to Server: {url} {json_data}"
            self.doc.writeToLogger(message, "info")
            response = self.session.post(
                url, data=json_data, headers=headers, proxies={}
            )
            message = (
                f"Receive Message from Server: {response.status_code} {response.text}"
            )
            self.doc.writeToLogger(message, "info")
            # self.data_Model.write_to_logger(response)
            statusCode = response.status_code
            if statusCode == 500:
                return {
                    "status": False,
                    "message": "Internal Server Error. Please contact the administrator.",
                    "args": {},
                }
            if statusCode == 404:
                return {
                    "status": False,
                    "message": "Not Found. Please contact the administrator.",
                    "args": {},
                }
            if statusCode == 400:
                return {
                    "status": False,
                    "message": "Bad Request. Please contact the administrator.",
                    "args": {},
                }
            # dictReturnResponse = json.loads(response.text)
            dictReturnResponse = response.json()
            print(dictReturnResponse)
            returnIdentifier = dictReturnResponse["identifier"]
            if identifier != returnIdentifier:
                print("Resend Message")
                dictReturnResponse = self.sendMessage(url, args)

        except requests.exceptions.ConnectTimeout as e:
            print(e)
            return {
                "status": False,
                "message": "TimeoutError: Failed to connect Server. Please contact to the administrator",
                "args": {"error", e},
            }
        except requests.exceptions.ConnectionError as e:
            print(e)
            return {
                "status": False,
                "message": "ConnectionError Failed to connect Server. Please contact to the administrator.",
                "args": {"error", e},
            }
        return dictReturnResponse

    def sendRequestCheckID(self, strExperimentId: str) -> dict:
        args = {"experiment_id": strExperimentId}
        url = self._urlBase + "/check_usage_id"
        dictResponse = self.sendMessage(url, args)
        return dictResponse

    def sendRequestLogin(self, strExperimentId: str, password: str) -> dict:
        args = {"experiment_id": strExperimentId, "password": password}
        url = self._urlBase + "/login"
        dictResponse = self.sendMessage(url, args)
        return dictResponse

    def sendRequestFinishExperiment(
        self, doc: TyDocDataMemoTransfer, isAppendExisting: bool = False
    ) -> dict:
        url = self._urlBase + "/finish_experiment"
        args = {}
        args["experiment_id"] = doc.getExperimentId()
        args["share_directory"] = self.doc.getDictExperimentInformation(
            "str_share_directory_in_storage"
        )
        args["dict_experiment_information"] = doc.getAllDictExperimentInformation()
        # args["isAppendExisting"] = isAppendExisting
        # args["file_names"] = doc.getFileNameList()
        # args["meta_data"] = doc.getListDictMetaData()
        # args["experiment_information"] = doc.getAllDictExperimentInformation()
        print(id(self.doc))
        self.doc.writeToLogger(f"args = {args}")
        dictResponse = self.sendMessage(url, args)
        return dictResponse

    def sendRequestStartExperiment(
        self, str_Experiment_ID: str, doc: TyDocDataMemoTransfer
    ) -> dict:
        url = self._urlBase + "/start_experiment"
        args = {}
        args["experiment_id"] = str_Experiment_ID
        args["share_directory"] = doc.getDictExperimentInformation(
            "str_share_directory_in_storage"
        )
        dictResponse = self.sendMessage(url, args)
        return dictResponse

    def sendRequestSendOneTimePassword(
        self, strExperimentId: str, isSuperVisor: bool = False
    ) -> dict:
        args = {"experiment_id": strExperimentId, "is_send_supervisor": isSuperVisor}
        url = self._urlBase + "/request_one_time_password"
        dictResponse = self.sendMessage(url, args)
        return dictResponse

    def sendRequestRegisterPassword(
        self, strExperimentId: str, password: str, oneTimePassword: str
    ) -> dict:
        args = {
            "experiment_id": strExperimentId,
            "password": password,
            "one_time_password": oneTimePassword,
        }
        url = self._urlBase + "/register_password"
        dictResponse = self.sendMessage(url, args)
        return dictResponse

    def sendRequestCheckProposal(self, str_Experiment_ID: str) -> dict:
        args = {"experiment_id": str_Experiment_ID}
        dictResponse = self.sendMessage(self.commandList[3], args)
        return dictResponse

    def sendRequestGetMetaData(self, str_Experiment_ID: str) -> dict:
        args = {}
        args["experiment_id"] = str_Experiment_ID
        # print(self.commandList[4])
        dictResponse = self.sendMessage(self.commandList[4], args)
        return dictResponse

    def sendRequestCopyOriginal(
        self, str_Experiment_ID: str, data_Model: TyDocDataMemoTransfer
    ) -> dict:
        self.doc = data_Model
        args = {}
        args["experiment_id"] = str_Experiment_ID
        args["storagePC_share_directory"] = self.doc.getDictExperimentInformation(
            "str_share_directory_in_storage"
        )
        dictResponse = self.sendMessage(self.commandList[5], args)
        return dictResponse
