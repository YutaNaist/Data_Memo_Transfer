from __future__ import annotations
from typing import TYPE_CHECKING
from typing import TypedDict, Any, Optional, Union, Dict, TypeVar, Type, cast

# from typing import Dict

import requests
import urllib3
import json
import random
import logging
import traceback

if TYPE_CHECKING:
    from TyDocDataMemoTransfer import TyDocDataMemoTransfer


class MessageSenderException(Exception):
    """Custom exception for message sender errors."""

    def __init__(self, message: str, status_code: int, logger: logging.Logger):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        logger.error(f"MessageSenderError: {message}, Status Code: {status_code}")
        logger.debug(traceback.format_exc())


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


class TyRequestOneTimePasswordResponse(TypedDict):
    status: bool
    message: str
    status_code: int
    mail_address: str
    one_time_password: str


class TyRegisterPasswordResponse(TypedDict):
    status: bool
    message: str
    status_code: int


class TyStartExperimentResponse(TypedDict):
    status: bool
    message: str
    status_code: int
    experiment_information: Dict[str, Any]
    # experiment_information: TyExperimentInformation


class TyFinishExperimentResponse(TypedDict):
    status: bool
    message: str
    status_code: int
    experiment_information: Dict[str, Any]


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
        # requests.packages.urllib3.disable_warnings(
        #     urllib3.exceptions.InsecureRequestWarning
        # )
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
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
                raise MessageSenderException(
                    "Send count exceeded maximum limit. Please contact the administrator.",
                    408,
                    self.logger,
                )
            identifier = str(int(random.random() * 9999999999 + 1))
            # json_data = json.dumps(json_data)
            headers = {
                "Content-type": "application/json",
                "Diamond-Connection-Identifier": identifier,
            }
            jsonDataSend = json.dumps(jsonData, ensure_ascii=False).encode("utf-8")
            self.logger.info(f"Send, URL: {url}, Method: {methods}")
            self.logger.debug(f"Json Data: {jsonData}")
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
                raise MessageSenderException(
                    f"Invalid method {methods} for {url}.",
                    400,
                    self.logger,
                )
            statusCode = response.status_code
            self.logger.info(f"Get response, Status Code: {statusCode}")
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                raise MessageSenderException(
                    f"HTTPError: {e}",
                    response.status_code,
                    self.logger,
                )
            except requests.exceptions.RequestException as e:
                raise MessageSenderException(
                    f"RequestException: {e}",
                    400,
                    self.logger,
                )
            self.logger.debug(f"Header Keys: {list(response.headers.keys())}")
            dictReturnResponse = response.json()
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
        except requests.exceptions.ConnectTimeout:
            raise MessageSenderException(
                "Connection timed out while trying to connect to the server. Please contact to the administrator.",
                408,
                self.logger,
            )
        except requests.exceptions.ConnectionError:
            raise MessageSenderException(
                "Connection error occurred while trying to connect to the server. Please contact to the administrator.",
                408,
                self.logger,
            )
        self.logger.debug(f"Response Key: {list(dictReturnResponse.keys())}")
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
            # raise ValueError("Invalid response format for sendRequestLogin")
            raise MessageSenderException(
                "Invalid response format for sendRequestFinishExperiment",
                500,
                self.logger,
            )

        return cast(TyLoginResponse, dictResponse)

    def sendRequestFinishExperiment(
        self,
        strExperimentId: str,
        doc: TyDocDataMemoTransfer,
    ) -> TyFinishExperimentResponse:
        url = self._urlBase + f"/finish_experiment/{strExperimentId}"
        jsonData = {}
        # jsonData["experiment_id"] = strExperimentId
        jsonData["share_directory"] = self.doc.getDictExperimentInformation(
            "str_share_directory_in_storage"
        )
        jsonData["dict_experiment_information"] = doc.getAllDictExperimentInformation()
        dictResponse = self.sendMessage(url, jsonData, "POST")
        if not all(
            key in dictResponse
            for key in [
                "status",
                "message",
                "status_code",
                "experiment_information",
            ]
        ):
            raise MessageSenderException(
                "Invalid response format for sendRequestFinishExperiment",
                500,
                self.logger,
            )
            # raise ValueError("Invalid response format for sendRequestFinishExperiment")
        return cast(TyFinishExperimentResponse, dictResponse)

    def sendRequestStartExperiment(
        self, strExperimentId: str, doc: TyDocDataMemoTransfer
    ) -> TyStartExperimentResponse:
        url = self._urlBase + f"/start_experiment/{strExperimentId}"
        jsonData = {}
        jsonData["share_directory"] = doc.getDictExperimentInformation(
            "str_share_directory_in_storage"
        )
        dictResponse = self.sendMessage(url, jsonData, "POST")
        if not all(
            key in dictResponse
            for key in [
                "status",
                "message",
                "status_code",
                "experiment_information",
            ]
        ):
            # raise ValueError("Invalid response format for sendRequestStartExperiment")
            raise MessageSenderException(
                "Invalid response format for sendRequestFinishExperiment",
                500,
                self.logger,
            )
        # dictResponse = self.sendMessage(url, args)
        return cast(TyStartExperimentResponse, dictResponse)

    def sendRequestSendOneTimePassword(
        self, strExperimentId: str, isSuperVisor: bool = False, isDebug: bool = False
    ) -> TyRequestOneTimePasswordResponse:
        jsonData = {
            "is_send_to_supervisor": isSuperVisor,
            "is_debug": isDebug,
        }
        url = self._urlBase + f"/request_one_time_password/{strExperimentId}"
        dictResponse = self.sendMessage(url, jsonData=jsonData, methods="POST")

        if not all(
            key in dictResponse
            for key in [
                "status",
                "message",
                "status_code",
                "mail_address",
                "one_time_password",
            ]
        ):
            raise MessageSenderException(
                "Invalid response format for sendRequestFinishExperiment",
                500,
                self.logger,
            )
            # raise ValueError("Invalid response format for sendRequestLogin")
        return cast(TyRequestOneTimePasswordResponse, dictResponse)

    def sendRequestRegisterPassword(
        self, strExperimentId: str, password: str, oneTimePassword: str
    ) -> TyRegisterPasswordResponse:
        jsonData = {
            "experiment_id": strExperimentId,
            "password": password,
            "one_time_password": oneTimePassword,
        }
        url = self._urlBase + f"/register_password/{strExperimentId}"
        dictResponse = self.sendMessage(url, jsonData=jsonData, methods="POST")
        if not all(key in dictResponse for key in ["status", "message", "status_code"]):
            raise MessageSenderException(
                "Invalid response format for sendRequestFinishExperiment",
                500,
                self.logger,
            )
            # raise ValueError("Invalid response format for sendRequestRegisterPassword")
        return cast(TyRegisterPasswordResponse, dictResponse)

    def sendRequestLogout(self, strExperimentId: str) -> TyMessageSenderResponce:
        url = self._urlBase + f"/logout/{strExperimentId}"
        dictResponse = self.sendMessage(url, {}, "POST")
        if not all(key in dictResponse for key in ["status", "message", "status_code"]):
            # raise ValueError("Invalid response format for sendRequestLogOut")
            raise MessageSenderException(
                "Invalid response format for sendRequestFinishExperiment",
                500,
                self.logger,
            )
        return cast(TyMessageSenderResponce, dictResponse)

    # T = TypeVar("T", bound=TypedDict)

    # def validate_response(self, response: dict, response_type: Type[T]) -> T:
    #     """
    #     レスポンスの型を検証し、型が一致しない場合は例外をスローします。
    #     """
    #     try:
    #         # 型チェックを行い、型が一致しない場合は KeyError や TypeError をスロー
    #         return cast(response_type, response)
    #     except (KeyError, TypeError) as e:
    #         raise ValueError(f"Invalid response format: {e}")

    # def sendRequestCheckProposal(self, str_Experiment_ID: str) -> dict:
    #     args = {"experiment_id": str_Experiment_ID}
    #     dictResponse = self.sendMessage(self.commandList[3], args)
    #     return dictResponse

    # def sendRequestGetMetaData(self, str_Experiment_ID: str) -> dict:
    #     args = {}
    #     args["experiment_id"] = str_Experiment_ID
    #     # print(self.commandList[4])
    #     dictResponse = self.sendMessage(self.commandList[4], args)
    #     return dictResponse
