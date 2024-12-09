from facebook_business.adobjects.campaign import Campaign
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.account import AdAccount

# Initialize the Facebook Ads API
access_token = 'your_facebook_access_token'
ad_account_id = 'your_ad_account_id'
app_id = 'your_app_id'
app_secret = 'your_app_secret'

FacebookAdsApi.init(app_id, app_secret, access_token)

# Function to create a new campaign
def create_facebook_campaign(name, objective, status):
    account = AdAccount(ad_account_id)
    campaign = account.create_campaign(
        params={
            'name': name,
            'objective': objective,
            'status': status,
        }
    )
    return campaign
