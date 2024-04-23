import os
import json

import requests
from dotenv import load_dotenv
from logger.logging_config import logger


load_dotenv()

RETOOL_WF_WEBHOOK = os.getenv("WF_WEBHOOK", "")


def get_payload(file_path):
    with open(file_path, "r") as f:
        payload = json.load(f)
    return payload


def send_email(url, payload):
    logger.info(f"{send_email.__name__} -- START EMAIL NOTIFICATION")
    response = requests.post(url=url, json=payload)
    if response.status_code == 200:
        logger.info(f"{send_email.__name__} -- EMAIL SENT SUCCESSFULLY")
    else:
        logger.error(f"{send_email.__name__} -- EMAIL SENDING FAILED WITH STATUS CODE:\nf{response.status_code}")
