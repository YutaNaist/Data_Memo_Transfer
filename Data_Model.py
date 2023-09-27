import copy
import json
import os
import datetime
import logging


class DataModel_DataMemoTransfer_Exception(Exception):
    def __init__(self):
        pass


class DataModel_DataMemoTransfer_TypeException(DataModel_DataMemoTransfer_Exception):
    def __str__(self):
        return "DataModelException DataMemoTransfer: Different Type is used."


class DataModel:
    def __init__(self):
        self.dict_Data_Model = {}
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
        self.logger = logging.getLogger(__name__)
        self.initialize_data_model()

    def initialize_data_model(self):
        self.dict_Data_Model["str_url_diamond"] = "http://192.168.0.10:5462/request"
        self.dict_Data_Model["str_save_directory"] = "Z:/"
        self.dict_Data_Model["str_share_directory_in_storage"] = "C:/Share/SmartLab/"
        self.dict_Data_Model["str_experiment_id"] = ""
        self.dict_Data_Model["dict_user_information"] = {}
        self.dict_Data_Model["is_exist_temp_file"] = False
        self.dict_Data_Model["is_upload_arim"] = False
        self.dict_Data_Model["is_share_with_google"] = False
        self.dict_Data_Model["str_parent_id_in_google_drive"] = ""
        # self.dict_Data_Model["list_file_name"] = []
        self.dict_Data_Model["dict_clipboard"] = {}
        self.dict_Data_Model["list_file_data"] = []

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
        self.dict_Data_Model["dict_clipboard"] = dict_Template_Clipboard

    # Function of Template Data
    def get_All_Dict_Data_Model(self):
        return self.dict_Data_Model

    def get_Dict_Data_Model(self, key):
        try:
            return self.dict_Data_Model[key]
        except KeyError:
            return ""

    def set_Dict_Data_Model(self, key, value):
        # if isinstance(value, type(self.dict_Data_Model[key])):
        if type(value) != type(self.dict_Data_Model[key]):
            raise DataModel_DataMemoTransfer_TypeException
        self.dict_Data_Model[key] = value

    def get_Number_Of_File(self) -> int:
        return len(self.dict_Data_Model["list_file_data"])

    def save_To_Temporary(self) -> None:
        self.dict_Data_Model["is_exist_temp_file"] = True
        json.dump(
            self.dict_Data_Model,
            open("temporary.json", "w", encoding="utf-8"),
            ensure_ascii=False,
            indent=4,
        )
        self.write_to_logger("save temporary")

    def load_From_Temporary(self) -> None:
        try:
            dict_Data_Model = json.load(open("temporary.json", "r", encoding="utf-8"))
            if dict_Data_Model == {}:
                raise FileNotFoundError
            self.dict_Data_Model = dict_Data_Model
            self.dict_Data_Model["is_exist_temp_file"] = True
            self.write_to_logger("load temporary")
        except FileNotFoundError:
            self.dict_Data_Model["is_exist_temp_file"] = False
            self.write_to_logger("failed to load temporary")
        except json.decoder.JSONDecodeError:
            self.dict_Data_Model["is_exist_temp_file"] = False
            self.write_to_logger("failed to load temporary")

    def delete_Temporary(self) -> None:
        os.remove("temporary.json")
        self.dict_Data_Model["is_exist_temp_file"] = False
        self.write_to_logger("delete temporary file")

    def get_Fili_Information_Clipboard(self) -> dict:
        return copy.copy(self.dict_Data_Model["dict_clipboard"])

    def get_All_File_Information(self) -> list:
        return self.dict_Data_Model["list_file_data"]

    def get_File_Name_List(self) -> list:
        list_File_Name = []
        for dict_File_Information in self.dict_Data_Model["list_file_data"]:
            list_File_Name.append(dict_File_Information["filename"])
        return list_File_Name

    def reset_File_Data(self) -> None:
        self.dict_Data_Model["list_file_data"] = []

    def add_File_Information(self, dict_File_Information: dict) -> None:
        self.dict_Data_Model["list_file_data"].append(dict_File_Information)

    def get_File_Information(self, index: int) -> dict:
        if index == -1:
            return copy.copy(self.dict_Data_Model["dict_clipboard"])
        else:
            return self.dict_Data_Model["list_file_data"][index]

    def set_File_Information(self, index: int, dict_File_Information: dict) -> None:
        if index == -1:
            self.dict_Data_Model["dict_clipboard"] = dict_File_Information
        else:
            self.dict_Data_Model["list_file_data"][index] = dict_File_Information

    def check_Index_File_Name(self, str_File_Name: str) -> int:
        list_file_names = self.get_File_Name_List()
        if str_File_Name in list_file_names:
            return list_file_names.index(str_File_Name)
        else:
            return -1

    # meta data converter for diamond
    def get_list_dict_meta_data(self) -> list:
        list_Dict_Meta_Data = []
        list_file_names = self.get_File_Name_List()
        for index, file_Name in enumerate(list_file_names):
            dict_Meta_Data = {
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
            dict_Meta_Data["titles"].append(
                {"title": self.dict_Data_Model["dict_clipboard"]["experiment"]["title"]}
            )
            dict_Meta_Data["identifiers"].append(
                {"identifier": self.dict_Data_Model["str_experiment_id"]}
            )
            dict_Meta_Data["experimental_identifier"] = self.dict_Data_Model[
                "str_experiment_id"
            ]
            dict_Meta_Data["resource_type"] = "dataset"
            dict_Meta_Data["descriptions"].append(
                {
                    "description": self.dict_Data_Model["dict_clipboard"]["experiment"][
                        "comment"
                    ]
                }
            )

            dict_Meta_Data["creators"] = self.dict_Data_Model["dict_user_information"][
                "creators"
            ]
            created = (
                self.dict_Data_Model["dict_user_information"]["experiment_date"][
                    "start_date"
                ]
                + " "
                + self.dict_Data_Model["dict_user_information"]["experiment_date"][
                    "start_time"
                ]
            )
            dict_Meta_Data["created_at"] = created
            current = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
            dict_Meta_Data["updated_at"] = current

            dict_File_Set = {}
            dict_File_Set["filename"] = file_Name
            dict_File_Set["description"] = self.dict_Data_Model["list_file_data"][
                index
            ]["experiment"]["comment"]
            dict_File_Set["status_valid"] = self.dict_Data_Model["list_file_data"][
                index
            ]["valid"]
            dict_Meta_Data["filesets"].append(dict_File_Set)

            dict_Instrument = {}
            dict_Instrument["name"] = self.dict_Data_Model["dict_user_information"][
                "instrument"
            ]["name"]
            dict_Instrument["identifier"] = self.dict_Data_Model[
                "dict_user_information"
            ]["instrument"]["identifier"]
            dict_Instrument["instrument_type"] = ""
            dict_Instrument["description"] = ""
            dict_Meta_Data["instruments"].append(dict_Instrument)

            dict_Experiment_Method = {}
            try:
                dict_Experiment_Method["category_description"] = self.dict_Data_Model[
                    "list_file_data"
                ][index]["equipment"]["method"]
            except KeyError:
                dict_Experiment_Method["category_description"] = ""
            dict_Experiment_Method["description"] = ""
            dict_Meta_Data["experimental_methods"].append(dict_Experiment_Method)

            dict_Specimens = {}
            dict_Specimens["name"] = self.dict_Data_Model["list_file_data"][index][
                "sample"
            ]["name"]
            dict_Specimens["identifier"] = self.dict_Data_Model["list_file_data"][
                index
            ]["sample"]["id"]
            dict_Specimens["description"] = self.dict_Data_Model["list_file_data"][
                index
            ]["sample"]["comment"]
            dict_Meta_Data["specimens"].append(dict_Specimens)

            if (
                len(
                    list(
                        self.dict_Data_Model["list_file_data"][index][
                            "equipment"
                        ].keys()
                    )
                )
                > 1
            ):
                keys = list(
                    self.dict_Data_Model["list_file_data"][index]["equipment"].keys()
                )
                for i, key in enumerate(keys):
                    if i == 0:
                        continue
                    dict_Equipment_Information = {}
                    dict_Equipment_Information["name"] = key
                    dict_Equipment_Information["value"] = self.dict_Data_Model[
                        "list_file_data"
                    ][index]["equipment"][key]
                    dict_Meta_Data["custom_properties"].append(
                        dict_Equipment_Information
                    )
            list_Dict_Meta_Data.append(dict_Meta_Data)
        return list_Dict_Meta_Data

    def set_from_meta_data_dict(self, list_File_Name, list_Dict_Meta_Data):
        pass

    def save_Initial_Temporary_From_Dict(self, dict_To_Save):
        try:
            json.dump(
                dict_To_Save,
                open("temporary.json", "w", encoding="utf-8"),
                indent=4,
                ensure_ascii=False,
            )
            self.load_From_Temporary()
            self.write_to_logger("save temporary")
        except BaseException:
            self.write_to_logger("failed to save temporary")
            pass

    def set_logger(self, logger: logging.Logger) -> None:
        self.logger = logger

    def write_to_logger(self, msg: str, mode: str = "debug") -> None:
        if mode == "error":
            self.logger.error(msg)
        elif mode == "warning":
            self.logger.warning(msg)
        elif mode == "critical":
            self.logger.critical(msg)
        elif mode == "info":
            self.logger.info(msg)
        else:
            self.logger.debug(msg)
