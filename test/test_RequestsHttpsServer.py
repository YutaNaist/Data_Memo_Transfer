import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import requests
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


def test_sendCheckExperimentId():
    # Test case for sending a check experiment ID request
    doc.setUrlBase(URL_DIAMOND)
    doc.setDiCtExperimentInformation("str_save_directory", SAVE_DIRECTORY)
    doc.setDiCtExperimentInformation(
        "str_share_directory_in_storage", SHARE_DIRECTORY_IN_STORAGE
    )
    messageSender = TyMessageSender(URL_DIAMOND, doc)

    strExperimentId = "0000-0000-0000"
    sendURL = URL_DIAMOND + f"/experiment_id/{strExperimentId}"
    logger.info(f"sendURL: {sendURL}")
    response = messageSender.sendMessage(sendURL, {}, "GET")
    logger.info(f"responce: {response}")
    assert (response["status_code"] == 200) and (
        response["status"] is True
    ), "Failed to send check experiment ID request"

    messageSender = TyMessageSender(URL_DIAMOND, doc)

    strExperimentId = "0013-0000-0000"
    sendURL = URL_DIAMOND + f"/experiment_id/{strExperimentId}"
    logger.info(f"sendURL: {sendURL}")
    response = messageSender.sendMessage(sendURL, {}, "GET")
    logger.info(f"responce: {response}")
    assert (response["status_code"] == 404) and (
        response["status"] is False
    ), "Failed to send check experiment ID request"


def test_sendLogin():
    doc.setUrlBase(URL_DIAMOND)
    doc.setDiCtExperimentInformation("str_save_directory", SAVE_DIRECTORY)
    doc.setDiCtExperimentInformation(
        "str_share_directory_in_storage", SHARE_DIRECTORY_IN_STORAGE
    )
    messageSender = TyMessageSender(URL_DIAMOND, doc)

    strExperimentId = "0000-0000-0000"
    rowPass = "password"
    hashPass = doc.makeHashFromString(rowPass)

    doc.setUrlBase(URL_DIAMOND)
    doc.setDiCtExperimentInformation("str_save_directory", SAVE_DIRECTORY)
    doc.setDiCtExperimentInformation(
        "str_share_directory_in_storage", SHARE_DIRECTORY_IN_STORAGE
    )
    messageSender = TyMessageSender(URL_DIAMOND, doc)
    sendURL = URL_DIAMOND + f"/login/{strExperimentId}"
    # jsonData = {
    #     "password": hashPass,
    # }
    logger.info(f"sendURL: {sendURL}")
    response = messageSender.sendRequestLogin(strExperimentId, hashPass)
    logger.info(f"responce: {response}")
    assert (response["status_code"] == 200) and (
        response["status"] is True
    ), "Failed to send check experiment ID request"

    logger.info("--------------------------------------------------")

    strExperimentId = "0000-0000-0000"
    rowPass = "wrong_password"
    hashPass = doc.makeHashFromString(rowPass)
    sendURL = URL_DIAMOND + f"/request_one_time_password/{strExperimentId}"
    response = messageSender.sendRequestLogin(strExperimentId, hashPass)
    logger.info(f"responce: {response}")
    assert (response["status_code"] == 404) and (
        response["status"] is False
    ), "Failed to send check experiment ID request"
    logger.info("--------------------------------------------------")

    strExperimentId = "0013-0000-0000"
    rowPass = "wrong_password"
    hashPass = doc.makeHashFromString(rowPass)
    sendURL = URL_DIAMOND + f"/request_one_time_password/{strExperimentId}"
    response = messageSender.sendRequestLogin(strExperimentId, hashPass)
    logger.info(f"responce: {response}")
    assert (response["status_code"] == 404) and (
        response["status"] is False
    ), "Failed to send check experiment ID request"

    logger.info("--------------------------------------------------")

    strExperimentId = "0000-0000-0000"
    rowPass = "password"
    hashPass = doc.makeHashFromString(rowPass)
    jsonData = {
        "password": hashPass,
    }
    sendURL = URL_DIAMOND + f"/request_one_time_password/{strExperimentId}"
    response = messageSender.sendMessage(sendURL, jsonData, "POST")
    logger.info(f"responce: {response}")
    assert (response["status_code"] == 400) and (
        response["status"] is False
    ), "Failed to send check experiment ID request"

    logger.info("--------------------------------------------------")


def test_requestOneTimePassword():
    doc.setUrlBase(URL_DIAMOND)
    doc.setDiCtExperimentInformation("str_save_directory", SAVE_DIRECTORY)
    doc.setDiCtExperimentInformation(
        "str_share_directory_in_storage", SHARE_DIRECTORY_IN_STORAGE
    )
    messageSender = TyMessageSender(URL_DIAMOND, doc)

    strExperimentId = "0000-0000-0000"
    sendURL = URL_DIAMOND + f"/request_one_time_password/{strExperimentId}"
    logger.info(f"sendURL: {sendURL}")
    dataJson = {
        "is_send_to_supervisor": False,
        "is_debug": True,
    }
    response = messageSender.sendMessage(sendURL, dataJson, "POST")
    logger.info(f"responce: {response}")
    assert (response["status_code"] == 200) and (
        response["status"] is True
    ), "Failed to send check experiment ID request"


if __name__ == "__main__":
    # test_sendCheckExperimentId()
    test_sendLogin()
    test_requestOneTimePassword()
