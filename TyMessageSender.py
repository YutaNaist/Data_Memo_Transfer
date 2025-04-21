from __future__ import annotations
from typing import TYPE_CHECKING
from typing import TypedDict, Any, Optional, Union, cast
# from typing import Dict

import requests
import urllib3
import json
import random
import logging

if TYPE_CHECKING:
    from TyDocDataMemoTransfer import TyDocDataMemoTransfer


# except BaseException:
#     pass
class TyMessageSenderResponce(TypedDict):
    status: bool
    message: str
    status_code: int
    # args: Dict[str, Any]


class TyProposalInfo(TypedDict):
    arim: dict[str, Optional[str]]
    date: dict[str, str]
    edit_url: str
    experiment_id: str
    instrument: dict[str, str]
    share: dict[str, Optional[str]]
    user: dict[str, Optional[str]]


class TyLoginResponse(TypedDict):
    message: str
    proposal: Union[TyProposalInfo, dict]
    status: bool
    status_code: int


class TyMessageSender:

    def __init__(self, strUrlBase: str, doc: TyDocDataMemoTransfer):
        self.doc = doc
        if self.doc.isBuild:
            self.logger = logging.getLogger("data_memo_transfer")
        else:
            self.logger = logging.getLogger("data_memo_transfer_debug")
            self.logger.setLevel(logging.DEBUG)

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

    def sendMessage(
        self,
        url: str,
        jsonData: dict[str, Any] = {},
        methods: str = "POST",
        sendCount: int = 0,
    ) -> dict[str, Any]:
        try:
            if sendCount > 10:
                return {
                    "status": False,
                    "message": "ConnectionError: Failed to connect Server. Please contact to the administrator",
                    "status_code": 408,
                }
            identifier = str(int(random.random() * 9999999999 + 1))
            # json_data = json.dumps(json_data)
            headers = {
                "Content-type": "application/json",
                "Diamond-Connection-Identifier": identifier,
            }
            message = f"Send Message to Server: {url}"
            # self.doc.writeToLogger(message, "info")
            self.logger.info(message)
            self.logger.debug(f"json data: {jsonData}")
            jsonDataSend = json.dumps(jsonData, ensure_ascii=False).encode("utf-8")
            if methods == "GET":
                response = self.session.get(
                    url, data=jsonDataSend, headers=headers, proxies={}
                )
            elif methods == "POST":
                response = self.session.post(
                    url, data=jsonDataSend, headers=headers, proxies={}
                )
            elif methods == "PUT":
                response = self.session.put(
                    url, data=jsonDataSend, headers=headers, proxies={}
                )
            elif methods == "DELETE":
                response = self.session.delete(
                    url, data=jsonDataSend, headers=headers, proxies={}
                )
            else:
                raise ValueError("Invalid method.")
            message = (
                f"Receive Message from Server: {response.status_code} {response.text}"
            )
            # self.doc.writeToLogger(message, "info")
            # self.data_Model.write_to_logger(response)
            statusCode = response.status_code
            self.logger.info(f"Get response, Status Code: {statusCode}")
            self.logger.debug(f"Header: {response.headers}")
            # self.logger.debug(f"Response: {response.text}")
            if statusCode == 500:
                return {
                    "status": False,
                    "message": "Internal Server Error. Please contact the administrator.",
                    "status_code": statusCode,
                }
            if statusCode == 404:
                return {
                    "status": False,
                    "message": "Not Found. Please contact the administrator.",
                    "status_code": statusCode,
                }
            if statusCode == 400:
                return {
                    "status": False,
                    "message": "Bad Request. Please contact the administrator.",
                    "status_code": statusCode,
                }
            if statusCode == 450:
                message = response.json()["message"]
                return {
                    "status": False,
                    "message": message,
                    "status_code": statusCode,
                }
            # dictReturnResponse = json.loads(response.text)
            dictReturnResponse = response.json()
            # print(dictReturnResponse)
            dictReturnResponse["status_code"] = statusCode
            returnIdentifier = response.headers.get(
                "Diamond-Connection-Identifier", None
            )
            self.logger.debug(
                f"Identifier Originale: {identifier}, Return: {returnIdentifier}"
            )
            if identifier != returnIdentifier:
                self.logger.error(
                    f"Identifier mismatch: {identifier} != {returnIdentifier}\nResend Message"
                )
                dictReturnResponse = self.sendMessage(
                    url, jsonData, methods, sendCount + 1
                )
        except requests.exceptions.ConnectTimeout as e:
            self.logger.warning(e)
            return {
                "status": False,
                "message": "TimeoutError: Failed to connect Server. Please contact to the administrator",
                "status_code": 408,
                "error": e,
            }
        except requests.exceptions.ConnectionError as e:
            self.logger.warning(e)
            return {
                "status": False,
                "message": "ConnectionError Failed to connect Server. Please contact to the administrator.",
                "status_code": 408,
                "error": e,
            }
        return dictReturnResponse

    def sendRequestCheckID(self, strExperimentId: str) -> dict[str, Any]:
        args = {"experiment_id": strExperimentId}
        url = self._urlBase + "/check_usage_id"
        dictResponse = self.sendMessage(url, args)
        return dictResponse

    def sendRequestLogin(self, strExperimentId: str, password: str) -> TyLoginResponse:
        # args = {"experiment_id": strExperimentId, "password": password}
        jsonData = {"password": password}
        url = self._urlBase + f"/login/{strExperimentId}"
        dictResponse = self.sendMessage(url, jsonData, "POST")

        # 実行時に型チェックを行う
        if not all(
            key in dictResponse
            for key in ["message", "proposal", "status", "status_code"]
        ):
            raise ValueError("Invalid response format for sendRequestLogin")

        return cast(TyLoginResponse, dictResponse)

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
        args = {"experiment_id": strExperimentId, "is_send_to_supervisor": isSuperVisor}
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
