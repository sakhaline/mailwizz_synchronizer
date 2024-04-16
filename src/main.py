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
    logger.info("GETTING WEEKLY CAMPAIGNS")

    response = ENDPOINT.get_campaigns(page=1, per_page=100)

    result = response.json()

    campaigns_list = result["data"]["records"]

    print(campaigns_list)

    needed_campaigns_list = [
        campaign for campaign in campaigns_list if "Daily" not in campaign["name"]]

    return needed_campaigns_list


def get_campaign_details(campaign_uuid):
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


def main(insert_mode: int = 1):
    """
    0 - Postgres
    1 - Retool
    """
    ...


if __name__ == "__main__":
    ...