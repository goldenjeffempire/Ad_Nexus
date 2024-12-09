import numpy as np
import matplotlib.pyplot as plt
import random


def simulate_ad_performance(ad_spend, ctr, engagement_rate, days=7):
    """
    Simulate the performance of an ad over a given period.

    Args:
        ad_spend (float): The total budget for the ad campaign.
        ctr (float): The click-through rate as a decimal (e.g., 0.05 for 5%).
        engagement_rate (float): The expected engagement rate as a decimal (e.g., 0.1 for 10% engagement).
        days (int): The number of days to simulate the campaign.

    Returns:
        dict: A dictionary containing daily clicks and engagements.
    """
    clicks = []
    engagements = []

    for day in range(1, days + 1):
        # Simulate daily clicks and engagements
        daily_clicks = ad_spend * ctr
        daily_engagements = daily_clicks * engagement_rate

        clicks.append(daily_clicks)
        engagements.append(daily_engagements)

    # Plot the simulated performance
    plt.figure(figsize=(12, 6))

    # Click performance plot
    plt.subplot(1, 2, 1)
    plt.plot(range(1, days + 1), clicks, label="Clicks", color="blue")
    plt.xlabel("Day")
    plt.ylabel("Number of Clicks")
    plt.title("Ad Click Performance")
    plt.legend()

    # Engagement performance plot
    plt.subplot(1, 2, 2)
    plt.plot(range(1, days + 1), engagements, label="Engagements", color="green")
    plt.xlabel("Day")
    plt.ylabel("Number of Engagements")
    plt.title("Ad Engagement Performance")
    plt.legend()

    plt.tight_layout()
    plt.show()

    return {"clicks": clicks, "engagements": engagements}


def simulate_campaign_performance(budget, audience_size, engagement_rate):
    """
    Simulate campaign performance based on input parameters.

    Args:
        budget (float): The total budget for the campaign.
        audience_size (int): The size of the target audience.
        engagement_rate (float): The expected engagement rate as a decimal.

    Returns:
        dict: A dictionary containing estimated reach, engagement, and ROI.
    """
    performance = {
        "estimated_reach": int(audience_size * (budget / 1000)),
        "estimated_engagement": int(engagement_rate * (budget / 1000)),
        "estimated_roi": round(random.uniform(0.5, 1.5), 2),  # Randomized ROI between 50% and 150%
    }
    return performance


def simulate_full_campaign(ad_spend, ctr, engagement_rate, budget, audience_size, days=7):
    """
    Simulates both ad performance and campaign performance.

    Args:
        ad_spend (float): The total budget for the ad simulation.
        ctr (float): The click-through rate for the ad simulation.
        engagement_rate (float): The engagement rate for both simulations.
        budget (float): The total budget for the campaign.
        audience_size (int): The size of the target audience.
        days (int): The number of days to simulate the ad campaign.

    Returns:
        dict: A dictionary containing ad performance and campaign performance results.
    """
    print("Simulating Ad Performance...")
    ad_performance = simulate_ad_performance(ad_spend, ctr, engagement_rate, days)

    print("\nSimulating Campaign Performance...")
    campaign_performance = simulate_campaign_performance(budget, audience_size, engagement_rate)

    print("\nCampaign Performance Summary:")
    print(f"Estimated Reach: {campaign_performance['estimated_reach']}")
    print(f"Estimated Engagement: {campaign_performance['estimated_engagement']}")
    print(f"Estimated ROI: {campaign_performance['estimated_roi']}x")

    return {
        "ad_performance": ad_performance,
        "campaign_performance": campaign_performance,
    }


# Example usage
if __name__ == "__main__":
    ad_spend = 100  # Total ad spend in dollars
    ctr = 0.05  # 5% click-through rate
    engagement_rate = 0.1  # 10% engagement rate
    budget = 1000  # Campaign budget in dollars
    audience_size = 50000  # Total target audience size
    days = 7  # Campaign duration in days

    results = simulate_full_campaign(ad_spend, ctr, engagement_rate, budget, audience_size, days)
