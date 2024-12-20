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
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('marketing-coach/', views.marketing_coach, name='marketing_coach'),
    path('recommendations/', views.content_recommendation, name='recommendations'),
    path('performance-simulation/', views.performance_simulation, name='performance_simulation'),
    path('creativity-boost/', views.creativity_boost, name='creativity_boost'),
    path('chatbot/', views.chatbot_interaction, name='chatbot_interaction'),
    path('manage_campaigns/', views.manage_campaigns, name='manage_campaigns'),
    path('content-recommendations/', views.content_recommendations, name='content_recommendations'),
    path('chatbot/', views.chatbot_interface, name='chatbot_interface'),
    path('create-ad/', views.create_facebook_ad, name='create_facebook_ad'),
    path('ai-tools-dashboard/', views.ai_tools_dashboard, name='ai_tools_dashboard'),
    path('ad/<int:ad_id>/', views.ad_detail, name='ad_detail'),
    path('analytics/', views.analytics, name='analytics'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('ad_performance/<int:campaign_id>/', views.ad_performance, name='ad_performance'),
    path('manage_ad_campaign/<int:campaign_id>/', views.manage_ad_campaign, name='manage_ad_campaign'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('get_chatbot_response/', views.get_chatbot_response_view, name='get_chatbot_response'),
    path('link_social_media_account/', views.link_social_media_account, name='link_social_media_account'),
    path('social_media_accounts/', views.social_media_accounts, name='social_media_accounts'),
    path('engagement_insights/<int:account_id>/', views.view_engagement_insights, name='view_engagement_insights'),
    path('schedule_post/<int:account_id>/', views.schedule_post, name='schedule_post'),
    path('engagement-insights/', views.engagement_insights, name='engagement_insights'),
    path('create-campaign/', views.create_campaign, name='create_campaign'),
    path('view-campaigns/', views.view_campaigns, name='view_campaigns'),
    path('integrate-api/', views.integrate_api, name='integrate_api'),
    path('view-api-settings/', views.view_api_settings, name='view_api_settings'),
    path('send_message', views.send_message, name='send_message'),
]
