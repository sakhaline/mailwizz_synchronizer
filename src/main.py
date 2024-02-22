from datetime import datetime, timedelta
import requests
import pprint
from mailwizz.base import Base
from mailwizz.config import Config
from mailwizz.endpoint.campaigns import Campaigns
from src.logging_config import logger
from db.mysql import m_queries as mysql


ENDPOINT = Campaigns()


def setup():
    logger.info("SETTING UP MAILWIZZ")

    config = Config({
        'api_url': 'https://mailwizz.findbusinesses4sale.com/api',
        'public_key': '635b076cd37ea8c1957337f8b8e386b953270b51',
        'private_key': '635b076cd37ea8c1957337f8b8e386b953270b51',
        'charset': 'utf-8'
    })
    Base.set_config(config)
    return True


def get_weekly_campaigns():
    logger.info("GETTING WEEKLY CAMPAIGNS")

    response = ENDPOINT.get_campaigns(page=1, per_page=100)

    result = response.json()
    campaigns_list = result["data"]["records"]
    weekly_campaigns_list = [
        campaign for campaign in campaigns_list if "Weekly" in campaign["name"]]

    # logger.info(f"FOUND WEEKLY CAMPAIGNS - {weekly_campaigns_list}")
    return weekly_campaigns_list


def get_campaign_details(campaign_uuid):
    logger.info(f"GETTING WEEKLY CAMPAIGN DATA - {campaign_uuid}")

    response = requests.get(
        url=f"https://mailwizz.findbusinesses4sale.com/api/campaigns/{campaign_uuid}/stats",
        headers={
            'X-Api-Key': '635b076cd37ea8c1957337f8b8e386b953270b51'
        }
    )

    status_code = response.status_code
    data = {}

    try:
        data = response.json()["data"]
    except Exception as ex:
        logger.error(
            f"{get_campaign_details.__name__} -- !!! ERROR OCCURRED - {ex}")

    logger.info(
        f"{get_campaign_details.__name__} -- STATUS CODE - {status_code}; RESPONSE DATA - {data}")
    return data


def main():
    setup()
    
    last_campaign_id = mysql.get_last_campaign_uuid()

    if last_campaign_id:
        last_campaign_details = get_campaign_details(last_campaign_id)
        
        if last_campaign_details:
            logger.info("SAVING CAMPAIGN DATA TO POSTGRES")
            ...


if __name__ == "__main__":
    main()
