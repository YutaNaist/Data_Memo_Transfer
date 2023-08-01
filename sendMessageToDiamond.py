import requests
import json
import random

from Data_Model import DataModel


class senderMessageToDiamond:

    def __init__(self, url):
        self._url = url
        self.data_Model = DataModel()
        self.commandList = [
            'Check_UsageID', 'Finish_Experiment',
            'read_Use_Information_From_Shared_Excel',
            'Check_And_Get_Single_Proposal', 'Get_Meta_Data',
            'Copy_From_Original_To_Share', 'Start_Experiment'
        ]
        pass

    def sendMessage(self, command: str, args: dict) -> dict:
        try:
            identifier = int(random.random() * 1000000000)
            json_data = json.dumps({
                "command": command,
                "args": args,
                "identifier": identifier
            })
            headers = {'Content-type': 'application/json'}
            response = requests.post(self._url,
                                     data=json_data,
                                     headers=headers)

            statusCode = response.status_code
            if statusCode == 500:
                return {
                    "status":
                    False,
                    "message":
                    "Internal Server Error. Please contact the administrator."
                }

            dictReturnResponse = json.loads(response.text)
            returnIdentifier = dictReturnResponse["identifier"]
            if identifier != returnIdentifier:
                print("Resend Message")
                dictReturnResponse = self.sendMessage(command, args)

        except requests.exceptions.ConnectTimeout:
            return {
                "status":
                False,
                "message":
                "TimeoutError: Failed to connect Server. Please contact to the administrator"
            }
        except requests.exceptions.ConnectionError:
            return {
                "status":
                False,
                "message":
                "ConnectionError Failed to connect Server. Please contact to the administrator."
            }
        return dictReturnResponse

    def sendRequestCheckID(self, str_Experiment_ID: str) -> dict:
        args = {"experiment_id": str_Experiment_ID}
        dictResponse = self.sendMessage(self.commandList[0], args)
        return dictResponse

    def sendRequestFinishExperiment(self,
                                    data_Model: DataModel,
                                    isAppendExisting: bool = False) -> dict:
        self.data_Model = data_Model
        args = {}
        args["experiment_id"] = self.data_Model.get_Dict_Data_Model(
            "str_experiment_id")
        args["storagePCShareDirectory"] = self.data_Model.get_Dict_Data_Model(
            "str_share_directory_in_storage")
        args["isAppendExisting"] = isAppendExisting
        args["file_names"] = self.data_Model.get_File_Name_List()
        args["meta_data"] = self.data_Model.get_list_dict_meta_data()
        args[
            "experiment_information"] = self.data_Model.get_All_Dict_Data_Model(
            )
        print(args)
        dictResponse = self.sendMessage(self.commandList[1], args)
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

    def sendRequestCopyOriginal(self, str_Experiment_ID: str,
                                data_Model: DataModel) -> dict:
        self.data_Model = data_Model
        args = {}
        args["experiment_id"] = str_Experiment_ID
        args[
            "storagePC_share_directory"] = self.data_Model.get_Dict_Data_Model(
                "str_share_directory_in_storage")
        dictResponse = self.sendMessage(self.commandList[5], args)
        return dictResponse

    def sendRequestStartExperiment(self, str_Experiment_ID: str) -> dict:
        args = {}
        args["experiment_id"] = str_Experiment_ID
        dictResponse = self.sendMessage(self.commandList[6], args)
        return dictResponse
