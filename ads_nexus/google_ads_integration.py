from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException

# Initialize Google Ads API client
google_ads_client = GoogleAdsClient.load_from_storage('google-ads.yaml')

# Function to create a new Google Ads campaign
def create_google_ads_campaign(customer_id, campaign_name, budget_amount):
    campaign_service = google_ads_client.get_service('CampaignService')

    # Define the campaign configuration
    campaign = {
        "name": campaign_name,
        "advertising_channel_type": "SEARCH",
        "status": "PAUSED",
        "campaign_budget": budget_amount,
    }

    try:
        campaign_operation = client.get_type("CampaignOperation")
        campaign_operation.create.CopyFrom(campaign)
        response = campaign_service.mutate_campaigns(customer_id, [campaign_operation])
        return response
    except GoogleAdsException as ex:
        print(f"Google Ads API error: {ex.failure}")
        return None
