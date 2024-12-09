from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad

class FacebookAdManager:
    def __init__(self, access_token, ad_account_id):
        self.access_token = access_token
        self.ad_account_id = ad_account_id
        self.api = FacebookAdsApi.init(access_token=self.access_token)
        self.ad_account = AdAccount(f'act_{ad_account_id}')

    def create_campaign(self, name, objective):
        campaign = Campaign(parent_id=self.ad_account.get_id())
        campaign.update({
            'name': name,
            'objective': objective,
            'status': 'PAUSED',
        })
        campaign.remote_create()
        return campaign

    def create_adset(self, campaign_id, name, targeting, daily_budget, start_time, end_time):
        adset = AdSet(parent_id=campaign_id)
        adset.update({
            'name': name,
            'campaign_id': campaign_id,
            'targeting': targeting,
            'daily_budget': daily_budget,
            'start_time': start_time,
            'end_time': end_time,
            'status': 'PAUSED',
        })
        adset.remote_create()
        return adset

    def create_ad(self, adset_id, name, creative_id):
        ad = Ad(parent_id=adset_id)
        ad.update({
            'name': name,
            'adset_id': adset_id,
            'creative': {
                'creative_id': creative_id,
            },
            'status': 'PAUSED',
        })
        ad.remote_create()
        return ad
