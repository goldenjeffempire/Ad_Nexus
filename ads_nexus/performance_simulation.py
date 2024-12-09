import random

def simulate_campaign_performance(budget, audience_size, engagement_rate):
    # Simulate campaign performance based on input parameters
    performance = {
        'estimated_reach': int(audience_size * (budget / 1000)),
        'estimated_engagement': int(engagement_rate * (budget / 1000)),
        'estimated_roi': random.uniform(0.5, 1.5),  # Randomized ROI between 50% and 150%
    }
    return performance
