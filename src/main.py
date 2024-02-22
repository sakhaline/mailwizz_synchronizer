from datetime import datetime, timedelta
from pprint import pprint

import requests
from mailwizz.base import Base
from mailwizz.config import Config
from mailwizz.endpoint.campaigns import Campaigns

from db.mysql import m_queries as mysql
from db.postgres import p_queries as postgres
from logging_config import logger

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

setup()


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

    # logger.info(
        # f"{get_campaign_details.__name__} -- STATUS CODE - {status_code}; RESPONSE DATA - {data}")
    return data


def main():
    last_campaign_id = mysql.get_last_campaign_uuid()

    if last_campaign_id:
        matched_campaigns = [item for item in get_weekly_campaigns() if item["campaign_uid"] == last_campaign_id]

        if matched_campaigns:
            campaign = matched_campaigns[-1]
        
            campaign_uid = last_campaign_id
            name = campaign["name"]
            status = campaign["status"]
            _type = campaign["type"]

            campaign_detailed_data = get_campaign_details(last_campaign_id)

            if campaign_detailed_data:
                # Extracting detailed data
                bounces_count = campaign_detailed_data["bounces_count"]
                campaign_status = campaign_detailed_data["campaign_status"]
                clicks_count = campaign_detailed_data["clicks_count"]
                complaints_rate = campaign_detailed_data["complaints_rate"]
                delivery_error_count = campaign_detailed_data["delivery_error_count"]
                delivery_error_rate = campaign_detailed_data["delivery_error_rate"]
                delivery_success_count = campaign_detailed_data["delivery_success_count"]
                delivery_success_rate = campaign_detailed_data["delivery_success_rate"]
                hard_bounces_count = campaign_detailed_data["hard_bounces_count"]
                hard_bounces_rate = campaign_detailed_data["hard_bounces_rate"]
                internal_bounces_count = campaign_detailed_data["internal_bounces_count"]
                internal_bounces_rate = campaign_detailed_data["internal_bounces_rate"]
                opens_count = campaign_detailed_data["opens_count"]
                opens_rate = campaign_detailed_data["opens_rate"]
                processed_count = campaign_detailed_data["processed_count"]
                soft_bounces_count = campaign_detailed_data["soft_bounces_count"]
                soft_bounces_rate = campaign_detailed_data["soft_bounces_rate"]
                subscribers_count = campaign_detailed_data["subscribers_count"]
                unique_clicks_count = campaign_detailed_data["unique_clicks_count"]
                unique_clicks_rate = campaign_detailed_data["unique_clicks_rate"]
                unique_opens_count = campaign_detailed_data["unique_opens_count"]
                unique_opens_rate = campaign_detailed_data["unique_opens_rate"]
                unsubscribes_count = campaign_detailed_data["unsubscribes_count"]
                unsubscribes_rate = campaign_detailed_data["unsubscribes_rate"]
                clicks_rate = campaign_detailed_data["clicks_rate"]
                complaints_count = campaign_detailed_data["complaints_count"]

                # Forming the data tuple
                insert_data = (
                    campaign_uid, name, status, _type, bounces_count, campaign_status, clicks_count, complaints_rate,
                    delivery_error_count, delivery_error_rate, delivery_success_count, delivery_success_rate,
                    hard_bounces_count, hard_bounces_rate, internal_bounces_count, internal_bounces_rate,
                    opens_count, opens_rate, processed_count, soft_bounces_count, soft_bounces_rate,
                    subscribers_count, unique_clicks_count, unique_clicks_rate, unique_opens_count,
                    unique_opens_rate, unsubscribes_count, unsubscribes_rate, clicks_rate, complaints_count
                )

                # Inserting data into PostgreSQL
                postgres.insert_mailwizz_campaign_data(insert_data)
                logger.info("MAILWIZZ SYNCHRONIZATION FINISHED")


if __name__ == "__main__":
    
    main()