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


def test_requestOneTimePasswordCase1():
    print("--------------------Request One Time Password--------------------")
    doc.setUrlBase(URL_DIAMOND)
    doc.setDiCtExperimentInformation("str_save_directory", SAVE_DIRECTORY)
    doc.setDiCtExperimentInformation(
        "str_share_directory_in_storage", SHARE_DIRECTORY_IN_STORAGE
    )
    messageSender = TyMessageSender(URL_DIAMOND, doc)

    print("--------------------Case 1: Correct experiment Id--------------------")
    strExperimentId = "0000-0000-0000"
    sendURL = URL_DIAMOND + f"/request_one_time_password/{strExperimentId}"
    logger.info(f"sendURL: {sendURL}")
    # dataJson = {
    #     "is_send_to_supervisor": False,
    #     "is_debug": True,
    # }
    # response = messageSender.sendMessage(sendURL, dataJson, "POST")
    response = messageSender.sendRequestSendOneTimePassword(strExperimentId, False, isDebug)
    logger.info(f"responce: {response}")
    assert (response["status_code"] == 200) and (
        response["status"] is True
    ), "Failed to send check experiment ID request Case 1"
    print(
        "--------------------------------------------------------------------------------"
    )


def test_requestOneTimePasswordCase2():
    print("--------------------Request One Time Password--------------------")
    doc.setUrlBase(URL_DIAMOND)
    doc.setDiCtExperimentInformation("str_save_directory", SAVE_DIRECTORY)
    doc.setDiCtExperimentInformation(
        "str_share_directory_in_storage", SHARE_DIRECTORY_IN_STORAGE
    )
    messageSender = TyMessageSender(URL_DIAMOND, doc)

    print("--------------------Case 2: Inorrect experiment Id--------------------")
    strExperimentId = "0013-0000-0000"
    sendURL = URL_DIAMOND + f"/request_one_time_password/{strExperimentId}"
    logger.info(f"sendURL: {sendURL}")
    response = messageSender.sendRequestSendOneTimePassword(strExperimentId, False, isDebug)
    # response = messageSender.sendMessage(sendURL, dataJson, "POST")
    logger.info(f"responce: {response}")
    assert (response["status_code"] == 404) and (
        response["status"] is False
    ), "Failed to send check experiment ID request Case 2"
    print(
        "--------------------------------------------------------------------------------"
    )


if __name__ == "__main__":
    test_requestOneTimePasswordCase1()
    test_requestOneTimePasswordCase2()
