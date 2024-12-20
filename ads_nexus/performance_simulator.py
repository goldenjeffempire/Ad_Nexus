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

class PerformanceSimulator:
    def __init__(self, budget, audience_size, ctr_base=0.05, conversion_base=0.1):
        self.budget = budget
        self.audience_size = audience_size
        self.ctr_base = ctr_base  # Base click-through rate
        self.conversion_base = conversion_base  # Base conversion rate

    def simulate_performance(self):
        # Simulate CTR: Higher budget and audience size increases CTR
        ctr = self.ctr_base + (self.budget * 0.0005) + (self.audience_size * 0.0001)
        ctr = min(ctr, 0.2)  # Limit CTR to a maximum of 20%

        # Simulate Conversion Rate: Higher CTR leads to higher conversion rate
        conversion_rate = self.conversion_base + (ctr * 0.2)

        # Simulate Impressions: Based on budget and audience size
        impressions = self.budget * 1000 + (self.audience_size * 500)

        return {
            "CTR": round(ctr * 100, 2),  # Percentage form
            "Conversion Rate": round(conversion_rate * 100, 2),
            "Impressions": impressions
        }
