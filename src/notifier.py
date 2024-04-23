import os
import json

import requests
from dotenv import load_dotenv


load_dotenv()

RETOOL_WF_WEBHOOK = os.getenv("WF_WEBHOOK", "")


def get_payload(file_path):
    print("START PAYLOAD FETCHING")
    with open(file_path, "r") as f:
        payload = json.load(f)
        print(f"PAYLOAD FETCHED SUCCESSFULLY:\n {payload}")
    return payload


def send_email(url, payload):
    print("START EMAIL SENDING")
    response = requests.post(url=url, json=payload)
    if response.status_code == 200:
        print("success")
    else:
        print(response.status_code)
