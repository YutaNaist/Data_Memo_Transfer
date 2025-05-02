import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import logging
from TyMessageSender import TyMessageSender
from TyDocDataMemoTransfer import TyDocDataMemoTransfer

SHARE_DIRECTORY_IN_STORAGE = r"C:\Project\DataDiamondTest\Share\NR-000"
URL_DIAMOND = "https://localhost:6426"
SAVE_DIRECTORY = r"C:\Project\DataDiamondTest\Share\NR-000"
doc = TyDocDataMemoTransfer()
doc.setIsBuild(False)
logger = logging.getLogger("data_memo_transfer_debug")
logger.setLevel(logging.DEBUG)


def test_sendLoginCase1():
    print("--------------------LOG IN--------------------")
    doc.setUrlBase(URL_DIAMOND)
    doc.setDiCtExperimentInformation("str_save_directory", SAVE_DIRECTORY)
    doc.setDiCtExperimentInformation(
        "str_share_directory_in_storage", SHARE_DIRECTORY_IN_STORAGE
    )
    messageSender = TyMessageSender(URL_DIAMOND, doc)

    print(
        "--------------------Case 1: Correct experiment id and password--------------------"
    )
    strExperimentId = "0000-0000-0000"
    # rowPass = "password"
    # hashPass = doc.makeHashFromString(rowPass)
    hashPass = "BILRGNtGU4Frmfw3qpOAikpkmjLdxr1mySkykz+H4Jw="
    doc.setUrlBase(URL_DIAMOND)
    doc.setDiCtExperimentInformation("str_save_directory", SAVE_DIRECTORY)
    doc.setDiCtExperimentInformation(
        "str_share_directory_in_storage", SHARE_DIRECTORY_IN_STORAGE
    )
    messageSender = TyMessageSender(URL_DIAMOND, doc)
    # sendURL = URL_DIAMOND + f"/login/{strExperimentId}"
    # logger.info(f"sendURL: {sendURL}")
    response = messageSender.sendRequestLogin(strExperimentId, hashPass)
    logger.info(f"responce: {response}")
    assert (response["status_code"] == 200) and (
        response["status"] is True
    ), "Failed to send check experiment ID request Case 1"
    print(
        "--------------------------------------------------------------------------------"
    )


def test_sendLoginCase2():
    print("--------------------LOG IN--------------------")
    doc.setUrlBase(URL_DIAMOND)
    doc.setDiCtExperimentInformation("str_save_directory", SAVE_DIRECTORY)
    doc.setDiCtExperimentInformation(
        "str_share_directory_in_storage", SHARE_DIRECTORY_IN_STORAGE
    )
    messageSender = TyMessageSender(URL_DIAMOND, doc)

    print(
        "--------------------Case 2: Correct experiment id and wrong password--------------------"
    )
    strExperimentId = "0000-0000-0000"
    # rowPass = "wrong_password"
    # hashPass = doc.makeHashFromString(rowPass)
    hashPass = "BILRGNtGU4Frmfw3qpOAiaaaaaaaaaaaaaaaaaaaaaaa"
    # sendURL = URL_DIAMOND + f"/request_one_time_password/{strExperimentId}"
    response = messageSender.sendRequestLogin(strExperimentId, hashPass)
    logger.info(f"responce: {response}")
    assert (response["status_code"] == 401) and (
        response["status"] is False
    ), "Failed to send check experiment ID request Case 2"
    print(
        "--------------------------------------------------------------------------------"
    )


def test_sendLoginCase3():
    print("--------------------LOG IN--------------------")
    doc.setUrlBase(URL_DIAMOND)
    doc.setDiCtExperimentInformation("str_save_directory", SAVE_DIRECTORY)
    doc.setDiCtExperimentInformation(
        "str_share_directory_in_storage", SHARE_DIRECTORY_IN_STORAGE
    )
    messageSender = TyMessageSender(URL_DIAMOND, doc)

    print("--------------------Case 3: Wrong experiment id--------------------")
    strExperimentId = "0014-0000-0000"
    # rowPass = "password"
    # hashPass = doc.makeHashFromString(rowPass)
    hashPass = "BILRGNtGU4Frmfw3qpOAikpkmjLdxr1mySkykz+H4Jw="
    # sendURL = URL_DIAMOND + f"/request_one_time_password/{strExperimentId}"
    response = messageSender.sendRequestLogin(strExperimentId, hashPass)
    logger.info(f"responce: {response}")
    assert (response["status_code"] == 404) and (
        response["status"] is False
    ), "Failed to send check experiment ID request Case 3"
    print(
        "--------------------------------------------------------------------------------"
    )


if __name__ == "__main__":
    test_sendLoginCase1()
    test_sendLoginCase2()
    test_sendLoginCase3()
