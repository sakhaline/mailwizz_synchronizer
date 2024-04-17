import os

import json
import requests
from dotenv import load_dotenv
from mailwizz.base import Base
from mailwizz.config import Config
from mailwizz.endpoint.campaigns import Campaigns
# from db.mysql import m_queries as mysql
# from db.postgres import p_queries as postgres
from logging_config import logger
from pprint import pprint
from datetime import datetime

load_dotenv()

ENDPOINT = Campaigns()
RETOOL_API_KEY = os.getenv("workflowApiKey", "")


def setup():
    """
    opens access to MailWizz API
    """

    logger.info("SETTING UP MAILWIZZ")

    config = Config({
        'api_url': os.getenv("MAILWIZZ_API_URL"),
        'public_key': os.getenv("MAILWIZZ_PUBLIC_KEY"),
        'private_key': os.getenv("MAILWIZZ_PRIVATE_KEY"),
        'charset': 'utf-8'
    })
    Base.set_config(config)
    return True

setup()


def get_weekly_campaigns() -> list[dict]:
    """
    gets a list of MailWizz campaigns
    """

    logger.info("GETTING WEEKLY CAMPAIGNS")

    response = ENDPOINT.get_campaigns(page=1, per_page=100)
    result = response.json()
    campaigns_list = result["data"]["records"]

    return campaigns_list


def filter_campaigns_by_name(campaigns: list[dict]) -> list[dict]:
    filtered_campaigns = list(
        filter(lambda campaign: "daily" not in campaign.get("name", "").lower(), campaigns)
    )
    logger.info(f"{filter_campaigns_by_name.__name__} -- FINIS WEEDING OUT DAILY CAMPAIGNS ^_^\n"
                f"SUCCESSFULLY REMOVED: {len(campaigns) - len(filtered_campaigns)}")
    return filtered_campaigns
    

def get_campaign_details(campaign_uuid: str) -> dict:
    """
    gets detailed data about MailWizz campaign by it's uniques UUID
    """

    logger.info(f"GETTING WEEKLY CAMPAIGN DATA - {campaign_uuid}")

    response = requests.get(
        url=f"{os.getenv('MAILWIZZ_BASE_URL')}api/campaigns/{campaign_uuid}/stats",
        headers={
            'X-Api-Key': os.getenv("MAILWIZZ_X_API_KEY")
        }
    )

    data = {}

    try:
        data = response.json()["data"]
    except Exception as ex:
        logger.error(
            f"{get_campaign_details.__name__} -- !!! ERROR OCCURRED - {ex}")
    return data


def process_campaign_list() -> None:
    logger.info(f"{process_campaign_list.__name__} -- START CAMPAIGN LIST PROCESSING")
    data = []

    raw_campaigns = get_weekly_campaigns()
    filtered_campaigns = filter_campaigns_by_name(raw_campaigns)

    for campaign in filtered_campaigns:
        uuid = campaign.get("campaign_uid", "")
        name = campaign.get("name", "")
        c_type = campaign.get("type", "")

        if uuid:
            campaign_details = get_campaign_details(uuid)
            campaign_details["name"] = name
            campaign_details["campaign_uid"] = uuid
            campaign_details["type"] = c_type
            data.append(campaign_details)

            with open("campaigns.json", "w") as file:
                json.dump(data, file, indent=4)
        else:
            logger.info(f"{process_campaign_list.__name__} -- CAMPAIGN UUID: #{uuid} NOT FOUND")

    logger.info(f"{process_campaign_list.__name__} -- FINISH CAMPAIGN LIST PROCESSING.\n"
                f"#{len(data)} CAMPAIGNS DUMPED TO JSON SUCCESSFULLY ^_^")


def prepare_retool_json() -> None:
    retool_data = []
    campaign = {}

    with open("campaigns.json", "r") as file:
        api_data = json.load(file)

    for c in api_data:
        campaign["name"] = c.get("name", "")
        campaign["campaign_uid"] = c.get("campaign_uid", "")
        campaign["type"] = c.get("type", "")
        campaign["status"] = c.get("campaign_status", "")
        campaign["bounces_count"] = c.get("bounces_count", "")
        campaign["bounces_rate"] = c.get("bounces_rate", "")
        campaign["hard_bounces_count"] = c.get("hard_bounces_count", "")
        campaign["hard_bounces_rate"] = c.get("hard_bounces_rate", "")
        campaign["soft_bounces_count"] = c.get("soft_bounces_count", "")
        campaign["soft_bounces_rate"] = c.get("soft_bounces_rate", "")
        campaign["internal_bounces_count"] = c.get("internal_bounces_count", "")
        campaign["complaints_rate"] = c.get("complaints_rate", "")
        campaign["complaints_count"] = c.get("complaints_count", "")
        campaign["unsubscribes_rate"] = c.get("unsubscribes_rate", "")
        campaign["unsubscribes_count"] = c.get("unsubscribes_count", "")
        campaign["unique_clicks_rate"] = c.get("unique_clicks_rate", "")
        campaign["unique_clicks_count"] = c.get("unique_clicks_count", "")
        campaign["clicks_rate"] = c.get("clicks_rate", "")
        campaign["clicks_count"] = c.get("clicks_count", "")
        campaign["unique_opens_rate"] = c.get("unique_opens_rate", "")
        campaign["unique_opens_count"] = c.get("unique_opens_count", "")
        campaign["opens_rate"] = c.get("opens_rate", "")
        campaign["opens_count"] = c.get("opens_count", "")
        campaign["delivery_error_rate"] = c.get("delivery_error_rate", "")
        campaign["delivery_error_count"] = c.get("delivery_error_count", "")
        campaign["delivery_success_rate"] = c.get("delivery_success_rate", "")
        campaign["delivery_success_count"] = c.get("delivery_success_count", "")
        campaign["processed_count"] = c.get("processed_count", "")
        campaign["subscribers_count"] = c.get("subscribers_count", "")
        campaign["date"] = str(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'))

        retool_data.append(campaign)
        with open("retool_payload.json", "w") as file:
            json.dump(retool_data, file, indent=4)
        campaign = {}


def retool_send_data() -> None:
    URL = ("https://api.retool.com/v1/workflows/58bf7bb8-ab22-4f73-b737"
        f"-98ef499abf02/startTrigger?workflowApiKey={RETOOL_API_KEY}")

    with open("retool_payload.json", "r") as file:
        payload = json.load(file)

    response = requests.post(url=URL, json=payload)
    if response.status_code == 200:
        logger.info(f"{main.__name__} -- DATA SEND SUCCESSFULLY!!!")
    else:
        logger.error(f"{main.__name__} -- DATA SENDING FAILED")


def main(postgres_access: bool = False) -> dict:
    process_campaign_list()
    if postgres_access:
        logger.info(f"{main.__name__} -- MODE - POSTGRES DIRECT ACCESS")
    else:
        logger.info(f"{main.__name__} -- MODE - RETOOL API")
        prepare_retool_json()
        retool_send_data()
    # # TODO: 
    # # 5: notify ACTSE team by email about sync result (see description in Telegram)
    # # NOTE:
    # # automation should run once a Week (Tuesday|Wednesday is preferred)


if __name__ == "__main__":
    main()