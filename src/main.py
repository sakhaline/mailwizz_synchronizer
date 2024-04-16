import os

import requests
from dotenv import load_dotenv
from mailwizz.base import Base
from mailwizz.config import Config
from mailwizz.endpoint.campaigns import Campaigns
from db.mysql import m_queries as mysql
from db.postgres import p_queries as postgres
from logging_config import logger

load_dotenv()

ENDPOINT = Campaigns()


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


def get_weekly_campaigns():
    """
    gets a list of MailWizz campaigns
    """

    logger.info("GETTING WEEKLY CAMPAIGNS")

    response = ENDPOINT.get_campaigns(page=1, per_page=100)

    result = response.json()

    campaigns_list = result["data"]["records"]

    print(campaigns_list)

    needed_campaigns_list = [
        campaign for campaign in campaigns_list if "Daily" not in campaign["name"]]

    return needed_campaigns_list


def get_campaign_details(campaign_uuid):
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


def main(postgres_access: bool = False) -> dict:

    # TODO: 
    # 1: get a list of campaigns (not Daily)
    # 2: fetch all necessary data for those campaigns
    # 3: prepare insert payload in format -> list[dict]
    # 4: send data to retool | insert to postgres
    # 5: notify ACTSE team by email about sync result

    result = {
        "success": False
    }

    if postgres_access:
        logger.info(f"{main.__name__} -- MODE - POSTGRES DIRECT ACCESS")
    else:
        logger.info(f"{main.__name__} -- MODE - RETOOL API")

    return result


if __name__ == "__main__":
    ...