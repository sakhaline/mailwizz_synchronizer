import os

from dotenv import load_dotenv

from notifier import get_payload, send_email
from retool_sync import process_campaign_list, prepare_retool_json, retool_send_data
from logger.logging_config import logger


load_dotenv()

BASEDIR = os.getcwd()
RETOOL_WF_WEBHOOK = os.getenv("WF_WEBHOOK", "")


def syncronize(postgres_access: bool = False) -> dict:
    process_campaign_list()
    if postgres_access:
        logger.info(f"{syncronize.__name__} -- MODE - POSTGRES DIRECT ACCESS")
    else:
        logger.info(f"{syncronize.__name__} -- MODE - RETOOL API")
        prepare_retool_json()
        retool_send_data()


def send_team_email(url) -> None:
    email_payload = os.path.join(BASEDIR, "data", "email_payload.json")
    payload = get_payload(email_payload)
    send_email(url, payload)
    logger.info(f"{syncronize.__name__} -- FINISH SCRIPT RUNNING")
