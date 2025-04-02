import copy
import json
import logging.config
import os
import datetime
import logging

# import urllib3
import hashlib
import base64

from TyMessageSender import TyMessageSender
from PyQt5 import QtWidgets

from controller.TyDialogLogin import TyDialogLogin
from controller.TyDialogSendOneTimePassword import TyDialogSendOneTimePassword
from controller.TyDialogRegisterPassword import TyDialogRegisterPassword
from controller.TyDialogSetInitial import TyDialogSetInitial
from controller.TyMainWindow import TyMainWindow


class DataModel_DataMemoTransfer_Exception(Exception):
    def __init__(self):
        pass


class DataModel_DataMemoTransfer_TypeException(DataModel_DataMemoTransfer_Exception):
    def __str__(self):
        return "DataModelException DataMemoTransfer: Different Type is used."


class TyDocDataMemoTransfer:
    def __init__(self):
        self.isBuild = False
        self.dictExperimentInformation = {}
        self.list_keys = [
            "str_url_diamond",
            "str_save_directory",
            "str_share_directory_in_storage",
            "str_experiment_id",
            "is_upload_arim",
            "is_share_with_google",
            "dict_user_information",
            "is_exist_temp_file",
            "dict_clipboard",
            "list_file_data",
            "str_parent_id_in_google_drive",
            "str_mail_address",
        ]
        self.list_keys_data = [
            "filename",
            "index",
            "classified",
            "valid",
            "arim_upload",
            "comment",
            "experiment",
            "sample",
            "equipment",
        ]
        self._logger = logging.getLogger(__name__)
        self.initializeExperimentInformation()
        urlBase = self.getDictExperimentInformation("str_url_diamond")
        self.messageSender = TyMessageSender(urlBase, self)
        self.__hashPassword = ""
        self.viewState = "log_in"
        self.currentWindow = None

    def initializeExperimentInformation(self):
        self.dictExperimentInformation["str_url_diamond"] = "http://192.168.0.10:5462"
        self.dictExperimentInformation["str_save_directory"] = "Z:/"
        self.dictExperimentInformation["str_share_directory_in_storage"] = (
            "C:/Share/SmartLab/"
        )
        self.dictExperimentInformation["str_experiment_id"] = ""
        self.dictExperimentInformation["dict_user_information"] = {}
        self.dictExperimentInformation["is_exist_temp_file"] = False
        self.dictExperimentInformation["is_upload_arim"] = False
        self.dictExperimentInformation["is_share_with_google"] = False
        self.dictExperimentInformation["str_parent_id_in_google_drive"] = ""
        self.dictExperimentInformation["str_mail_address"] = ""
        # self.dict_Data_Model["list_file_name"] = []
        self.dictExperimentInformation["dict_clipboard"] = {}
        self.dictExperimentInformation["list_file_data"] = []

        dict_Template_Clipboard = {}
        dict_Template_Clipboard["filename"] = ""
        dict_Template_Clipboard["index"] = -1
        dict_Template_Clipboard["classified"] = "Unclassified"
        dict_Template_Clipboard["valid"] = False
        dict_Template_Clipboard["arim_upload"] = False
        dict_Template_Clipboard["comment"] = ""

        dict_Template_Clipboard["experiment"] = {}
        dict_Template_Clipboard["experiment"]["title"] = ""
        dict_Template_Clipboard["experiment"]["comment"] = ""
        dict_Template_Clipboard["sample"] = {}
        dict_Template_Clipboard["sample"]["id"] = ""
        dict_Template_Clipboard["sample"]["name"] = ""
        dict_Template_Clipboard["sample"]["comment"] = ""
        dict_Template_Clipboard["equipment"] = {}
        dict_Template_Clipboard["equipment"]["method"] = ""
        self.dictExperimentInformation["dict_clipboard"] = dict_Template_Clipboard

    # Function of Template Data
    def getAllDictExperimentInformation(self):
        return self.dictExperimentInformation

    def setAllDictExperimentInformation(self, dictExperimentInformation):
        for key, value in dictExperimentInformation.items():
            if key not in self.list_keys:
                raise DataModel_DataMemoTransfer_Exception
            else:
                self.dictExperimentInformation[key] = value

    def getDictExperimentInformation(self, key):
        try:
            return self.dictExperimentInformation[key]
        except KeyError:
            return ""

    def setDiCtExperimentInformation(self, key, value):
        # if isinstance(value, type(self.dict_Data_Model[key])):
        if type(value) != type(self.dictExperimentInformation[key]):
            raise DataModel_DataMemoTransfer_TypeException
        self.dictExperimentInformation[key] = value

    def setNumberOfFiles(self) -> int:
        return len(self.dictExperimentInformation["list_file_data"])

    def saveToTemporary(self) -> None:
        self.dictExperimentInformation["is_exist_temp_file"] = True
        json.dump(
            self.dictExperimentInformation,
            open("temporary.json", "w", encoding="utf-8"),
            ensure_ascii=False,
            indent=4,
        )
        self.writeToLogger("save temporary")

    def loadFromTemporary(self) -> bool:
        try:
            docLoad = json.load(open("temporary.json", "r", encoding="utf-8"))
            if docLoad == {}:
                raise FileNotFoundError
            self.dictExperimentInformation = docLoad
            self.dictExperimentInformation["is_exist_temp_file"] = True
            self.writeToLogger("load temporary")
            return True
        except FileNotFoundError:
            self.dictExperimentInformation["is_exist_temp_file"] = False
            self.writeToLogger("Temporary file not found")
            return False
        except json.decoder.JSONDecodeError:
            self.dictExperimentInformation["is_exist_temp_file"] = False
            self.writeToLogger("Temporary file can't read")
            return False

    def deleteTemporary(self) -> None:
        os.remove("temporary.json")
        self.dictExperimentInformation["is_exist_temp_file"] = False
        self.writeToLogger("delete temporary file")

    def getFillClipboard(self) -> dict:
        return copy.copy(self.dictExperimentInformation["dict_clipboard"])

    def getAllFileInformation(self) -> list:
        return self.dictExperimentInformation["list_file_data"]

    def getFileNameList(self) -> list:
        list_File_Name = []
        for dict_File_Information in self.dictExperimentInformation["list_file_data"]:
            list_File_Name.append(dict_File_Information["filename"])
        return list_File_Name

    def resetFileData(self) -> None:
        self.dictExperimentInformation["list_file_data"] = []

    def addFileInformation(self, dict_File_Information: dict) -> None:
        self.dictExperimentInformation["list_file_data"].append(dict_File_Information)

    def getFileInformation(self, index: int) -> dict:
        if index == -1:
            return copy.copy(self.dictExperimentInformation["dict_clipboard"])
        else:
            return self.dictExperimentInformation["list_file_data"][index]

    def setFileInformation(self, index: int, dict_File_Information: dict) -> None:
        if index == -1:
            self.dictExperimentInformation["dict_clipboard"] = dict_File_Information
        else:
            self.dictExperimentInformation["list_file_data"][
                index
            ] = dict_File_Information

    def checkIndexFileName(self, str_File_Name: str) -> int:
        list_file_names = self.getFileNameList()
        if str_File_Name in list_file_names:
            return list_file_names.index(str_File_Name)
        else:
            return -1

    # meta data converter for diamond
    def getListDictMetaData(self) -> list:
        listDictMetaData = []
        listFileNames = self.getFileNameList()
        for index, file_Name in enumerate(listFileNames):
            dictMetaData = {
                "titles": [],
                "identifiers": [],
                "experimental_identifier": "",
                "resource_type": "",
                "descriptions": [],
                "creators": [],
                "created_at": "",
                "updated_at": "",
                "filesets": [],
                "instruments": [],
                "experimental_methods": [],
                "specimens": [],
                "custom_properties": [],
            }
            print(self.dictExperimentInformation)
            dictMetaData["titles"].append(
                {
                    "title": self.dictExperimentInformation["dict_clipboard"][
                        "experiment"
                    ]["title"]
                }
            )
            dictMetaData["identifiers"].append(
                {"identifier": self.dictExperimentInformation["str_experiment_id"]}
            )
            dictMetaData["experimental_identifier"] = self.dictExperimentInformation[
                "str_experiment_id"
            ]
            dictMetaData["resource_type"] = "dataset"
            dictMetaData["descriptions"].append(
                {
                    "description": self.dictExperimentInformation["dict_clipboard"][
                        "experiment"
                    ]["comment"]
                }
            )

            dictMetaData["creators"] = [
                self.dictExperimentInformation["dict_user_information"]["user"]
            ]
            # created = (
            #     self.dictExperimentInformation["dict_user_information"][
            #         "experiment_date"
            #     ]["start_date"]
            #     + " "
            #     + self.dictExperimentInformation["dict_user_information"][
            #         "experiment_date"
            #     ]["start_time"]
            # )
            created = self.dictExperimentInformation["dict_user_information"]["date"][
                "start"
            ]
            dictMetaData["created_at"] = created
            current = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            dictMetaData["updated_at"] = current

            dict_File_Set = {}
            dict_File_Set["filename"] = file_Name
            dict_File_Set["description"] = self.dictExperimentInformation[
                "list_file_data"
            ][index]["experiment"]["comment"]
            dict_File_Set["status_valid"] = self.dictExperimentInformation[
                "list_file_data"
            ][index]["valid"]
            dictMetaData["filesets"].append(dict_File_Set)
            dict_Instrument = {}
            dict_Instrument["name"] = self.dictExperimentInformation[
                "dict_user_information"
            ]["instrument"]["name"]
            dict_Instrument["identifier"] = self.dictExperimentInformation[
                "dict_user_information"
            ]["instrument"]["id"]
            dict_Instrument["instrument_type"] = ""
            dict_Instrument["description"] = ""
            dictMetaData["instruments"].append(dict_Instrument)

            dict_Experiment_Method = {}
            try:
                dict_Experiment_Method["category_description"] = (
                    self.dictExperimentInformation["list_file_data"][index][
                        "equipment"
                    ]["method"]
                )
            except KeyError:
                dict_Experiment_Method["category_description"] = ""
            dict_Experiment_Method["description"] = ""
            dictMetaData["experimental_methods"].append(dict_Experiment_Method)

            dict_Specimens = {}
            dict_Specimens["name"] = self.dictExperimentInformation["list_file_data"][
                index
            ]["sample"]["name"]
            dict_Specimens["identifier"] = self.dictExperimentInformation[
                "list_file_data"
            ][index]["sample"]["id"]
            dict_Specimens["description"] = self.dictExperimentInformation[
                "list_file_data"
            ][index]["sample"]["comment"]
            dictMetaData["specimens"].append(dict_Specimens)

            if (
                len(
                    list(
                        self.dictExperimentInformation["list_file_data"][index][
                            "equipment"
                        ].keys()
                    )
                )
                > 1
            ):
                keys = list(
                    self.dictExperimentInformation["list_file_data"][index][
                        "equipment"
                    ].keys()
                )
                for i, key in enumerate(keys):
                    if i == 0:
                        continue
                    dict_Equipment_Information = {}
                    dict_Equipment_Information["name"] = key
                    dict_Equipment_Information["value"] = (
                        self.dictExperimentInformation["list_file_data"][index][
                            "equipment"
                        ][key]
                    )
                    dictMetaData["custom_properties"].append(dict_Equipment_Information)
            listDictMetaData.append(dictMetaData)
        return listDictMetaData

    def set_from_meta_data_dict(self, list_File_Name, list_Dict_Meta_Data):
        pass

    def saveInitialTemporaryFromDict(self, dict_To_Save):
        try:
            json.dump(
                dict_To_Save,
                open("temporary.json", "w", encoding="utf-8"),
                indent=4,
                ensure_ascii=False,
            )
            self.loadFromTemporary()
            self.writeToLogger("save temporary")
        except BaseException:
            self.writeToLogger("failed to save temporary")
            pass

    def setLogger(self, logger: logging.Logger) -> None:
        self._logger = logger

    def makeLogger(self, strLogConfigName: str = "", name: str = "") -> logging.Logger:
        if strLogConfigName == "":
            self._logger = logging.getLogger(__name__)
            if name != "":
                self._logger = logging.getLogger(name)
            self._logger.setLevel(logging.DEBUG)
            log_Stream_Handler = logging.StreamHandler()
            sh_formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(process)d - %(message)s",
                "%Y/%m/%d %H:%M:%S",
            )
            log_Stream_Handler.setFormatter(sh_formatter)
            self._logger.addHandler(log_Stream_Handler)
        else:
            log_config = json.load(open(strLogConfigName, mode="r"))
            logging.config.dictConfig(log_config)
            self._logger = logging.getLogger(__name__)
            if name != "":
                self._logger = logging.getLogger(name)
        return self._logger

    def writeToLogger(self, msg: str, mode: str = "debug") -> None:
        if mode == "error":
            self._logger.error(msg)
        elif mode == "warning":
            self._logger.warning(msg)
        elif mode == "critical":
            self._logger.critical(msg)
        elif mode == "info":
            self._logger.info(msg)
        else:
            self._logger.debug(msg)

    def makeHashFromString(self, string: str) -> str:
        salt = "abcd".encode("utf-8")
        hashPass = hashlib.pbkdf2_hmac("sha256", string.encode("utf-8"), salt, 100000)
        strHashPass = str(base64.standard_b64encode(hashPass).decode("utf-8"))
        return strHashPass

    def setHashPassword(self, hashPassword: str) -> None:
        self.__hashPassword = hashPassword

    def getHashPassword(self) -> str:
        return self.__hashPassword

    def setUrlBase(self, urlBase: str):
        self.dictExperimentInformation["str_url_diamond"] = urlBase
        self.messageSender.updateUrlBase(urlBase)

    def setExperimentId(self, experimentId: str):
        self.dictExperimentInformation["str_experiment_id"] = experimentId

    def getExperimentId(self) -> str:
        return self.dictExperimentInformation["str_experiment_id"]

    def setMailAddress(self, mailAddress: str):
        self.dictExperimentInformation["str_mail_address"] = mailAddress

    def getMailAddress(self) -> str:
        return self.dictExperimentInformation["str_mail_address"]

    def changeView(self, state: str):
        viewStateTemp = self.viewState
        self.viewState = state
        newWindow = self.__setView(state)
        if newWindow is None:
            self.viewState = viewStateTemp
            return False
        self.__changeViewMain(newWindow)
        return True

    def createView(self, state: str):
        newWindow = self.__setView(state)
        self.__changeViewMain(newWindow, isChange=False)
        return

    def __setView(self, state: str):
        if state == "log_in":
            newWindow = TyDialogLogin(doc=self)
        elif state == "send_one_time_password":
            newWindow = TyDialogSendOneTimePassword(doc=self)
        elif state == "register_password":
            print(self.getExperimentId())
            newWindow = TyDialogRegisterPassword(
                doc=self,
            )
        elif state == "set_initial":
            newWindow = TyDialogSetInitial(doc=self)
        elif state == "main_window":
            newWindow = TyMainWindow(doc=self)
        else:
            return None
        return newWindow

    def __changeViewMain(self, viewNext, isChange: bool = True):
        if self.currentWindow is not None and isChange:
            self.currentWindow.close()
        self.currentWindow = viewNext
        self.currentWindow.show()
        self.currentWindow.activateWindow()

    def messageBox(self, title: str, message: str, buttonNo: int = 1):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        if buttonNo == 1:
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        elif buttonNo == 2:
            msg.setStandardButtons(
                QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
            )
        else:
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        return msg.exec_()
