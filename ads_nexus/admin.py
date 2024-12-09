from django.contrib import admin
from .models import Ad, SocialShareAnalytics

@admin.register(SocialShareAnalytics)
class SocialShareAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('ad', 'platform', 'share_count')
