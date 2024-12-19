from django.core.management.base import BaseCommand
from datetime import date
from myapp.models import AdCampaign, AdAnalytics

class Command(BaseCommand):
    help = 'Collect ad performance data for campaigns'

    def handle(self, *args, **kwargs):
        campaigns = AdCampaign.objects.all()
        for campaign in campaigns:
            impressions = 1000  # Example data - replace with actual metrics
            clicks = 100        # Example data - replace with actual metrics
            conversions = 20    # Example data - replace with actual metrics
            analytics = AdAnalytics(
                ad_campaign=campaign,
                date=date.today(),
                impressions=impressions,
                clicks=clicks,
                conversions=conversions
            )
            analytics.save()
            self.stdout.write(self.style.SUCCESS(f'Collected data for campaign {campaign.campaign_name}'))
