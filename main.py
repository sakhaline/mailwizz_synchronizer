from datetime import datetime, timedelta
import requests
import pprint
from mailwizz.base import Base
from mailwizz.config import Config
from mailwizz.endpoint.campaigns import Campaigns

def setup():

    # configuration object
    config = Config({
        'api_url': 'https://mailwizz.findbusinesses4sale.com/api',
        'public_key': '635b076cd37ea8c1957337f8b8e386b953270b51',
        'private_key': '635b076cd37ea8c1957337f8b8e386b953270b51',
        'charset': 'utf-8'
    })

    # now inject the configuration and we are ready to make api calls
    Base.set_config(config)

setup()

endpoint = Campaigns()

response = endpoint.get_campaigns(page=1, per_page=100)

result = response.json()
campaigns_list = result["data"]["records"]
weekly_campaigns_list = [campaign for campaign in campaigns_list if "Weekly" in campaign["name"]]
print(weekly_campaigns_list)
campaign_id = weekly_campaigns_list[1]["campaign_uid"]
response = endpoint.get_campaign(campaign_id)

res = requests.get(
    url="https://mailwizz.findbusinesses4sale.com/api/campaigns/lr4120nrqrffe/stats",
    headers={
        'X-Api-Key': '635b076cd37ea8c1957337f8b8e386b953270b51'
    }
)
pprint.pprint(res.json())