from django.urls import path
from . import views

urlpatterns = [
    path('recommendations/', ad_recommendations, name='ad_recommendations'),
    path('simulate/<int:ad_id>/', ad_simulation, name='ad_simulation'),
    path('creativity-booster/', ai_creativity_booster, name='ai_creativity_booster'),
    path('social-media/', social_media_dashboard, name='social_media_dashboard'),
    path('social-media/connect/<int:platform_id>/', connect_social_media_account, name='connect_social_media_account'),
    path('campaigns/create/', create_ad_campaign, name='create_ad_campaign'),
    path('campaigns/<int:campaign_id>/targeting/', set_ad_targeting, name='set_ad_targeting'),
    path('campaigns/<int:campaign_id>/simulate/', simulate_performance, name='simulate_performance'),
    path('generate-ad-content/', generate_ad_content, name='generate_ad_content'),
    path('social-media-dashboard/', social_media_dashboard, name='social_media_dashboard'),
    path('chatbot/', chatbot_view, name='chatbot'),
    path('marketing-coach/', marketing_coach, name='marketing_coach'),
    path('recommendations/', content_recommendation, name='recommendations'),
    path('performance-simulation/', performance_simulation, name='performance_simulation'),
    path('creativity-boost/', creativity_boost, name='creativity_boost'),
    path('chatbot/', chatbot_interaction, name='chatbot_interaction'),
    path('manage_campaigns/', manage_campaigns, name='manage_campaigns'),
    path('content_recommendations/', content_recommendations, name='content_recommendations'),
    path('chatbot/', chatbot_interface, name='chatbot_interface'),
    path('create-ad/', create_facebook_ad, name='create_facebook_ad'),
    path('ai-tools-dashboard/', ai_tools_dashboard, name='ai_tools_dashboard'),
    path('ad/<int:ad_id>/', views.ad_detail, name='ad_detail'),
    path('analytics/', views.analytics, name='analytics'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('ad_performance/<int:campaign_id>/', views.ad_performance, name='ad_performance'),]
    path('manage_ad_campaign/<int:campaign_id>/', views.manage_ad_campaign, name='manage_ad_campaign'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('get_chatbot_response/', views.get_chatbot_response_view, name='get_chatbot_response'),
    path('link_social_media_account/', views.link_social_media_account, name='link_social_media_account'),
    path('social_media_accounts/', views.social_media_accounts, name='social_media_accounts'),
    path('engagement_insights/<int:account_id>/', views.view_engagement_insights, name='view_engagement_insights'),
    path('schedule_post/<int:account_id>/', views.schedule_post, name='schedule_post'),
]

