import copy
import json
import os
import datetime


class DataModel:
    def __init__(self):
        self.str_Diamond_URL = "http://192.168.0.10:5462/request"
        self.str_Share_Directory = "Z:/"
        self.str_Share_Directory_In_Storage = "C:/Share/SmartLab/"
        self.str_Experiment_ID = ""
        self.dict_User_Information = {}
        self.is_exist_Temp_File = False

        self.dict_Template_Data = {}
        self.list_file_names = []
        self.list_Dict_Files_Data = []

        self.list_keys_Template_Data = [
            "title", "experiment_comment", "sample_id", "sample_name",
            "sample_comment", "equipment_contents"
        ]
        self.list_keys_File_Data = [
            "file_name", "file_index", "file_status_classified",
            "file_is_valid", "file_comment", "file_sample_id",
            "file_sample_name", "file_sample_comment",
            "file_equipment_contents"
        ]
        for key in self.list_keys_Template_Data:
            if key == "equipment_contents":
                self.dict_Template_Data[key] = {"experiment_method": ""}
            else:
                self.dict_Template_Data[key] = ""

        self.list_Dict_Files_Data_Template = {}
        for key in self.list_keys_File_Data:
            if key == "file_equipment_contents":
                self.list_Dict_Files_Data_Template[key] = {
                    "experiment_method": ""
                }
            elif key == "file_status_classified":
                self.list_Dict_Files_Data_Template[key] = "not_classified"
            elif key == "file_index":
                self.list_Dict_Files_Data_Template[key] = 0
            else:
                self.list_Dict_Files_Data_Template[key] = ""

    # Function of Template Data
    def set_User_Information(self, dict_User_Information):
        self.dict_User_Information = dict_User_Information

    def set_Template_Data(self, dict_Template_Data):
        self.dict_Template_Data = dict_Template_Data

    def set_URL_Address_Diamond(self, str_URL):
        self.str_Diamond_URL = str_URL

    def get_URL_Address_Diamond(self):
        return self.str_Diamond_URL

    def set_Share_Directory(self, str_Share_Directory):
        self.str_Share_Directory = str_Share_Directory

    def get_Share_Directory(self):
        return self.str_Share_Directory

    def set_Share_Directory_In_Storage(self, str_Share_Directory_In_Storage):
        self.str_Share_Directory_In_Storage = str_Share_Directory_In_Storage

    def get_Share_Directory_In_Storage(self):
        return self.str_Share_Directory_In_Storage

    def set_Experiment_ID(self, str_Experiment_ID):
        self.str_Experiment_ID = str_Experiment_ID

    def get_Experiment_ID(self):
        return self.str_Experiment_ID

    def set_All_Template_Data(self, dict_Template_Data):
        self.dict_Template_Data = dict_Template_Data

    def get_All_Template_Data(self):
        return self.dict_Template_Data

    def set_Template_Data_By_Key(self, str_Key, str_Value):
        self.dict_Template_Data[str_Key] = str_Value

    def get_Template_Data_By_Key(self, str_Key):
        return self.dict_Template_Data[str_Key]

    def set_Equipment_Contents(self, str_Key, str_Equipment_Contents):
        self.dict_Template_Data["equipment_contents"][
            str_Key] = str_Equipment_Contents

    def get_Equipment_Contents(self, str_Key):
        return self.dict_Template_Data["equipment_contents"][str_Key]

    def get_Equipment_Contents_Keys(self):
        return self.dict_Template_Data["equipment_contents"].keys()

    # Saving Temporary Data
    def save_To_Temporary(self):
        dict_To_Save = {}
        # dict_To_Save["url_diamond"] = self.str_Diamond_URL
        dict_To_Save["share_directory"] = self.str_Share_Directory
        dict_To_Save["file_names"] = self.list_file_names
        dict_To_Save["experiment_id"] = self.str_Experiment_ID
        dict_To_Save["template_data"] = self.dict_Template_Data
        dict_To_Save["file_data"] = self.list_Dict_Files_Data
        json.dump(dict_To_Save,
                  open("temporary.json", "w", encoding="utf-8"),
                  indent=4,
                  ensure_ascii=False)

    def load_From_Temporary(self):
        try:
            dict_Load = json.load(open("temporary.json", "r",
                                       encoding="utf-8"))
            # self.str_Diamond_URL = dict_Load["url_diamond"]
            self.str_Share_Directory = dict_Load["share_directory"]
            self.list_file_names = dict_Load["file_names"]
            self.dict_Template_Data = dict_Load["template_data"]
            self.list_Dict_Files_Data = dict_Load["file_data"]
            self.is_exist_Temp_File = True
        except FileNotFoundError:
            pass
        except json.decoder.JSONDecodeError:
            pass
        except KeyError:
            pass

    def remove_Temporary(self):
        try:
            os.remove("temporary.json")
        except FileNotFoundError:
            pass

    # Function File Data
    def set_File_Names(self, list_File_Names):
        self.list_file_names = list_File_Names

    def get_File_Names(self):
        return self.list_file_names

    def get_File_Data_Template(self):
        return self.list_Dict_Files_Data_Template

    def set_File_Data(self, str_File_Name, dict_File_Data):
        index = self.check_Index_File_Name(str_File_Name)
        if index == -1:
            self.list_file_names.append(str_File_Name)
            self.list_Dict_Files_Data.append(
                copy.deepcopy(self.list_Dict_Files_Data_Template))
        for key in dict_File_Data.keys():
            self.list_Dict_Files_Data[index][key] = dict_File_Data[key]

    def append_File_Data_Without_Check(self, str_File_Name, dict_File_Data):
        self.list_file_names.append(str_File_Name)
        self.list_Dict_Files_Data.append(
            copy.deepcopy(self.list_Dict_Files_Data_Template))
        for key in dict_File_Data.keys():
            self.list_Dict_Files_Data[-1][key] = dict_File_Data[key]

    def set_File_Data_By_Index(self, index, dict_File_Data):
        for key in dict_File_Data.keys():
            self.list_Dict_Files_Data[index][key] = dict_File_Data[key]

    def set_File_Data_By_Key(self, str_File_Name, str_Key, str_Value):
        index = self.check_Index_File_Name(str_File_Name)
        if index == -1:
            self.list_file_names.append(str_File_Name)
            self.list_Dict_Files_Data.append(
                copy.deepcopy(self.list_Dict_Files_Data_Template))
        self.list_Dict_Files_Data[index][str_Key] = str_Value

    def set_File_Data_By_Index_And_Key(self, index, str_Key, str_Value):
        self.list_Dict_Files_Data[index][str_Key] = str_Value

    def get_File_Data(self, str_File_Name):
        index = self.check_Index_File_Name(str_File_Name)
        if index == -1:
            return {}
        else:
            return self.list_Dict_Files_Data[index]

    def get_File_Data_By_Index(self, int_Index):
        return self.list_Dict_Files_Data[int_Index]

    def get_File_Data_By_Key(self, str_File_Name, str_Key):
        index = self.check_Index_File_Name(str_File_Name)
        if index == -1:
            return {}
        else:
            return self.list_Dict_Files_Data[index][str_Key]

    def get_File_Data_By_Index_And_Key(self, int_Index, str_Key):
        return self.list_Dict_Files_Data[int_Index][str_Key]

    def set_All_File_Data(self, list_Dict_Files_Data):
        self.list_Dict_Files_Data = list_Dict_Files_Data

    def get_All_File_Data(self):
        return self.list_Dict_Files_Data

    def set_File_Data_Equipment_Contents(self, str_File_Name, str_Key,
                                         str_Equipment_Contents):
        index = self.check_Index_File_Name(str_File_Name)
        if index == -1:
            pass
        else:
            self.list_Dict_Files_Data[index]["file_equipment_contents"][
                str_Key] = str_Equipment_Contents

    def get_File_Data_Equipment_Contents(self, str_File_Name, str_Key):
        index = self.check_Index_File_Name(str_File_Name)
        if index == -1:
            return {}
        else:
            return self.list_Dict_Files_Data[index]["file_equipment_contents"][
                str_Key]

    def set_File_Data_Equipment_Contents_By_Index(self, int_index, str_Key,
                                                  str_Equipment_Contents):
        self.list_Dict_Files_Data[int_index]["file_equipment_contents"][
            str_Key] = str_Equipment_Contents

    def get_File_Data_Equipment_Contents_By_Index(self, int_index, str_Key):
        return self.list_Dict_Files_Data[int_index]["file_equipment_contents"][
            str_Key]

    def get_File_Data_Equipment_Contents_Keys(self, str_File_Name):
        index = self.check_Index_File_Name(str_File_Name)
        if index == -1:
            return []
        else:
            return self.list_Dict_Files_Data[index][
                "file_equipment_contents"].keys()

    def get_File_Data_Equipment_Contents_Keys_By_Index(self, int_index):
        return self.list_Dict_Files_Data[int_index][
            "file_equipment_contents"].keys()

    def reset_File_Data(self):
        self.list_file_names = []
        self.list_Dict_Files_Data = []

    def check_Index_File_Name(self, str_File_Name):
        if str_File_Name in self.list_file_names:
            return self.list_file_names.index(str_File_Name)
        else:
            return -1

    # Basic Setter and Getter
    def set_Title(self, str_Title):
        self.dict_Template_Data["title"] = str_Title

    def get_Title(self):
        return self.dict_Template_Data["title"]

    def set_experiment_comment(self, str_experiment_comment):
        self.dict_Template_Data["experiment_comment"] = str_experiment_comment

    def get_experiment_comment(self):
        return self.dict_Template_Data["experiment_comment"]

    def set_sample_id(self, str_sample_id):
        self.dict_Template_Data["sample_id"] = str_sample_id

    def get_sample_id(self):
        return self.dict_Template_Data["sample_id"]

    def set_sample_name(self, str_sample_name):
        self.dict_Template_Data["sample_name"] = str_sample_name

    def get_sample_name(self):
        return self.dict_Template_Data["sample_name"]

    def set_sample_comment(self, str_sample_comment):
        self.dict_Template_Data["sample_comment"] = str_sample_comment

    def get_sample_comment(self):
        return self.dict_Template_Data["sample_comment"]

    # meta data converter for diamond
    def get_list_dict_meta_data(self):
        list_Dict_Meta_Data = []
        for index, file_Name in enumerate(self.list_file_names):
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
                "custom_properties": []
            }
            dict_Meta_Data["titles"].append(
                {"title": self.dict_Template_Data["title"]})
            dict_Meta_Data["identifiers"].append(
                {"identifier": self.str_Experiment_ID})
            dict_Meta_Data["experimental_identifier"] = self.str_Experiment_ID
            dict_Meta_Data["resource_type"] = "dataset"
            dict_Meta_Data["descriptions"].append(
                {"description": self.dict_Template_Data["experiment_comment"]})

            dict_Meta_Data["creators"] = self.dict_User_Information["creators"]
            created = self.dict_User_Information["experiment_date"][
                "start_date"] + " " + self.dict_User_Information[
                    "experiment_date"]["start_time"]
            dict_Meta_Data["created_at"] = created
            current = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
            dict_Meta_Data["updated_at"] = current

            dict_File_Set = {}
            dict_File_Set["filename"] = file_Name
            dict_File_Set["description"] = self.list_Dict_Files_Data[index][
                "file_comment"]
            dict_File_Set["status_valid"] = self.list_Dict_Files_Data[index][
                "file_is_valid"]
            dict_Meta_Data["filesets"].append(dict_File_Set)

            dict_Instrument = {}
            dict_Instrument["name"] = self.dict_User_Information["instrument"][
                "name"]
            dict_Instrument["identifier"] = self.dict_User_Information[
                "instrument"]["identifier"]
            dict_Instrument["instrument_type"] = ""
            dict_Instrument["description"] = ""
            dict_Meta_Data["instruments"].append(dict_Instrument)

            dict_Experiment_Method = {}
            dict_Experiment_Method[
                "category_description"] = self.list_Dict_Files_Data[index][
                    "file_equipment_contents"]["experiment_method"]
            dict_Experiment_Method["description"] = ""
            dict_Meta_Data["experimental_methods"].append(
                dict_Experiment_Method)

            dict_Specimens = {}
            dict_Specimens["name"] = self.list_Dict_Files_Data[index][
                "file_sample_name"]
            dict_Specimens["identifier"] = self.list_Dict_Files_Data[index][
                "file_sample_id"]
            dict_Specimens["description"] = self.list_Dict_Files_Data[index][
                "file_sample_comment"]
            dict_Meta_Data["specimens"].append(dict_Specimens)

            if len(self.list_Dict_Files_Data[index]
                   ["file_equipment_contents"]) > 1:
                keys = self.list_Dict_Files_Data[index][
                    "file_equipment_contents"].keys()
                for i in range(
                        len(self.list_Dict_Files_Data[index]
                            ["file_equipment_contents"] - 1)):
                    dict_Equipment_Information = {}
                    dict_Equipment_Information["name"] = keys[i + 1]
                    dict_Equipment_Information[
                        "value"] = self.list_Dict_Files_Data[index][
                            "file_equipment_contents"][keys[i + 1]]
                    dict_Meta_Data["custom_properties"].append(
                        dict_Equipment_Information)
            list_Dict_Meta_Data.append(dict_Meta_Data)
        return list_Dict_Meta_Data

    def set_from_meta_data_dict(self, list_File_Name, list_Dict_Meta_Data):
        pass

    def get_All_Data_To_Save(self):
        dict_To_Save = {}
        # dict_To_Save["url_diamond"] = self.str_Diamond_URL
        dict_To_Save["share_directory"] = self.str_Share_Directory
        dict_To_Save["file_names"] = self.list_file_names
        dict_To_Save["experiment_id"] = self.str_Experiment_ID
        dict_To_Save["template_data"] = self.dict_Template_Data
        dict_To_Save["file_data"] = self.list_Dict_Files_Data
        return dict_To_Save

    def save_Initial_Temporary_From_Dict(self, dict_To_Save):
        try:
            # dict_To_Save["share_directory"] = self.str_Share_Directory
            # dict_To_Save["file_names"] = self.list_file_names
            # dict_To_Save["experiment_id"] = self.str_Experiment_ID
            # dict_To_Save["template_data"] = self.dict_Template_Data
            # dict_To_Save["file_data"] = self.list_Dict_Files_Data
            json.dump(dict_To_Save,
                      open("temporary.json", "w", encoding="utf-8"),
                      indent=4,
                      ensure_ascii=False)
            self.load_From_Temporary()
        except BaseException:
            pass
