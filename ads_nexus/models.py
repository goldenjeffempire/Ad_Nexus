from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    interests = models.TextField()  # Store user interests as a JSON string
    preferences = models.TextField()  # Store preferences for ad categories

    def __str__(self):
        return self.user.username

class Ad(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    target_audience = models.TextField()  # JSON string defining audience attributes
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Recommendation(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    score = models.FloatField()  # Relevance score

    def __str__(self):
        return f"{self.user.user.username} -> {self.ad.title} (Score: {self.score})"

class AdSimulation(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    impressions = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    conversions = models.IntegerField(default=0)
    ctr = models.FloatField(default=0.0)  # Click-Through Rate
    conversion_rate = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Simulation for {self.ad.title} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

class SocialMediaPlatform(models.Model):
    name = models.CharField(max_length=100)
    api_url = models.URLField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class SocialMediaAccount(models.Model):
    PLATFORM_CHOICES = [
        ('FB', 'Facebook'),
        ('IG', 'Instagram'),
        ('TW', 'Twitter'),
        ('TK', 'Tiktok'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=2, choices=PLATFORM_CHOICES)
    platform_username = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_platform_display()} account for {self.user.username}"

class AdCampaign(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    audience_size = models.IntegerField()

    def __str__(self):
        return self.name

class AdTargeting(models.Model):
    campaign = models.OneToOneField(AdCampaign, on_delete=models.CASCADE, related_name='targeting')
    age_range = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    interests = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Targeting for {self.campaign.name}"

class AdPerformance(models.Model):
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE, related_name='performance')
    date = models.DateField()
    platform = models.CharField(max_length=50)  # e.g., Facebook, Instagram, Twitter, Tiktok, etc.
    impressions = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    conversions = models.IntegerField(default=0)
    engagement_rate = models.FloatField(default=0.0)
    conversion_rate = models.FloatField(default=0.0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    ctr = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # Click-through rate
    cpc = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Cost per click
    roi = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Return on investment
    updated_at = models.DateTimeField(default=timezone.now)

    def calculate_ctr(self):
        """Calculate Click-through Rate (CTR)."""
        if self.impressions > 0:
            self.ctr = (self.clicks / self.impressions) * 100
        else:
            self.ctr = 0

    def calculate_cpc(self, ad_spend):
        """Calculate Cost per Click (CPC)."""
        if self.clicks > 0:
            self.cpc = ad_spend / self.clicks
        else:
            self.cpc = 0

    def calculate_roi(self, ad_spend, revenue):
        """Calculate Return on Investment (ROI)."""
        if ad_spend > 0:
            self.roi = (revenue - ad_spend) / ad_spend * 100
        else:
            self.roi = 0

    def calculate_conversion_rate(self):
        """Calculate Conversion Rate."""
        if self.impressions > 0:
            self.conversion_rate = (self.conversions / self.impressions) * 100
        else:
            self.conversion_rate = 0

    def save(self, *args, **kwargs):
        """Override save method to auto-calculate metrics before saving."""
        self.calculate_ctr()
        self.calculate_conversion_rate()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Performance for {self.campaign.title} on {self.platform}"

class SocialShareAnalytics(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    platform = models.CharField(max_length=50)
    share_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.ad.title} shared on {self.platform}'

class UserDemographics(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Demographics"

class UserBehavior(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    interests = models.JSONField(default=list)  # Store interests as a list of strings
    past_ad_interactions = models.JSONField(default=list)  # Store interaction data as JSON

    def __str__(self):
        return f"{self.user.username}'s Behaviors"

class ChatHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat with {self.user.username} at {self.timestamp}"

class AIChatbot(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question

class EngagementInsight(models.Model):
    social_media_account = models.ForeignKey(SocialMediaAccount, on_delete=models.CASCADE)
    date = models.DateField()
    likes = models.PositiveIntegerField()
    comments = models.PositiveIntegerField()
    shares = models.PositiveIntegerField()
    reach = models.PositiveIntegerField()  # Total reach of the post
    impressions = models.PositiveIntegerField()  # How many times the post was seen

    def __str__(self):
        return f"Insights for {self.social_media_account.account_name} on {self.date}"

class ScheduledPost(models.Model):
    social_media_account = models.ForeignKey(SocialMediaAccount, on_delete=models.CASCADE)
    post_content = models.TextField()  # Content of the post (text, images, etc.)
    scheduled_time = models.DateTimeField()  # Time when the post will go live
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('posted', 'Posted')])

    def __str__(self):
        return f"Post for {self.social_media_account.account_name} scheduled for {self.scheduled_time}"

class TargetAudience(models.Model):
    ad_campaign = models.ForeignKey(AdCampaign, on_delete=models.CASCADE)
    age_range = models.CharField(max_length=50)  # e.g., "18-24"
    location = models.CharField(max_length=100)  # Location-based targeting
    interests = models.TextField()  # Interests based targeting
    behavior = models.TextField()  # Behavioral data (e.g., "frequent shoppers", "tech enthusiasts")

    def __str__(self):
        return f"Audience for {self.ad_campaign.campaign_name}"

class AdCreative(models.Model):
    ad_campaign = models.ForeignKey(AdCampaign, on_delete=models.CASCADE)
    creative_type = models.CharField(max_length=50, choices=[('image', 'Image'), ('video', 'Video')])
    creative_url = models.URLField()  # URL to the hosted creative (image or video)
    description = models.TextField()  # Description of the ad creative

    def __str__(self):
        return f"Creative for {self.ad_campaign.campaign_name}"

class SplitTest(models.Model):
    ad_campaign = models.ForeignKey(AdCampaign, on_delete=models.CASCADE)
    version_name = models.CharField(max_length=100)  # e.g., "Version A", "Version B"
    creative = models.ForeignKey(AdCreative, on_delete=models.CASCADE)  # Link to the ad creative being tested
    impressions = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Split Test for {self.ad_campaign.campaign_name} - {self.version_name}"

class AdAnalytics(models.Model):
    ad_campaign = models.ForeignKey(AdCampaign, on_delete=models.CASCADE)
    date = models.DateField()
    impressions = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    conversions = models.PositiveIntegerField(default=0)  # Conversions represent the number of actions taken, like purchases or sign-ups
    click_through_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    conversion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Analytics for {self.ad_campaign.campaign_name} on {self.date}"

    def save(self, *args, **kwargs):
        if self.impressions > 0:
            self.click_through_rate = (self.clicks / self.impressions) * 100
        if self.impressions > 0:
            self.conversion_rate = (self.conversions / self.impressions) * 100
        super().save(*args, **kwargs)

class ContentRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recommended_content = models.ForeignKey(AdCampaign, on_delete=models.CASCADE)
    recommendation_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    date_recommended = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation for {self.user.username}: {self.recommended_content.campaign_name}"

from django.db import models

class SocialMediaPost(models.Model):
    account = models.ForeignKey(SocialMediaAccount, on_delete=models.CASCADE)
    post_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post_url = models.URLField()

    def __str__(self):
        return f"Post for {self.account.platform_username} on {self.created_at}"

class EngagementMetric(models.Model):
    post = models.OneToOneField(SocialMediaPost, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    reach = models.IntegerField(default=0)  # Reach refers to how many users saw the post

    def __str__(self):
        return f"Engagement for {self.post} - Likes: {self.likes}, Comments: {self.comments}, Shares: {self.shares}, Reach: {self.reach}"

class AdPerformanceSimulation(models.Model):
    post = models.OneToOneField(SocialMediaPost, on_delete=models.CASCADE)
    impressions = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    conversions = models.IntegerField(default=0)
    estimated_roi = models.FloatField(default=0.0)  # Estimated return on investment

    def simulate_performance(self):
        # Simple algorithm to estimate performance
        click_through_rate = (self.clicks / self.impressions) * 100 if self.impressions > 0 else 0
        conversion_rate = (self.conversions / self.clicks) * 100 if self.clicks > 0 else 0
        self.estimated_roi = conversion_rate * 1.5  # Example ROI based on conversion rate
        self.save()

    def __str__(self):
        return f"Ad Performance for {self.post} - Estimated ROI: {self.estimated_roi}%"

class Platform(models.Model):
    name = models.CharField(max_length=100)
    api_url = models.URLField()

    def __str__(self):
        return self.name

class CrossPlatformCampaign(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    platforms = models.ManyToManyField(Platform, related_name='campaigns')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('active', 'Active'), ('completed', 'Completed')], default='pending')

    def __str__(self):
        return self.name

class SocialMediaAPI(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('tiktok', 'Tiktok'),
    ]

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    api_key = models.CharField(max_length=255)
    api_secret = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
    access_token_secret = models.CharField(max_length=255, null=True, blank=True)  # For platforms like Twitter

    def __str__(self):
        return f"{self.platform} API Settings"

class Content(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    tags = models.JSONField()  # Tags for content, to help with content-based recommendations
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Interaction(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.ForeignKey('Content', on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=50)  # Like, View, Comment, etc.
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.interaction_type} on {self.content.title}"
