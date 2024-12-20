from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights

class FacebookAdAnalytics:
    def __init__(self, access_token, app_id, app_secret):
        self.access_token = access_token
        self.app_id = app_id
        self.app_secret = app_secret
        self.api = FacebookAdsApi.init(self.app_id, self.app_secret, self.access_token)

    def get_ad_performance(self, ad_account_id, since, until):
        ad_account = AdAccount(ad_account_id)
        params = {
            'time_range': {'since': since, 'until': until},
            'fields': ['impressions', 'clicks', 'spend', 'cpc', 'ctr', 'conversions'],
        }
        insights = ad_account.get_insights(params=params)
        return insights
