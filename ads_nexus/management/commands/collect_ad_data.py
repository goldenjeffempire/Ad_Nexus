from django.core.management.base import BaseCommand
from datetime import date
from ads_nexus.models import AdCampaign, AdAnalytics, ContentRecommendation

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

class Command(BaseCommand):
    help = 'Generate content recommendations for all users'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            recommendations = generate_recommendations(user)
            for rec in recommendations:
                ContentRecommendation.objects.create(
                    user=user,
                    recommended_content=rec['ad_campaign'],
                    recommendation_score=rec['score'],
                    date_recommended=date.today()
                )
            self.stdout.write(self.style.SUCCESS(f'Recommendations generated for {user.username}'))
