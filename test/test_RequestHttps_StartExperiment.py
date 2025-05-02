import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import logging
from TyMessageSender import TyMessageSender
from TyDocDataMemoTransfer import TyDocDataMemoTransfer

SHARE_DIRECTORY_IN_STORAGE = r"C:\Project\DataDiamond\Share\NR-000"
URL_DIAMOND = "https://localhost:6426"
SAVE_DIRECTORY = r"C:\Project\DataDiamond\Share\NR-000"
doc = TyDocDataMemoTransfer()
doc.setIsBuild(False)
logger = logging.getLogger("data_memo_transfer_debug")
logger.setLevel(logging.DEBUG)
isDebug = True


def test_startExperimentCase1():
    print("--------------------Start Experiment--------------------")
    doc.setUrlBase(URL_DIAMOND)
    doc.setDiCtExperimentInformation("str_save_directory", SAVE_DIRECTORY)
    doc.setDiCtExperimentInformation(
        "str_share_directory_in_storage", SHARE_DIRECTORY_IN_STORAGE
    )
    messageSender = TyMessageSender(URL_DIAMOND, doc)

    print(
        "--------------------Case 1: Start experiment correct experiment ID--------------------"
    )
    strExperimentId = "0000-0000-0000"
    # rowPass = "password"
    # hashPass = doc.makeHashFromString(rowPass)
    hashPass = "BILRGNtGU4Frmfw3qpOAikpkmjLdxr1mySkykz+H4Jw="
    response = messageSender.sendRequestLogin(strExperimentId, hashPass)
    response = messageSender.sendRequestStartExperiment(strExperimentId, doc)
    logger.info(f"responce: {response}")
    assert (response["status_code"] == 200) and (
        response["status"] is True
    ), "Failed to send start experiment ID request Case 1"
    response = messageSender.sendRequestLogout(strExperimentId)
    print(
        "--------------------------------------------------------------------------------"
    )


def test_startExperimentCase2():
    print("--------------------Start Experiment--------------------")
    doc.setUrlBase(URL_DIAMOND)
    doc.setDiCtExperimentInformation("str_save_directory", SAVE_DIRECTORY)
    doc.setDiCtExperimentInformation(
        "str_share_directory_in_storage", SHARE_DIRECTORY_IN_STORAGE
    )
    messageSender = TyMessageSender(URL_DIAMOND, doc)

    print(
        "--------------------Case 2: Start experiment without login: --------------------"
    )
    strExperimentId = "0000-0000-0000"
    response = messageSender.sendRequestStartExperiment(strExperimentId, doc)
    logger.info(f"responce: {response}")
    assert (response["status_code"] == 401) and (
        response["status"] is False
    ), "Failed to send start experiment ID request Case 2"
    print(
        "--------------------------------------------------------------------------------"
    )
    # response = messageSender.sendRequestLogout(strExperimentId)


def test_startExperimentCase3():
    print("--------------------Start Experiment--------------------")
    doc.setUrlBase(URL_DIAMOND)
    doc.setDiCtExperimentInformation("str_save_directory", SAVE_DIRECTORY)
    SHARE_DIRECTORY_IN_STORAGE = r"C:\Project\DataDiamond-2\Share\NR-000"
    doc.setDiCtExperimentInformation(
        "str_share_directory_in_storage", SHARE_DIRECTORY_IN_STORAGE
    )
    messageSender = TyMessageSender(URL_DIAMOND, doc)

    print("--------------------Case 3: Not found share directory--------------------")
    strExperimentId = "0000-0000-0000"
    # rowPass = "password"
    # hashPass = doc.makeHashFromString(rowPass)
    hashPass = "BILRGNtGU4Frmfw3qpOAikpkmjLdxr1mySkykz+H4Jw="
    response = messageSender.sendRequestLogin(strExperimentId, hashPass)
    response = messageSender.sendRequestStartExperiment(strExperimentId, doc)
    logger.info(f"responce: {response}")
    assert (response["status_code"] == 500) and (
        response["status"] is False
    ), "Failed to send start experiment ID request Case 3"
    response = messageSender.sendRequestLogout(strExperimentId)
    print(
        "--------------------------------------------------------------------------------"
    )


def test_startExperimentCase4():
    print("--------------------Start Experiment--------------------")
    doc.setUrlBase(URL_DIAMOND)
    doc.setDiCtExperimentInformation("str_save_directory", SAVE_DIRECTORY)
    doc.setDiCtExperimentInformation(
        "str_share_directory_in_storage", SHARE_DIRECTORY_IN_STORAGE
    )
    messageSender = TyMessageSender(URL_DIAMOND, doc)

    print(
        "--------------------Case 4: experiment id is changed after login--------------------"
    )
    strExperimentId = "0000-0000-0000"
    # rowPass = "password"
    # hashPass = doc.makeHashFromString(rowPass)
    hashPass = "BILRGNtGU4Frmfw3qpOAikpkmjLdxr1mySkykz+H4Jw="
    response = messageSender.sendRequestLogin(strExperimentId, hashPass)
    strExperimentId = "0013-0000-0000"
    response = messageSender.sendRequestStartExperiment(strExperimentId, doc)
    logger.info(f"responce: {response}")
    assert (response["status_code"] == 401) and (
        response["status"] is False
    ), "Failed to send start experiment ID request Case 4"
    response = messageSender.sendRequestLogout(strExperimentId)
    print(
        "--------------------------------------------------------------------------------"
    )


if __name__ == "__main__":
    test_startExperimentCase1()
    test_startExperimentCase2()
    test_startExperimentCase3()
    test_startExperimentCase4()
