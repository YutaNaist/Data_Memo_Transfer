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
isDebug = True


def test_registerPasswordCase1():
    print("--------------------Register password--------------------")
    doc.setUrlBase(URL_DIAMOND)
    doc.setDiCtExperimentInformation("str_save_directory", SAVE_DIRECTORY)
    doc.setDiCtExperimentInformation(
        "str_share_directory_in_storage", SHARE_DIRECTORY_IN_STORAGE
    )
    messageSender = TyMessageSender(URL_DIAMOND, doc)

    print(
        "--------------------Case 1: Correct experiment Id and OTP--------------------"
    )
    strExperimentId = "0000-0000-0000"
    sendURL = URL_DIAMOND + f"/request_one_time_password/{strExperimentId}"
    logger.info(f"sendURL: {sendURL}")
    response = messageSender.sendRequestSendOneTimePassword(
        strExperimentId, False, isDebug
    )
    oneTimePassword = response["one_time_password"]
    logger.info(f"responce: {response}")

    # rowPass = "password"
    # hashPass = doc.makeHashFromString(rowPass)
    hashPass = "BILRGNtGU4Frmfw3qpOAikpkmjLdxr1mySkykz+H4Jw="
    response = messageSender.sendRequestRegisterPassword(
        strExperimentId, hashPass, oneTimePassword
    )

    assert (response["status_code"] == 200) and (
        response["status"] is True
    ), "Failed to send check experiment ID request Case 1"
    print(
        "--------------------------------------------------------------------------------"
    )


def test_registerPasswordCase2():
    print("--------------------Register password--------------------")
    doc.setUrlBase(URL_DIAMOND)
    doc.setDiCtExperimentInformation("str_save_directory", SAVE_DIRECTORY)
    doc.setDiCtExperimentInformation(
        "str_share_directory_in_storage", SHARE_DIRECTORY_IN_STORAGE
    )
    messageSender = TyMessageSender(URL_DIAMOND, doc)

    print("--------------------Case 2: Wrong one time password--------------------")
    strExperimentId = "0000-0000-0000"
    sendURL = URL_DIAMOND + f"/request_one_time_password/{strExperimentId}"
    logger.info(f"sendURL: {sendURL}")
    response = messageSender.sendRequestSendOneTimePassword(
        strExperimentId, False, isDebug
    )
    # oneTimePassword = response["one_time_password"]
    oneTimePassword = "0000"
    logger.info(f"responce: {response}")

    # rowPass = "password"
    # hashPass = doc.makeHashFromString(rowPass)
    hashPass = "BILRGNtGU4Frmfw3qpOAikpkmjLdxr1mySkykz+H4Jw="
    response = messageSender.sendRequestRegisterPassword(
        strExperimentId, hashPass, oneTimePassword
    )

    assert (response["status_code"] == 401) and (
        response["status"] is False
    ), "Failed to send check experiment ID request Case 2"
    print(
        "--------------------------------------------------------------------------------"
    )


def test_registerPasswordCase3():
    print("--------------------Register password--------------------")
    doc.setUrlBase(URL_DIAMOND)
    doc.setDiCtExperimentInformation("str_save_directory", SAVE_DIRECTORY)
    doc.setDiCtExperimentInformation(
        "str_share_directory_in_storage", SHARE_DIRECTORY_IN_STORAGE
    )
    messageSender = TyMessageSender(URL_DIAMOND, doc)

    print("--------------------Case 3: Different experiment id--------------------")
    strExperimentId = "0000-0000-0000"
    sendURL = URL_DIAMOND + f"/request_one_time_password/{strExperimentId}"
    logger.info(f"sendURL: {sendURL}")
    response = messageSender.sendRequestSendOneTimePassword(
        strExperimentId, False, isDebug
    )
    # oneTimePassword = response["one_time_password"]
    strExperimentId = "0013-0000-0000"
    oneTimePassword = "0000"
    logger.info(f"responce: {response}")

    # rowPass = "password"
    # hashPass = doc.makeHashFromString(rowPass)
    hashPass = "BILRGNtGU4Frmfw3qpOAikpkmjLdxr1mySkykz+H4Jw="
    response = messageSender.sendRequestRegisterPassword(
        strExperimentId, hashPass, oneTimePassword
    )

    assert (response["status_code"] == 401) and (
        response["status"] is False
    ), "Failed to send check experiment ID request Case 3"
    print(
        "--------------------------------------------------------------------------------"
    )


def test_registerPasswordCase4():
    print("--------------------Register password--------------------")
    doc.setUrlBase(URL_DIAMOND)
    doc.setDiCtExperimentInformation("str_save_directory", SAVE_DIRECTORY)
    doc.setDiCtExperimentInformation(
        "str_share_directory_in_storage", SHARE_DIRECTORY_IN_STORAGE
    )
    messageSender = TyMessageSender(URL_DIAMOND, doc)

    print(
        "--------------------Case 4: One time password is not issued--------------------"
    )
    strExperimentId = "0000-0000-0000"
    oneTimePassword = "0000"
    # rowPass = "password"
    # hashPass = doc.makeHashFromString(rowPass)
    hashPass = "BILRGNtGU4Frmfw3qpOAikpkmjLdxr1mySkykz+H4Jw="
    response = messageSender.sendRequestRegisterPassword(
        strExperimentId, hashPass, oneTimePassword
    )

    assert (response["status_code"] == 401) and (
        response["status"] is False
    ), "Failed to send check experiment ID request Case 4"
    print(
        "--------------------------------------------------------------------------------"
    )


if __name__ == "__main__":
    test_registerPasswordCase1()
    test_registerPasswordCase2()
    test_registerPasswordCase3()
    test_registerPasswordCase4()
