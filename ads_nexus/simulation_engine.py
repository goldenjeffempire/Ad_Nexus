import random
from .models import AdSimulation

def simulate_ad_performance(ad_id):
    try:
        # Fetch the ad
        ad = Ad.objects.get(id=ad_id)
    except Ad.DoesNotExist:
        return None

    # Generate simulated metrics
    impressions = random.randint(1000, 5000)
    clicks = random.randint(100, impressions // 2)
    conversions = random.randint(10, clicks // 5)
    ctr = (clicks / impressions) * 100  # Click-Through Rate
    conversion_rate = (conversions / clicks) * 100 if clicks > 0 else 0

    # Save simulation results
    simulation = AdSimulation.objects.create(
        ad=ad,
        impressions=impressions,
        clicks=clicks,
        conversions=conversions,
        ctr=ctr,
        conversion_rate=conversion_rate,
    )

    return simulation
