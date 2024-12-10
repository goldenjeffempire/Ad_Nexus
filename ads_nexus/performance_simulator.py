import random
from .models import AdCampaign, AdPerformance

# Function to simulate the ad's performance
def simulate_ad_performance(ad_campaign):
    # Simulate engagement rate based on the ad's budget
    engagement_rate = random.uniform(0.05, 0.25) * ad_campaign.budget

    # Simulate estimated impressions based on target audience size (randomly generated for simplicity)
    estimated_impressions = random.randint(1000, 10000) * (ad_campaign.budget / 1000)

    # Simulate clicks based on engagement rate
    clicks = int(engagement_rate * estimated_impressions)

    # Store the simulated performance data in the database
    ad_performance = AdPerformance(
        ad_campaign=ad_campaign,
        engagement_rate=engagement_rate,
        estimated_impressions=estimated_impressions,
        clicks=clicks
    )
    ad_performance.save()

    return ad_performance
