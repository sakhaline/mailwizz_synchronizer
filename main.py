from datetime import datetime, timedelta
import requests
import pprint
from mailwizz.base import Base
from mailwizz.config import Config
from mailwizz.endpoint.campaigns import Campaigns
from logging_config import logger


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
    endpoint = Campaigns()

    response = endpoint.get_campaigns(page=1, per_page=100)

    result = response.json()
    campaigns_list = result["data"]["records"]
    weekly_campaigns_list = [campaign for campaign in campaigns_list if "Weekly" in campaign["name"]]

    # logger.info(f"FOUND WEEKLY CAMPAIGNS - {weekly_campaigns_list}")
    return weekly_campaigns_list



if __name__ == "__main__":
    setup()

    # weekly_campaigns = get_weekly_campaigns()
    # print(weekly_campaigns[0])

    


    # campaign_id = weekly_campaigns_list[1]["campaign_uid"]
    # response = endpoint.get_campaign(campaign_id)

    res = requests.get(
        url="https://mailwizz.findbusinesses4sale.com/api/campaigns/fl689t2d62fcc/stats",
        headers={
            'X-Api-Key': '635b076cd37ea8c1957337f8b8e386b953270b51'
        }
    )
    pprint.pprint(res.json())